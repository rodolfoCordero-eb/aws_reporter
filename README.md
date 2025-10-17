# AWS Reports

A Python-based tool for auditing and comparing AWS resources across multiple accounts and regions — primarily designed to support post-migration verification between AWS Organizations.

## Features

- Retrieves and validates resources such as:
  - **VPC Peering Connections**
  - **PrivateLinks (VPC Endpoints)** (in progress)

- Supports **multi-account** and **multi-region** scanning.
- Exports results in  **JSON**s.
- Generates reports to compare pre- and post-migration configurations.

---

## Requirements

- **Python** ≥ 3.11  
- **Poetry** ≥ 1.8  
- Valid **AWS credentials** in `~/.aws/credentials` or environment variables.

---

## Installation

```bash
git clone
cd aws_reports
poetry install
```

## Create a new Module

```
cd modules 
poetry new [module_name]
```

tests 
go to module

```
poetry run pytest
```

## Structure

```
aws_reports/
│
├── modules/
│   ├── sessions/        # Handles AWS sessions and role assumptions
│   ├── resources/       # Resource discovery logic (EC2, RDS, etc.)
│   └── utils/           # Shared helpers
│
├── src/
│   ├── __main__.py      # CLI entry point
│   └── commands/        # Command definitions per AWS service
│
├── tests/               # Unit tests
├── pyproject.toml       # Poetry configuration
└── README.md

```

## Development

Run Unit Tests
`poetry run pytest`

Code Linting
`poetry run ruff check .`

## Post-Migration Validation

This project is particularly useful after migrating AWS accounts to a new Organization.
You can re-run the reports and compare the JSON/CSV outputs to ensure:

VPC Peering connections remain functional.

PrivateLinks, VPNs, and IAM configurations are preserved.

SecurityHub and CloudTrail integrations are still active.

# Contributing

Fork the repository.

Create a new branch (feature/my-feature).

Commit your changes with clear messages.

Submit a Pull Request.