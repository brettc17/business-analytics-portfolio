
# Design Decisions

## Overview

This document explains the main technical and operational decisions made while developing the Client Prioritization & Operations Dashboard.

## Use of Fictional Data

All client, staff, program, and contact records were generated specifically for this portfolio project.

Python was used to create realistic but fictional data because:

- Real client information cannot be used in a public portfolio
- Synthetic data allows the project to demonstrate realistic operational scenarios
- The dataset can be regenerated and expanded
- Data-quality and business-rule logic can be tested safely

## Separate Client and Contact Tables

Client information and contact history are stored as separate datasets.

This reflects a one-to-many relationship:

```text
One Client → Many Contact Records
```

Separating the tables avoids repeating client information for every interaction and more closely reflects a relational data model.

## Central Client Summary Model

A single Power Query reporting model, `qryClientSummary`, was created with one row per client.

The model combines:

- Client information
- Program thresholds
- Contact-history summaries
- Staff assignments
- Operational business rules

Downstream queues and dashboard calculations reference this model instead of recreating transformation logic.

This reduces duplication and makes the workbook easier to maintain.

## Power Query References Instead of Duplicates

Downstream queries were created using **Reference** rather than **Duplicate**.

Examples include:

- `qryPriorityQueue`
- `qryInactiveQueue`
- `qryClientDataQuality`

Using references ensures that each output remains connected to the central client-summary model and inherits upstream changes.

## Program-Specific Thresholds

Follow-up and inactivity thresholds are stored in the Programs table rather than hard-coded into each calculation.

This allows different programs to use different operational expectations and makes future changes easier to manage.

For example, one program may require contact every 14 days while another may allow 30 days.

## Successful Contacts as the Primary Activity Measure

Days since contact are based on the most recent contact with a `Successful` outcome.

This decision prevents unsuccessful attempts from resetting the client’s activity clock and better reflects meaningful engagement.

Clients without a successful contact use their enrollment date as the fallback reference date.

## Operational Priority Classification

Priority is calculated using multiple indicators rather than relying only on the client’s base risk level.

The classification considers:

- Client status
- Days since successful contact
- Follow-up requirements
- Approaching inactivity
- Inactivity-review requirements
- Base risk level

The resulting categories are:

- **Critical:** Requires an inactivity review
- **High:** High-risk and overdue, or approaching inactivity
- **Medium:** Routine follow-up is overdue
- **Low:** No immediate operational action is required
- **Closed:** Client is no longer part of the active workload

This approach prioritizes actionable workload rather than displaying risk in isolation.

## Read-Only Operational Queues

The Priority Queue and Inactive Queue are generated through Power Query rather than worksheet formulas.

This design:

- Reduces the risk of formulas being overwritten
- Creates consistent outputs after refresh
- Keeps business logic in the transformation layer
- Makes the queue worksheets easier for end users to navigate

## Separate Metrics Layer

Dashboard calculations are maintained on a dedicated Metrics worksheet.

The dashboard references those calculated values rather than containing complex formulas inside shapes or charts.

This separates:

```text
Reporting Logic → Dashboard Presentation
```

and makes KPI calculations easier to inspect and troubleshoot.

## Staff Capacity Comparison

The staff-capacity visual compares open Active and Pending clients with each employee’s capacity target.

Staff members with a capacity target of zero are excluded because their roles are not intended to carry a client caseload.

## Data-Quality Controls

Data-quality checks are separated into two categories.

### Row-Level Checks

These evaluate individual client records for issues such as:

- Missing assignments
- Invalid dates
- Inconsistent status and exit information
- Missing contact history

### Cross-Table Checks

These compare full datasets to identify:

- Duplicate Client IDs
- Invalid staff references
- Invalid program references

Separating these checks improves clarity and allows each control to use the most appropriate validation method.

## Connection-Only Validation Queries

Validation queries that return zero rows are stored as connection-only queries rather than loaded as empty worksheet tables.

Their results are summarized in `qryDataQualitySummary`, allowing users to see whether each control passed without cluttering the workbook.

## Excel as the User Interface

Excel was selected as the presentation layer because it supports:

- Familiar navigation for operational users
- Power Query refreshes
- Filterable tables
- Conditional formatting
- Dashboard charts
- Portable distribution

The workbook is designed to function as an operational reporting tool rather than only as a static visualization.

## Version Control

Git and GitHub are used to track:

- Python scripts
- Documentation
- Sample data
- Workbook development
- Project screenshots

This provides a visible development history and supports reproducibility.

## Maintainability Principle

The project follows a layered design:

```text
Source Data
    ↓
Power Query Transformations
    ↓
Client Summary Reporting Model
    ↓
Metrics and Exception Queries
    ↓
Dashboard and Operational Queues
```

Each layer has a distinct responsibility, reducing duplicated logic and making future modifications easier.
