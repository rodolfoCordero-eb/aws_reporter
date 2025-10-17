# AWS Reports – Sessions Module

The `sessions` module manages authenticated AWS sessions across multiple accounts and regions.  
It provides a unified interface to assume roles, create session objects, and reuse credentials securely — whether for a single account or an entire AWS Organization.

---

## Overview

This module abstracts all session-handling logic for the **AWS Reports** project, allowing other modules (like `resources`) to focus only on AWS service calls.

It supports:
- **Cross-account access** via `assume_role`
- **Organization-wide scanning**
- **Single-account execution**
- Configurable AWS profile and region settings

---

## Main Classes

### OrgSession

Handles access to AWS Organizations and creates sessions for each member account.

```python
from sessions import OrgSession
```
**Responsibilities**:

Uses the OrganizationAccountAccessRole (default)

Assumes the role into each target AWS account.

Returns an authenticated boto3.Session object ready for use.


### SingleSession

```python
from sessions import SingleSession
```


Supports setting custom regions and profiles.

Simplifies running reports for a single AWS account.

## File Structure
```

bash
Copy code
sessions/
├── __init__.py
├── org_session.py        # Implements OrgSession
├── single_session.py     # Implements SingleSession
```




## Notes
Ensure your IAM trust policy allows sts:AssumeRole for the defined role name.

Default role: **OrganizationAccountAccessRole**

