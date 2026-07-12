
# Client Prioritization & Operations Dashboard

![Client Operations Dashboard overview](./images/dashboard-overview.png)

## Project Overview

This project demonstrates the design and development of a fictional client-operations reporting system using Python, Excel, Power Query, and Git.

The solution centralizes client and contact data, applies operational business rules, prioritizes follow-up activity, monitors staff capacity, and surfaces data-quality exceptions.

All records, names, organizations, and scenarios used in this project are fictional.

## Business Problem

Operational teams often manage client information, contact histories, staff assignments, and follow-up requirements across separate files.

This makes it difficult to:

- Identify urgent cases
- Monitor client inactivity
- Understand staff workload
- Apply follow-up rules consistently
- Detect data-quality issues
- Produce reliable operational reporting

This project recreates that challenge using fully fictional data and demonstrates how a centralized reporting workflow can support faster and more consistent decision-making.

## Solution

The solution combines Python-generated sample data, Excel, and Power Query to create an automated reporting workbook that:

- Consolidates client, contact, program, and staff data
- Calculates days since the most recent successful contact
- Applies program-specific follow-up and inactivity thresholds
- Assigns operational priority levels
- Generates automated priority and inactivity queues
- Compares staff caseloads with capacity targets
- Surfaces client-level data-quality exceptions
- Tests for duplicate IDs and invalid staff or program references
- Refreshes through a repeatable Power Query workflow

## Key Features

- Executive dashboard with operational KPIs
- Critical and high-priority client queue
- Inactivity-review queue
- Monthly contact-volume trend
- Program workload comparison
- Staff caseload-versus-capacity analysis
- Client-level data-quality exception report
- Duplicate Client ID validation
- Invalid staff-assignment validation
- Invalid program-assignment validation
- Workbook navigation and user instructions
- Fully fictional data suitable for public portfolio use

## Dashboard Metrics

The dashboard includes:

- Active clients
- Critical-priority clients
- High-priority clients
- Follow-up required
- Clients needing inactivity review
- Average days since successful contact
- Active and pending clients by program
- Operational-priority distribution
- Monthly contact volume
- Staff caseload compared with capacity targets

## Technology Stack

- **Python:** Generates fictional client and contact datasets
- **Microsoft Excel:** Provides the reporting interface, metrics, queues, and charts
- **Power Query:** Handles data ingestion, transformation, merging, aggregation, and business-rule logic
- **Git and GitHub:** Support version control and portfolio publishing
- **Visual Studio Code:** Used for Python development and project documentation

## Data Model

The reporting system uses four primary datasets:

- **Clients:** One row per fictional client
- **Contacts:** Multiple interaction records per client
- **Staff:** Staff assignments and capacity targets
- **Programs:** Program-specific contact and inactivity thresholds

Power Query combines these sources into a client-summary reporting layer containing calculated operational fields.

## Business Rules

The reporting model calculates:

- Latest successful contact
- Total contact count
- Successful contact count
- Days since successful contact
- Follow-up required
- Approaching inactivity
- Needs inactivity review
- Operational priority

Operational-priority categories include:

- **Critical:** Client requires an inactivity review
- **High:** Urgent follow-up or elevated operational risk
- **Medium:** Routine follow-up required
- **Low:** No immediate action required
- **Closed:** Client is no longer active

## Data Quality Controls

The workbook includes automated checks for:

- Missing required client information
- Clients without contact history
- Duplicate Client IDs
- Invalid staff assignments
- Invalid program assignments
- Future enrollment dates
- Exit dates before enrollment dates
- Closed clients without exit dates
- Open clients with exit dates

## Refresh Process

To refresh the workbook:

1. Open the Excel workbook.
2. Select the **Data** tab.
3. Click **Refresh All**.
4. Wait for the Power Query connections to finish.
5. Review the Dashboard, Priority Queue, Inactive Queue, and Data Quality sheets.

## Repository Structure

```text
client-operations-dashboard/
├── README.md
├── documentation/
├── images/
│   └── dashboard-overview.png
├── sample-data/
│   ├── client_data.csv
│   └── contact_data.csv
├── scripts/
│   ├── generate_clients.py
│   └── generate_contacts.py
└── workbook/
    └── Client Operations Dashboard.xlsx
```
