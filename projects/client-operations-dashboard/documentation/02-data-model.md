
# Data Model

## Project Information

| Item       | Value                                        |
| ---------- | -------------------------------------------- |
| Project    | Client Prioritization & Operations Dashboard |
| Version    | 0.1                                          |
| Status     | Planning                                     |
| Author     | Brett Coulter                                |
| Model Type | Relational Operational Data Model            |

---

## Overview

The Client Prioritization & Operations Dashboard uses four related datasets to represent clients, staff members, programs, and client interactions.

The model separates descriptive information from transactional activity so that client engagement, staff workloads, program participation, and follow-up needs can be analyzed without duplicating data unnecessarily.

The initial version will be implemented using Microsoft Excel and Power Query. The same model can later support a Power BI dashboard or SQL-based solution.

---

## Data Model Summary

| Dataset  | Purpose                               |                     Expected Size |
| -------- | ------------------------------------- | --------------------------------: |
| Clients  | Stores one record per client          |                        1,000 rows |
| Staff    | Stores one record per staff member    |                           18 rows |
| Programs | Stores one record per program         |                            6 rows |
| Contacts | Stores individual client interactions | Approximately 10,000–15,000 rows |

---

# Dataset 1: Clients

Each row represents one client.

| Field           | Data Type    | Required | Description                                      |
| --------------- | ------------ | -------: | ------------------------------------------------ |
| ClientID        | Whole Number |      Yes | Unique identifier assigned to each client        |
| FirstName       | Text         |      Yes | Fictional client first name                      |
| LastName        | Text         |      Yes | Fictional client last name                       |
| DateOfBirth     | Date         |      Yes | Client date of birth                             |
| EnrollmentDate  | Date         |      Yes | Date the client entered the organization         |
| ProgramID       | Whole Number |      Yes | Identifier for the client’s assigned program    |
| AssignedStaffID | Whole Number |      Yes | Identifier for the primary assigned staff member |
| ClientStatus    | Text         |      Yes | Current client status                            |
| BaseRiskLevel   | Text         |      Yes | Initial assessed risk level                      |
| ExitDate        | Date         |       No | Date services ended, when applicable             |
| ExitReason      | Text         |       No | Reason the client exited the program             |

## Allowed Client Status Values

- Active
- Pending
- Inactive
- Closed

## Allowed Base Risk Levels

- Low
- Medium
- High

---

# Dataset 2: Staff

Each row represents one staff member.

| Field            | Data Type    | Required | Description                                     |
| ---------------- | ------------ | -------: | ----------------------------------------------- |
| StaffID          | Whole Number |      Yes | Unique identifier assigned to each staff member |
| StaffName        | Text         |      Yes | Fictional employee name                         |
| JobTitle         | Text         |      Yes | Employee role                                   |
| ProgramID        | Whole Number |      Yes | Primary program assignment                      |
| SupervisorID     | Whole Number |       No | Identifier for the employee’s supervisor       |
| EmploymentStatus | Text         |      Yes | Current employment status                       |
| CapacityTarget   | Whole Number |      Yes | Recommended maximum active caseload             |

## Allowed Job Titles

- Case Manager
- Senior Case Manager
- Program Coordinator
- Program Manager
- Operations Specialist

## Allowed Employment Status Values

- Active
- Leave
- Inactive

---

# Dataset 3: Programs

Each row represents one service program.

| Field                 | Data Type    | Required | Description                                   |
| --------------------- | ------------ | -------: | --------------------------------------------- |
| ProgramID             | Whole Number |      Yes | Unique identifier assigned to each program    |
| ProgramName           | Text         |      Yes | Name of the program                           |
| ProgramCategory       | Text         |      Yes | General type of service provided              |
| ProgramManagerID      | Whole Number |      Yes | Staff identifier for the responsible manager  |
| ContactTargetDays     | Whole Number |      Yes | Expected maximum days between client contacts |
| InactiveThresholdDays | Whole Number |      Yes | Days without contact before inactivity review |
| ProgramStatus         | Text         |      Yes | Indicates whether the program is operating    |

## Planned Programs

1. Community Support
2. Housing Navigation
3. Employment Services
4. Behavioral Health Coordination
5. Family Stabilization
6. Transition Services

## Allowed Program Status Values

- Active
- Paused
- Closed

---

# Dataset 4: Contacts

Each row represents one documented interaction or attempted interaction with a client.

| Field                  | Data Type    | Required | Description                                           |
| ---------------------- | ------------ | -------: | ----------------------------------------------------- |
| ContactID              | Whole Number |      Yes | Unique identifier assigned to each contact record     |
| ClientID               | Whole Number |      Yes | Identifier for the associated client                  |
| StaffID                | Whole Number |      Yes | Identifier for the staff member recording the contact |
| ContactDate            | Date         |      Yes | Date of the interaction or attempt                    |
| ContactType            | Text         |      Yes | Method used to contact the client                     |
| ContactOutcome         | Text         |      Yes | Result of the interaction                             |
| ContactDurationMinutes | Whole Number |       No | Duration of successful interactions                   |
| FollowUpDate           | Date         |       No | Planned date for the next action                      |
| ContactNotesCategory   | Text         |       No | General category describing the interaction           |

## Allowed Contact Types

- Phone
- Email
- In Person
- Video
- Text Message
- Outreach Attempt

## Allowed Contact Outcomes

- Successful
- No Answer
- Voicemail
- Rescheduled
- Client Declined
- Unable to Locate

## Allowed Contact Notes Categories

- General Check-In
- Documentation
- Service Planning
- Referral
- Crisis Support
- Follow-Up
- Program Update

---

# Table Relationships

| Primary Dataset | Related Dataset | Relationship                                  |
| --------------- | --------------- | --------------------------------------------- |
| Programs        | Clients         | One program can serve many clients            |
| Programs        | Staff           | One program can include many staff members    |
| Staff           | Clients         | One staff member can be assigned many clients |
| Clients         | Contacts        | One client can have many contact records      |
| Staff           | Contacts        | One staff member can record many contacts     |

## Relationship Diagram

```text
Programs
   │
   ├────< Staff
   │        │
   │        ├────< Clients
   │        │        │
   │        │        └────< Contacts
   │        │
   │        └─────────────< Contacts
   │
   └────< Clients
```

---

# Calculated Reporting Fields

The following fields will be created through Excel formulas, Power Query, or the Power BI data model rather than stored directly in the source data.

| Calculated Field       | Source                                 | Logic                                                  |
| ---------------------- | -------------------------------------- | ------------------------------------------------------ |
| LatestContactDate      | Contacts                               | Most recent successful contact for each client         |
| DaysSinceContact       | LatestContactDate                      | Current date minus latest successful contact date      |
| ContactCount           | Contacts                               | Number of contact records associated with each client  |
| SuccessfulContactCount | Contacts                               | Number of contacts with a successful outcome           |
| FollowUpRequired       | Clients and Contacts                   | Determined by contact timing and business rules        |
| OperationalPriority    | Clients and Contacts                   | Calculated using risk, status, and engagement history  |
| InactivityStatus       | Clients and Programs                   | Compares days since contact with the program threshold |
| StaffActiveCaseload    | Clients and Staff                      | Count of active clients assigned to each staff member  |
| CapacityUtilization    | StaffActiveCaseload and CapacityTarget | Active caseload divided by capacity target             |

---

# Dashboard Metrics

The model will support the following primary metrics:

- Total clients
- Active clients
- Pending clients
- Clients requiring follow-up
- Clients approaching inactivity
- Inactive clients
- High-priority clients
- Average days since successful contact
- Successful contact rate
- Clients by program
- Clients by assigned staff member
- Staff caseload utilization
- Contacts by method
- Contacts by outcome
- Monthly client engagement trends

---

# Data Quality Requirements

The system should validate that:

- Every ClientID is unique in the Clients dataset.
- Every StaffID is unique in the Staff dataset.
- Every ProgramID is unique in the Programs dataset.
- Every ContactID is unique in the Contacts dataset.
- All ProgramID values in Clients and Staff exist in Programs.
- All AssignedStaffID values in Clients exist in Staff.
- All ClientID values in Contacts exist in Clients.
- All StaffID values in Contacts exist in Staff.
- Enrollment dates are not in the future.
- Contact dates are not in the future.
- Exit dates do not occur before enrollment dates.
- Contact durations are not negative.
- Required fields are not blank.
- Duplicate contact records are identified for review.

---

# Data Privacy

All names, identifiers, dates, programs, and interaction records used in this portfolio project will be fictional and generated specifically for demonstration purposes.

No client-level information, employer-owned files, confidential business rules, or protected data from current or former employers will be included.

---

# Future Model Enhancements

Future versions may add:

- Multiple program enrollments per client
- Separate enrollment history
- Referrals and referral outcomes
- Service plans and goals
- Client assessments
- Detailed case notes
- Program outcomes
- Geographic information
- Staff performance targets
- Historical status tracking
