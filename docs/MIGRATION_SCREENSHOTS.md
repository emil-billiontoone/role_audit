# Screenshot Location Migration

## What Changed

Screenshots are now saved to `test_results/screenshots/` instead of `screenshots/` to keep all test outputs organized in one place.

## New Structure

```
role_audit/
└── test_results/
    ├── all_role_tests.json        ← JSON results
    ├── role_test_report_*.pdf     ← PDF reports
    └── screenshots/               ← Screenshots (NEW LOCATION)
        ├── clarity_login_*.png
        ├── api_login_*.png
        └── ...
```

## Files Updated

✅ `role_permission_tester.py` - Main test framework  
✅ `permissions/test_utils.py` - Screenshot utilities  
✅ All 11 permission test files in `permissions/` folder  
✅ `README.md` - Documentation  

## Migration Steps

If you have existing screenshots in the old `screenshots/` folder:

```bash
# Navigate to project directory
cd /Users/edeguzman/projects/code/2025/role_audit

# Create new screenshots directory (if not exists)
mkdir -p test_results/screenshots

# Move existing screenshots (optional - only if you want to keep old ones)
mv screenshots/* test_results/screenshots/ 2>/dev/null || true

# Remove old empty directory (optional)
rmdir screenshots 2>/dev/null || true
```

## What This Means

### ✅ Benefits
- **Everything in one place** - All test outputs in `test_results/`
- **Better organization** - Easy to find all test artifacts
- **Cleaner project root** - Fewer top-level folders
- **Easier cleanup** - Delete entire `test_results/` to start fresh

### ✅ No Code Changes Required
- All code automatically updated
- Future tests save to new location
- PDF generator works with new paths
- JSON file already references correct paths

### ✅ Backward Compatibility
- Old screenshots in JSON still reference their original paths
- New screenshots save to new location
- Both work fine in PDF reports

## Testing the Change

Run a quick test to verify:

```bash
# Run a single test
python run_role_tests.py "Lab Operator"

# Check that screenshots are created in new location
ls -la test_results/screenshots/

# Generate PDF to verify it works
python generate_pdf_report.py
```

## Cleanup (Optional)

After verifying everything works, you can optionally clean up:

```bash
# Remove old screenshots folder if empty
rmdir screenshots 2>/dev/null

# Or if you want to keep old screenshots, you already moved them above
```

## Summary

✅ **All done!** Next time you run tests:
- Screenshots → `test_results/screenshots/`
- JSON → `test_results/all_role_tests.json`
- PDFs → `test_results/role_test_report_*.pdf`

Everything organized in one place! 🎯

