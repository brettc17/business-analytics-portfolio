
# Business Rules

## Project Information

| Item    | Value                                        |
| ------- | -------------------------------------------- |
| Project | Client Prioritization & Operations Dashboard |
| Version | 0.1                                          |
| Status  | Planning                                     |
| Author  | Brett Coulter                                |

---

# Overview

Business rules determine how the system evaluates client activity, prioritizes follow-up, identifies inactive clients, and calculates operational metrics.

These rules are configurable and designed to support operational decision-making while minimizing manual review.

---

# Rule 1 - Client Status

A client shall be considered **Active** if:

- Exit Date is blank
- Client Status = Active

Otherwise the client shall be excluded from active workload calculations.

---

# Rule 2 - Latest Contact

The system shall identify the most recent successful contact for every client.

Only contacts with an outcome of:

- Successful

shall be considered when calculating engagement.

---

# Rule 3 - Days Since Contact

Days Since Contact shall equal:

Today's Date - Latest Successful Contact Date

---

# Rule 4 - Follow-Up Required

A client requires follow-up when:

- Days Since Contact exceeds the Program Contact Target

OR

- A future Follow-Up Date is due

---

# Rule 5 - Approaching Inactivity

A client is approaching inactivity when:

Days Since Contact >= 75% of the Program Inactivity Threshold

Example:

Program threshold = 60 days

Approaching inactivity begins at 45 days.

---

# Rule 6 - Inactive Client

A client is considered inactive when:

Days Since Contact exceeds the Program Inactivity Threshold.

Inactive clients automatically appear in the Inactive Queue.

---

# Rule 7 - High Priority

A client becomes High Priority when ANY of the following occur:

- Base Risk = High
- Follow-Up Required = Yes
- Approaching Inactivity = Yes

---

# Rule 8 - Staff Caseload

Active Caseload equals:

Count of Active Clients assigned to each staff member.

Inactive and Closed clients are excluded.

---

# Rule 9 - Capacity Utilization

Capacity Utilization =

Active Caseload ÷ Capacity Target

---

# Rule 10 - Dashboard Refresh

All dashboard metrics shall automatically update after the source data is refreshed.

No manual recalculation should be required.

---

# Rule 11 - Data Validation

The system shall identify:

- Duplicate Client IDs
- Duplicate Contact IDs
- Missing required fields
- Invalid dates
- Missing staff assignments

Records failing validation should be flagged for review.

---

# Rule 12 - Dashboard KPIs

The dashboard shall display:

- Active Clients
- Clients Requiring Follow-Up
- High Priority Clients
- Inactive Clients
- Average Days Since Contact
- Staff Caseload
- Capacity Utilization
- Contacts This Month
