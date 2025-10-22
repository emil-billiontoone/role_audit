# Complete Testing Flow

## Overview

When you run `python run_all_roles.py "Emil" "Test"`, here's the exact sequence:

## Initialization
```
User starts with ANY roles → Reset to ONLY Lab Operator (BTO)
```

## Testing Sequence

### MAIN ROLE 1: Lab Operator (BTO)
- **Roles Assigned**: Lab Operator (BTO)
- **Tests**: Lab Operator (BTO) (BASE)

---

- **Roles Assigned**: Lab Operator (BTO) + Sample Creation (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Operator (BTO) + Editor
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Operator (BTO) + Reagent Manufacturing (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Operator (BTO) + ReviewEscalations
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Operator (BTO) + ReWork
- **Tests**: All permissions from BOTH roles combined

**→ PROMPT: Continue to System Admin (BTO)? [Y/n]**

---

### MAIN ROLE 2: System Admin (BTO)
- **Roles Assigned**: System Admin (BTO)
- **Tests**: System Admin (BTO) (BASE)

---

- **Roles Assigned**: System Admin (BTO) + Sample Creation (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: System Admin (BTO) + Editor
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: System Admin (BTO) + Reagent Manufacturing (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: System Admin (BTO) + ReviewEscalations
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: System Admin (BTO) + ReWork
- **Tests**: All permissions from BOTH roles combined

**→ PROMPT: Continue to Lab Admin (BTO)? [Y/n]**

---

### MAIN ROLE 3: Lab Admin (BTO)
- **Roles Assigned**: Lab Admin (BTO)
- **Tests**: Lab Admin (BTO) (BASE)

---

- **Roles Assigned**: Lab Admin (BTO) + Sample Creation (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Admin (BTO) + Editor
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Admin (BTO) + Reagent Manufacturing (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Admin (BTO) + ReviewEscalations
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Lab Admin (BTO) + ReWork
- **Tests**: All permissions from BOTH roles combined

**→ PROMPT: Continue to Limited (BTO)? [Y/n]**

---

### MAIN ROLE 4: Limited (BTO)
- **Roles Assigned**: Limited (BTO)
- **Tests**: Limited (BTO) (BASE)

---

- **Roles Assigned**: Limited (BTO) + Sample Creation (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Limited (BTO) + Editor
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Limited (BTO) + Reagent Manufacturing (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Limited (BTO) + ReviewEscalations
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: Limited (BTO) + ReWork
- **Tests**: All permissions from BOTH roles combined

**→ PROMPT: Continue to BTO API? [Y/n]**

---

### MAIN ROLE 5: BTO API
- **Roles Assigned**: BTO API
- **Tests**: BTO API (BASE)

---

- **Roles Assigned**: BTO API + Sample Creation (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: BTO API + Editor
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: BTO API + Reagent Manufacturing (BTO)
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: BTO API + ReviewEscalations
- **Tests**: All permissions from BOTH roles combined

---

- **Roles Assigned**: BTO API + ReWork
- **Tests**: All permissions from BOTH roles combined

**→ DONE**

---

## Summary Statistics

- **Total MAIN Roles**: 5
- **Total ADD_ON Roles**: 5
- **Tests per MAIN Role**: 6 (1 BASE + 5 ADD_ONs)
- **Total Test Combinations**: 30
- **Prompts**: 4 (after each MAIN role except the last)

## Key Features

✅ **Always Safe**: User always has at least 1 role assigned  
✅ **Combined Testing**: Tests both MAIN + ADD_ON permissions together  
✅ **Clean State**: Each MAIN role tested with fresh ADD_ON combinations  
✅ **Interactive Control**: Can stop after each MAIN role completion  
✅ **Comprehensive Coverage**: Every MAIN role tested with every ADD_ON  

## Role Management Details

### When Testing MAIN Role BASE
- User has: `[MAIN_ROLE]`

### When Testing MAIN Role + ADD_ON
1. Add ADD_ON role → User has: `[MAIN_ROLE, ADD_ON]`
2. Run tests with combined permissions
3. Before next ADD_ON:
   - Remove previous ADD_ON
   - Add next ADD_ON

### When Moving to Next MAIN Role
1. Add new MAIN role → User has: `[OLD_MAIN, NEW_MAIN]`
2. Remove old MAIN role → User has: `[NEW_MAIN]`
3. Start testing new MAIN with its BASE configuration

## Permissions Tested

### Example: Lab Operator (BTO) BASE
- `permissions_clarity_login`
- `permissions_API_login`

### Example: Lab Operator (BTO) + Sample Creation (BTO)
- `permissions_clarity_login` (from Lab Operator)
- `permissions_API_login` (from Lab Operator)
- `permissions_create_project` (from Sample Creation)

### Example: Lab Operator (BTO) + Editor
- `permissions_clarity_login` (from Lab Operator)
- `permissions_API_login` (from Lab Operator)
- `permissions_edit_completed_steps` (from Editor)

And so on for all combinations!

