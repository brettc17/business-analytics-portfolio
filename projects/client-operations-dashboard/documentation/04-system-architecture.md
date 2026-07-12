
# System Architecture

## Overview

The Client Prioritization & Operations Dashboard uses a layered reporting architecture that separates source-data generation, transformation logic, operational reporting, and presentation.

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
Metrics, Queues, and Data-Quality Controls
        ↓
Excel Dashboard and User Interface
```
