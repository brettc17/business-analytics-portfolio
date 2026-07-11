import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Produces the same fictional dataset every time.
random.seed(42)

CLIENT_COUNT = 250
TODAY = date.today()

FIRST_NAMES = [
    "Aaliyah", "Aaron", "Adrian", "Aisha", "Alex", "Amara", "Andre",
    "Angela", "Anthony", "Ariana", "Benjamin", "Brandon", "Brianna",
    "Caleb", "Camila", "Carlos", "Carmen", "Chloe", "Christopher",
    "Daniel", "David", "Dominique", "Elena", "Elijah", "Emily", "Emma",
    "Ethan", "Gabriel", "Grace", "Hannah", "Isaac", "Isabella", "Jamal",
    "Jasmine", "Jordan", "Jose", "Kayla", "Kevin", "Lauren", "Leah",
    "Lucas", "Luis", "Marcus", "Maria", "Maya", "Michael", "Natalie",
    "Nathan", "Noah", "Olivia", "Omar", "Priya", "Rachel", "Samuel",
    "Sofia", "Taylor", "Victoria", "William", "Xavier", "Zoe"
]

LAST_NAMES = [
    "Adams", "Allen", "Anderson", "Bailey", "Bennett", "Brooks",
    "Brown", "Campbell", "Carter", "Clark", "Collins", "Cooper",
    "Davis", "Edwards", "Evans", "Foster", "Garcia", "Gonzalez",
    "Green", "Hall", "Harris", "Hernandez", "Hill", "Jackson", "Johnson",
    "Kim", "Lee", "Lewis", "Martin", "Martinez", "Miller", "Mitchell",
    "Moore", "Morgan", "Nelson", "Nguyen", "Patel", "Perez", "Price",
    "Ramirez", "Reed", "Rivera", "Robinson", "Rodriguez", "Scott",
    "Shah", "Smith", "Taylor", "Thomas", "Thompson", "Turner",
    "Walker", "White", "Williams", "Wilson", "Wright", "Young"
]

# Staff members are mapped to their assigned programs.
STAFF_BY_PROGRAM = {
    1001: [2002, 2003],
    1002: [2005, 2006],
    1003: [2007, 2008, 2009],
    1004: [2011, 2012],
    1005: [2013, 2014, 2015],
    1006: [2017, 2018],
}

PROGRAM_IDS = list(STAFF_BY_PROGRAM.keys())

STATUS_OPTIONS = ["Active", "Pending", "Inactive", "Closed"]
STATUS_WEIGHTS = [0.68, 0.10, 0.10, 0.12]

RISK_OPTIONS = ["Low", "Medium", "High"]
RISK_WEIGHTS = [0.45, 0.35, 0.20]

EXIT_REASONS = [
    "Completed Program",
    "Transferred to Another Program",
    "Client Withdrew",
    "Unable to Contact",
    "No Longer Eligible",
    "Relocated",
]


def random_date(start: date, end: date) -> date:
    """Return a random date between start and end, inclusive."""
    day_range = (end - start).days
    return start + timedelta(days=random.randint(0, day_range))


def create_client(client_number: int) -> dict:
    program_id = random.choice(PROGRAM_IDS)
    staff_id = random.choice(STAFF_BY_PROGRAM[program_id])

    status = random.choices(
        STATUS_OPTIONS,
        weights=STATUS_WEIGHTS,
        k=1,
    )[0]

    risk_level = random.choices(
        RISK_OPTIONS,
        weights=RISK_WEIGHTS,
        k=1,
    )[0]

    date_of_birth = random_date(
        TODAY - timedelta(days=75 * 365),
        TODAY - timedelta(days=18 * 365),
    )

    enrollment_date = random_date(
        TODAY - timedelta(days=3 * 365),
        TODAY - timedelta(days=14),
    )

    exit_date = ""
    exit_reason = ""

    if status in {"Inactive", "Closed"}:
        earliest_exit = enrollment_date + timedelta(days=7)

        if earliest_exit <= TODAY:
            exit_date_value = random_date(earliest_exit, TODAY)
            exit_date = exit_date_value.isoformat()
            exit_reason = random.choice(EXIT_REASONS)

    return {
        "ClientID": 3000 + client_number,
        "FirstName": random.choice(FIRST_NAMES),
        "LastName": random.choice(LAST_NAMES),
        "DateOfBirth": date_of_birth.isoformat(),
        "EnrollmentDate": enrollment_date.isoformat(),
        "ProgramID": program_id,
        "AssignedStaffID": staff_id,
        "ClientStatus": status,
        "BaseRiskLevel": risk_level,
        "ExitDate": exit_date,
        "ExitReason": exit_reason,
    }


def main() -> None:
    project_folder = Path(__file__).resolve().parent.parent
    output_file = project_folder / "sample-data" / "client_data.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    clients = [
        create_client(client_number)
        for client_number in range(1, CLIENT_COUNT + 1)
    ]

    fieldnames = [
        "ClientID",
        "FirstName",
        "LastName",
        "DateOfBirth",
        "EnrollmentDate",
        "ProgramID",
        "AssignedStaffID",
        "ClientStatus",
        "BaseRiskLevel",
        "ExitDate",
        "ExitReason",
    ]

    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clients)

    print(f"Created {len(clients)} fictional clients.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()