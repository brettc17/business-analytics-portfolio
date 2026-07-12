
# System Architecture

## Overview

The Client Prioritization & Operations Dashboard uses a layered reporting architecture that separates source-data generation, transformation logic, reporting logic, exception handling, and presentation.

The design is intended to make the workbook easier to maintain, refresh, audit, and explain.

## Architecture Flow

```text
Python Data Generation
        ↓
Fictional CSV Source Files
        ↓
Excel Source Tables
        ↓
Power Query Transformation Layer
        ↓
Client Summary Reporting Model
        ↓
Metrics, Operational Queues, and Data-Quality Controls
        ↓
Excel Dashboard and User Interface
```

## Architecture Principles

The solution follows several core principles:

- Separate source data from reporting outputs
- Centralize reusable transformation logic
- Avoid duplicating calculations across worksheets
- Use reference queries for downstream outputs
- Keep the user-facing workbook simple
- Maintain a clear refresh path
- Use only fictional data suitable for public portfolio use

## Data Generation Layer

Python scripts generate the fictional datasets used by the project.

### Client Data Generation

The `generate_clients.py` script creates one row per fictional client.

The generated data includes:

- Client ID
- First name
- Last name
- Program assignment
- Staff assignment
- Enrollment date
- Client status
- Exit date
- Exit destination
- Base risk level
- Additional operational fields

### Contact Data Generation

The `generate_contacts.py` script creates multiple contact records for each client.

The generated data includes:

- Contact ID
- Client ID
- Contact date
- Contact type
- Contact outcome
- Follow-up date
- Contact notes
- Additional interaction fields

The contact dataset creates a one-to-many relationship between clients and contact records.

```text
One Client → Many Contact Records
```

### Purpose of the Data Generation Layer

Python-generated data was used because:

- Real client information cannot be included in a public portfolio
- Synthetic data allows realistic operational scenarios to be modeled
- The dataset can be regenerated and expanded
- Business rules can be tested safely
- Data-quality controls can be demonstrated without exposing protected information

## Source Data Layer

The workbook contains four primary source tables.

### Clients

The Clients table contains one row per fictional client.

Primary key:

```text
ClientID
```

The table includes:

- Client identity fields
- Program assignment
- Staff assignment
- Enrollment information
- Current status
- Exit information
- Base risk level

### Contacts

The Contacts table contains multiple records per client.

Primary key:

```text
ContactID
```

Foreign key:

```text
ClientID
```

The table includes:

- Contact date
- Contact type
- Contact outcome
- Follow-up date
- Contact notes

### Staff

The Staff table contains staff assignment and capacity information.

Primary key:

```text
StaffID
```

The table includes:

- Staff name
- Job title
- Program assignment
- Capacity target
- Employment status

### Programs

The Programs table contains program-level operational thresholds.

Primary key:

```text
ProgramID
```

The table includes:

- Program name
- Contact target
- Inactivity threshold
- Program status

## Data Relationships

The primary relationships are:

```text
Programs[ProgramID]
        ↓
Clients[ProgramID]

Staff[StaffID]
        ↓
Clients[AssignedStaffID]

Clients[ClientID]
        ↓
Contacts[ClientID]
```

These relationships support the aggregation of contact history and the application of staff- and program-specific logic.

## Power Query Transformation Layer

Power Query performs the primary extract, transform, and load workflow.

The transformation layer is responsible for:

- Importing source data
- Applying data types
- Filtering invalid or unnecessary records
- Grouping contact records by client
- Calculating latest successful contact dates
- Counting contact records
- Joining client, program, staff, and contact data
- Applying operational business rules
- Creating queue and exception outputs
- Supporting workbook refreshes

## Contact Summary Query

The contact-summary query aggregates the Contacts table to one row per client.

It calculates:

- Latest successful contact date
- Successful contact count
- Total contact count

The latest successful contact date is used as the primary measure of meaningful client engagement.

Unsuccessful contact attempts do not reset the activity clock.

## Contact Count Query

A separate contact-count query calculates the total number of contact records for each client.

This count includes all contact outcomes.

It is merged with the successful-contact summary so the reporting model can display both:

- Total contact volume
- Successful contact activity

## Client Summary Reporting Model

`qryClientSummary` serves as the central reporting model.

It contains one row per client and combines:

- Client information
- Staff assignments
- Program assignments
- Program-specific thresholds
- Contact-history summaries
- Operational business-rule outputs

This query acts as the primary semantic layer for the workbook.

Downstream queries reference `qryClientSummary` rather than rebuilding the same transformations.

## Calculated Operational Fields

The client-summary model calculates several reporting fields.

### Latest Successful Contact

The most recent contact record with a successful outcome.

### Successful Contact Count

The number of successful contact records associated with the client.

### Contact Count

The total number of contact records associated with the client.

### Days Since Contact

The number of days since the latest successful contact.

If no successful contact exists, the enrollment date is used as the fallback reference date.

### Follow-Up Required

Indicates whether the client has exceeded the contact target assigned to their program.

### Approaching Inactivity

Indicates whether the client is nearing the inactivity threshold but has not yet exceeded it.

The calculation uses a percentage of the program-specific inactivity threshold.

### Needs Inactivity Review

Indicates whether an Active or Pending client has exceeded the inactivity threshold.

This field does not automatically change the client’s official status.

Instead, it identifies records requiring review.

### Operational Priority

Assigns a workload category based on client status, contact history, inactivity rules, follow-up requirements, and base risk.

Priority categories include:

- Critical
- High
- Medium
- Low
- Closed

## Operational Queue Layer

Operational queues are created as reference queries from `qryClientSummary`.

This ensures that queue logic remains connected to the central reporting model.

### Priority Queue

`qryPriorityQueue` contains clients classified as:

- Critical
- High

The queue is sorted by:

1. Operational priority
2. Days since contact

The most urgent records appear first.

### Inactive Queue

`qryInactiveQueue` contains clients where:

```text
NeedsInactivityReview = Yes
```

The queue is sorted by:

1. Days since contact, descending
2. Last name, ascending

This places the longest contact gaps at the top.

## Metrics Layer

The Metrics worksheet provides a dedicated calculation layer for dashboard KPIs and chart support data.

The metrics layer includes:

- Total clients
- Active clients
- Pending clients
- Closed clients
- Critical-priority clients
- High-priority clients
- Follow-up required
- Needs inactivity review
- Average days since contact
- Total contact records
- Successful contacts
- Successful contact rate
- Active staff members
- Active programs

It also contains support tables for:

- Clients by program
- Operational-priority distribution
- Contact volume by month
- Staff caseload versus capacity

Separating metrics from the dashboard keeps calculations visible and easier to troubleshoot.

## Dashboard Layer

The Dashboard worksheet provides the primary user-facing summary.

It includes:

- KPI cards
- Active and pending clients by program
- Operational-priority distribution
- Contact volume by month
- Staff caseload versus capacity
- Navigation buttons
- Reporting date
- Workbook title and subtitle

The dashboard references the Metrics worksheet rather than embedding complex logic directly in shapes and charts.

## Staff Capacity Analysis

Staff capacity is calculated using Active and Pending clients assigned to each staff member.

The chart compares:

- Open client caseload
- Capacity target

Staff members with a capacity target of zero are excluded because their roles are not intended to carry a client caseload.

Utilization is calculated as:

```text
Open Clients ÷ Capacity Target
```

## Data-Quality Layer

The workbook includes row-level and cross-table validation controls.

### Client Record Exceptions

`qryClientDataQuality` evaluates individual client records.

Checks include:

- Missing Client ID
- Missing program assignment
- Missing staff assignment
- Missing enrollment date
- Future enrollment date
- Exit before enrollment
- Closed client without exit date
- Open client with exit date
- No contact history

Multiple issues can be combined into one exception field.

Example:

```text
Missing Staff Assignment; No Contact History
```

### Duplicate Client ID Check

`qryDuplicateClientIDs` groups client records by Client ID and counts rows.

Records with a count greater than one are flagged as duplicates.

### Invalid Staff Assignment Check

`qryInvalidStaffAssignments` uses a Left Anti join between:

```text
Clients[AssignedStaffID]
```

and:

```text
Staff[StaffID]
```

Only client records with unmatched staff assignments are returned.

### Invalid Program Assignment Check

`qryInvalidProgramAssignments` uses a Left Anti join between:

```text
Clients[ProgramID]
```

and:

```text
Programs[ProgramID]
```

Only client records with unmatched program assignments are returned.

### Data Quality Summary

`qryDataQualitySummary` consolidates the issue count from each validation query.

The summary displays:

- Data-quality check
- Issue count
- Status

Status logic:

```text
Issue Count = 0 → Pass
Issue Count > 0 → Review
```

Validation queries that return no records are stored as connection-only queries to avoid cluttering the workbook with empty tables.

## User Interface Layer

Microsoft Excel provides the presentation and interaction layer.

The workbook includes:

- Dashboard navigation
- Back-to-dashboard buttons
- Filterable tables
- Conditional formatting
- KPI cards
- Operational charts
- Instructions
- Data and privacy disclaimers
- Refresh guidance

## Workbook Navigation

Navigation buttons link the primary user-facing worksheets:

- Dashboard
- Priority Queue
- Inactive Queue
- Data Quality

The Priority Queue, Inactive Queue, and Data Quality sheets also include a Back to Dashboard button.

This makes the workbook feel like a connected reporting application rather than a collection of unrelated worksheets.

## Refresh Workflow

The workbook is refreshed using Excel’s **Refresh All** command.

The refresh workflow is:

1. Read the latest Clients, Contacts, Staff, and Programs data.
2. Apply data types and source transformations.
3. Recalculate contact summaries.
4. Merge client, contact, staff, and program data.
5. Rebuild `qryClientSummary`.
6. Reapply operational business rules.
7. Refresh the Priority Queue.
8. Refresh the Inactive Queue.
9. Recalculate data-quality controls.
10. Refresh workbook metrics and charts.

## Dependency Flow

The core query dependency structure is:

```text
Contacts
    ├── qryContactSummary
    └── qryContactCounts
            ↓
Clients + Programs + Contact Summaries
            ↓
qryClientSummary
    ├── qryPriorityQueue
    ├── qryInactiveQueue
    └── qryClientDataQuality

Clients
    ├── qryDuplicateClientIDs
    ├── qryInvalidStaffAssignments
    └── qryInvalidProgramAssignments

Validation Queries
            ↓
qryDataQualitySummary
```

## Separation of Responsibilities

The architecture separates responsibilities across layers.

```text
Python
    Generates fictional source data

Excel Source Tables
    Store operational reference and source data

Power Query
    Performs transformation and validation

Client Summary Model
    Centralizes reusable reporting logic

Metrics Layer
    Calculates KPI and chart support values

Dashboard and Queues
    Present actionable information to users
```

## Maintainability

The architecture improves maintainability by:

- Centralizing reusable logic
- Using query references
- Separating calculations from presentation
- Storing thresholds in reference tables
- Avoiding duplicate formulas
- Using structured Excel tables
- Providing documented refresh steps
- Keeping validation controls independent
- Using version control for scripts and documentation

## Privacy and Security

All data included in the project is fictional.

The architecture was designed specifically to avoid the use of:

- Real client records
- Employer data
- Protected health information
- Personally identifiable information
- Internal production files

The public repository contains only synthetic datasets, documentation, scripts, screenshots, and the portfolio workbook.

## Design Principle

The overall design follows this structure:

```text
Source Data
    ↓
Transformation Logic
    ↓
Central Reporting Model
    ↓
Metrics and Exception Outputs
    ↓
Dashboard and Operational Queues
```

Each layer has a distinct responsibility.

This reduces duplicated logic, improves auditability, supports repeatable refreshes, and makes the system easier to explain to technical and nontechnical users.
