# AWS Reports – Resources Module

The `resources` module is responsible for discovering, validating, and exporting AWS resource data.  
It uses sessions from the [`sessions`](../sessions) module to connect to AWS services and retrieve information across multiple accounts and regions.

---

##  Overview

This module powers the main reporting logic of **AWS Reports**.  
It collects information from AWS services such as EC2, VPC, CloudTrail, and SecurityHub, and outputs structured data for post-migration or auditing purposes.

**Main capabilities:**
- Collect AWS resource data (multi-account, multi-region)
- Normalize results into consistent data structures
- Export to **JSON** 


