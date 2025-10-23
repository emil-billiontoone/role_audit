#!/usr/bin/env python3
"""
PDF Report Generator for Role Permission Tests
===============================================
Reads all_role_tests.json and generates a comprehensive PDF report
with all test results organized by role.
"""

import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


class PDFReportGenerator:
    """Generate comprehensive PDF reports from test results."""
    
    # Permission test descriptions
    PERMISSION_DESCRIPTIONS = {
        "Clarity Login": "Tests ability to authenticate and access the Clarity LIMS web interface. Verifies successful login and dashboard loading.",
        "Api Login": "Tests ability to authenticate and connect to the Clarity LIMS API programmatically using s4 library credentials.",
        "Create Project": "Tests permission to create new projects in Clarity LIMS. Verifies the NEW PROJECT button is accessible and project creation completes successfully.",
        "Delete Project": "Tests permission to delete existing projects. Verifies the delete button is available and project deletion can be executed.",
        "Create Sample": "Tests permission to create new samples within projects. Verifies sample creation workflow and required fields.",
        "Delete Sample": "Tests permission to delete samples from the system. Verifies delete functionality and proper cleanup.",
        "Update Sample": "Tests permission to modify existing sample information. Verifies edit capabilities for sample metadata and properties.",
        "Sample Workflow Assignment": "Tests permission to assign samples to workflows. Verifies the workflow assignment interface and successful sample routing.",
        "Move To Next Step": "Tests permission to progress samples through workflow steps. Verifies step completion and transition capabilities.",
        "Remove Sample From Workflow": "Tests permission to remove samples from assigned workflows. Verifies removal process and workflow cleanup.",
        "Sample Rework": "Tests permission to send samples back for rework. Verifies rework functionality and sample status updates.",
        "Review Escalated Samples": "Tests permission to review and handle escalated samples. Verifies access to escalation queues and resolution capabilities.",
        "Requeue Sample": "Tests permission to requeue samples in the workflow system. Verifies requeue functionality and proper queue management.",
        "Edit Completed Steps": "Tests permission to edit steps that have been marked as completed. Verifies edit confirmation dialogs and modification capabilities.",
        "Overview Dashboard": "Tests access to the Overview Dashboard. Verifies dashboard loading and display of system-wide metrics.",
        "Create User": "Tests permission to create new user accounts. Verifies user creation form access and successful account creation.",
        "Read User": "Tests permission to view user information and profiles. Verifies access to user management interface and user details.",
        "Update User": "Tests permission to modify existing user accounts. Verifies edit capabilities for user properties and roles.",
        "Delete User": "Tests permission to delete user accounts from the system. Verifies delete functionality and user removal process.",
        "Create Control": "Tests permission to create quality control samples. Verifies control creation interface and successful setup.",
        "Update Control": "Tests permission to modify existing quality control samples. Verifies edit capabilities for control properties.",
        "Delete Control": "Tests permission to delete quality control samples. Verifies control deletion and proper cleanup.",
        "Create Reagent Kit": "Tests permission to create reagent kit records. Verifies kit creation workflow and required fields.",
        "Update Reagent Kit": "Tests permission to modify reagent kit information. Verifies edit capabilities for kit metadata.",
        "Delete Reagent Kit": "Tests permission to delete reagent kit records. Verifies deletion process and inventory cleanup.",
        "Create Process": "Tests permission to create new process definitions. Verifies process creation workflow and configuration options.",
        "Read Process": "Tests permission to view process information and definitions. Verifies access to process details and configurations.",
        "Update Process": "Tests permission to modify existing process definitions. Verifies edit capabilities for process configurations.",
        "Delete Process": "Tests permission to delete process definitions. Verifies deletion and impact on existing workflows.",
        "Create Role": "Tests permission to create new user roles. Verifies role creation interface and permission assignment.",
        "Update Role": "Tests permission to modify existing roles and their permissions. Verifies role edit capabilities.",
        "Delete Role": "Tests permission to delete user roles from the system. Verifies role deletion and user impact.",
        "Create Contact": "Tests permission to create contact records. Verifies contact creation form and required information.",
        "Read Contact": "Tests permission to view contact information. Verifies access to contact management interface.",
        "Update Contact": "Tests permission to modify contact records. Verifies edit capabilities for contact details.",
        "Delete Contact": "Tests permission to delete contact records. Verifies deletion process and cleanup.",
        "Update Configuration": "Tests permission to modify system configuration settings. Verifies access to configuration interface.",
        "Esignature Signing": "Tests permission to use electronic signature functionality. Verifies e-signature workflows and validation.",
        "Search Index": "Tests permission to use search functionality. Verifies search interface and result access.",
        "Administer Lab Link": "Tests permission to administer lab link integrations. Verifies lab link management capabilities.",
        "Url Check": "Tests that protected URLs redirect unauthenticated users to login. Verifies access control for all major system pages.",
        "Collaborations Login": "Tests access to the Collaborations module interface. Verifies module availability and login.",
        "Operations Login": "Tests access to the Operations module interface. Verifies module availability and functionality.",
    }
    
    def __init__(self, json_file="test_results/all_role_tests.json"):
        """
        Initialize the PDF generator.
        
        Args:
            json_file: Path to the JSON results file
        """
        self.json_file = json_file
        self.data = None
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Role heading style
        self.styles.add(ParagraphStyle(
            name='RoleHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#3498db'),
            borderWidth=0,
            borderPadding=5
        ))
        
        # Section style
        self.styles.add(ParagraphStyle(
            name='Section',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Info style
        self.styles.add(ParagraphStyle(
            name='Info',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=6
        ))
    
    def load_data(self):
        """Load test results from JSON file."""
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"JSON file not found: {self.json_file}")
        
        with open(self.json_file, 'r') as f:
            self.data = json.load(f)
        
        print(f"Loaded test results from: {self.json_file}")
        return self.data
    
    def _create_header_section(self):
        """Create the header section with metadata."""
        elements = []
        
        # Title
        title = Paragraph("Role Permission Test Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Metadata
        server = self.data.get('server', 'Unknown')
        timestamp = self.data.get('timestamp', 'Unknown')
        total_roles = len(self.data.get('tests', {}))
        
        metadata = [
            ['Server:', server],
            ['Test Date:', timestamp],
            ['Total Role Configurations:', str(total_roles)]
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_permission_reference_section(self):
        """Create Permission Test Reference section."""
        elements = []
        
        # Section title
        reference_title = Paragraph("Permission Test Reference", self.styles['RoleHeading'])
        elements.append(reference_title)
        
        # Introduction
        intro_text = "This section provides detailed descriptions of each permission test available in the testing framework. Each test validates specific functionality and access rights within Clarity LIMS."
        intro = Paragraph(intro_text, self.styles['Info'])
        elements.append(intro)
        elements.append(Spacer(1, 0.15*inch))
        
        # Organize permissions by category
        categories = {
            "Authentication & Access": [
                "Clarity Login", "Api Login", "Collaborations Login", "Operations Login", "Url Check"
            ],
            "Project Management": [
                "Create Project", "Delete Project"
            ],
            "Sample Management": [
                "Create Sample", "Delete Sample", "Update Sample", "Sample Workflow Assignment",
                "Move To Next Step", "Remove Sample From Workflow", "Sample Rework",
                "Review Escalated Samples", "Requeue Sample"
            ],
            "Workflow Operations": [
                "Edit Completed Steps", "Overview Dashboard"
            ],
            "User Management": [
                "Create User", "Read User", "Update User", "Delete User"
            ],
            "Quality Control": [
                "Create Control", "Update Control", "Delete Control"
            ],
            "Reagent Management": [
                "Create Reagent Kit", "Update Reagent Kit", "Delete Reagent Kit"
            ],
            "Process Management": [
                "Create Process", "Read Process", "Update Process", "Delete Process"
            ],
            "Role Management": [
                "Create Role", "Update Role", "Delete Role"
            ],
            "Contact Management": [
                "Create Contact", "Read Contact", "Update Contact", "Delete Contact"
            ],
            "System Administration": [
                "Update Configuration", "Esignature Signing", "Search Index", "Administer Lab Link"
            ]
        }
        
        # Create a table for each category
        for category, tests in categories.items():
            # Category heading
            category_heading = Paragraph(f"<b>{category}</b>", self.styles['Section'])
            elements.append(category_heading)
            
            # Build table data for this category
            table_data = []
            for test in tests:
                if test in self.PERMISSION_DESCRIPTIONS:
                    desc = self.PERMISSION_DESCRIPTIONS[test]
                    # Create a two-column table: Test Name | Description
                    test_cell = Paragraph(f"<b>{test}</b>", self.styles['Normal'])
                    desc_cell = Paragraph(desc, self.styles['Normal'])
                    table_data.append([test_cell, desc_cell])
            
            if table_data:
                # Create table
                perm_table = Table(table_data, colWidths=[1.8*inch, 4.6*inch])
                perm_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ]))
                elements.append(perm_table)
                elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def _create_summary_section(self):
        """Create summary statistics section."""
        elements = []
        
        # Summary title
        summary_title = Paragraph("Summary Statistics", self.styles['RoleHeading'])
        elements.append(summary_title)
        
        tests = self.data.get('tests', {})
        
        # Calculate statistics
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_errors = 0
        total_execution_time = 0
        
        for role_name, role_tests in tests.items():
            for test in role_tests:
                total_tests += 1
                total_execution_time += test.get('execution_time', 0)
                result = test.get('result', 'unknown')
                if result == 'pass':
                    total_passed += 1
                elif result == 'fail':
                    total_failed += 1
                elif result == 'error':
                    total_errors += 1
        
        avg_execution_time = total_execution_time / total_tests if total_tests > 0 else 0
        
        # Create summary table
        summary_data = [
            ['Metric', 'Count'],
            ['Role Configurations Tested', str(len(tests))],
            ['Total Test Executions', str(total_tests)],
            ['Tests Passed (as expected)', str(total_passed)],
            ['Tests Failed (unexpected)', str(total_failed)],
            ['Errors Encountered', str(total_errors)],
            ['Total Execution Time', f'{total_execution_time:.1f}s'],
            ['Average Time per Test', f'{avg_execution_time:.1f}s'],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_role_section(self, role_name, role_tests):
        """Create a section for a specific role with all its tests."""
        elements = []
        
        # Role heading
        role_heading = Paragraph(f"Role: {role_name}", self.styles['RoleHeading'])
        elements.append(role_heading)
        
        # Role statistics
        total = len(role_tests)
        passed = sum(1 for t in role_tests if t.get('result') == 'pass')
        failed = sum(1 for t in role_tests if t.get('result') == 'fail')
        errors = sum(1 for t in role_tests if t.get('result') == 'error')
        
        # Execution time statistics
        total_time = sum(t.get('execution_time', 0) for t in role_tests)
        avg_time = total_time / total if total > 0 else 0
        
        stats_text = f"<b>Tests:</b> {total} | <b>Passed:</b> {passed} | <b>Failed:</b> {failed} | <b>Errors:</b> {errors}"
        stats_para = Paragraph(stats_text, self.styles['Info'])
        elements.append(stats_para)
        
        time_text = f"<b>Total Execution Time:</b> {total_time:.1f}s | <b>Average:</b> {avg_time:.1f}s per test"
        time_para = Paragraph(time_text, self.styles['Info'])
        elements.append(time_para)
        
        elements.append(Spacer(1, 0.15*inch))
        
        # Create test results table with screenshots
        table_data = [['Test Name', 'Expected', 'Result', 'Time (s)', 'Status', 'Screenshot']]
        
        for test in role_tests:
            test_name = test.get('test_name', 'Unknown')
            expected = '✓' if test.get('expected') else '✗'
            passed = '✓' if test.get('passed') else '✗'
            exec_time = f"{test.get('execution_time', 0):.1f}s"
            result = test.get('result', 'unknown').upper()
            screenshot = test.get('screenshot', None)
            
            # Color code the result
            if result == 'PASS':
                result_cell = Paragraph(f'<font color="green"><b>{result}</b></font>', self.styles['Normal'])
            elif result == 'FAIL':
                result_cell = Paragraph(f'<font color="red"><b>{result}</b></font>', self.styles['Normal'])
            else:
                result_cell = Paragraph(f'<font color="orange"><b>{result}</b></font>', self.styles['Normal'])
            
            # Format screenshot info
            if screenshot:
                # Extract just the filename
                screenshot_name = screenshot.split('/')[-1] if '/' in screenshot else screenshot
                screenshot_cell = Paragraph(f'<font size="8">{screenshot_name}</font>', self.styles['Normal'])
            else:
                screenshot_cell = Paragraph('<font size="8" color="gray">None</font>', self.styles['Normal'])
            
            table_data.append([
                test_name,
                expected,
                passed,
                exec_time,
                result_cell,
                screenshot_cell
            ])
        
        # Create table with wider columns for better spacing
        col_widths = [2.5*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.7*inch, 1.3*inch]
        test_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Style the table
        test_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            
            # Grid and backgrounds
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            
            # Padding - more padding for header
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),  # Extra padding for header
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Extra padding for header
            ('TOPPADDING', (0, 1), (-1, -1), 7),  # Regular padding for data rows
            ('BOTTOMPADDING', (0, 1), (-1, -1), 7),  # Regular padding for data rows
            
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(test_table)
        
        # Add error summary if there are any errors
        errors_found = [t for t in role_tests if t.get('error')]
        if errors_found:
            elements.append(Spacer(1, 0.15*inch))
            error_section = Paragraph("<b>Errors:</b>", self.styles['Section'])
            elements.append(error_section)
            
            for test in errors_found:
                error_text = f"<b>• {test.get('test_name')}:</b> <font color='red'>{test.get('error', 'Unknown error')}</font>"
                error_para = Paragraph(error_text, self.styles['Info'])
                elements.append(error_para)
                elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def generate_pdf(self, output_file=None):
        """
        Generate the PDF report.
        
        Args:
            output_file: Output PDF filename (default: auto-generated)
        
        Returns:
            str: Path to generated PDF file
        """
        # Load data if not already loaded
        if not self.data:
            self.load_data()
        
        # Generate output filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_results/role_test_report_{timestamp}.pdf"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.5*inch
        )
        
        # Build document content
        elements = []
        
        # Header section
        elements.extend(self._create_header_section())
        
        # Permission Test Reference section
        elements.extend(self._create_permission_reference_section())
        
        # Add page break before summary
        elements.append(PageBreak())
        
        # Summary section
        elements.extend(self._create_summary_section())
        
        # Add page break before detailed results
        elements.append(PageBreak())
        
        # Detailed results title
        details_title = Paragraph("Detailed Test Results by Role", self.styles['RoleHeading'])
        elements.append(details_title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add section for each role
        tests = self.data.get('tests', {})
        for idx, (role_name, role_tests) in enumerate(sorted(tests.items())):
            elements.extend(self._create_role_section(role_name, role_tests))
            
            # Add page break between roles (except last one)
            if idx < len(tests) - 1:
                elements.append(PageBreak())
        
        # Build PDF
        print(f"\nGenerating PDF report: {output_file}")
        doc.build(elements)
        print(f"✓ PDF report generated successfully!")
        print(f"  Location: {output_file}")
        
        return output_file


def main():
    """Main entry point for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate PDF report from role test results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_pdf_report.py
  python generate_pdf_report.py --input custom_results.json
  python generate_pdf_report.py --output my_report.pdf
  python generate_pdf_report.py -i results.json -o report.pdf

This script reads the JSON test results and generates a comprehensive
PDF report with:
  - Server and timestamp information
  - Summary statistics
  - Detailed results for each role
  - Color-coded pass/fail indicators
  - Error details
"""
    )
    
    parser.add_argument(
        '-i', '--input',
        default='test_results/all_role_tests.json',
        help='Input JSON file (default: test_results/all_role_tests.json)'
    )
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Output PDF file (default: auto-generated with timestamp)'
    )
    
    args = parser.parse_args()
    
    # Generate report
    try:
        generator = PDFReportGenerator(args.input)
        pdf_file = generator.generate_pdf(args.output)
        print(f"\n{'='*60}")
        print("PDF REPORT GENERATION COMPLETE")
        print(f"{'='*60}")
        print(f"Report saved to: {pdf_file}")
        print(f"{'='*60}\n")
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Make sure you have run tests first to generate the JSON file.")
    except Exception as e:
        print(f"\nError generating PDF: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

