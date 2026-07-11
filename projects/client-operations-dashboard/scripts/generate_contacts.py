import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

random.seed(84)

TODAY = date.today()
MIN_CONTACTS_PER_CLIENT = 4
MAX_CONTACTS_PER_CLIENT = 20

CONTACT_TYPES = [
    "Phone",
    "Email",
    "In Person",
    "Video",
    "Text Message",
    "Outreach Attempt",
]

CONTACT_TYPE_WEIGHTS = [0.28, 0.16, 0.20, 0.08, 0.14, 0.14]

CONTACT_OUTCOMES = [
    "Successful",
    "No Answer",
    "Voicemail",
    "Rescheduled",
    "Client Declined",
    "Unable to Locate",
]

SUCCESSFUL_OUTCOMES = ["Successful", "Rescheduled"]

CONTACT_NOTE_CATEGORIES = [
    "General Check-In",
    "Documentation",
    "Service Planning",
    "Referral",
    "Crisis Support",
    "Follow-Up",
    "Program Update",
]


def parse_date(value: str):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {value}")


def random_date(start: date, end: date) -> date:
    if start > end:
        return end

    day_range = (end - start).days
    return start + timedelta(days=random.randint(0, day_range))


def load_clients(client_file: Path) -> list[dict]:
    with client_file.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def choose_contact_outcome(contact_type: str) -> str:
    if contact_type == "Outreach Attempt":
        return random.choices(
            CONTACT_OUTCOMES,
            weights=[0.15, 0.30, 0.25, 0.08, 0.07, 0.15],
            k=1,
        )[0]

    return random.choices(
        CONTACT_OUTCOMES,
        weights=[0.55, 0.14, 0.10, 0.10, 0.06, 0.05],
        k=1,
    )[0]


def create_contacts_for_client(
    client: dict,
    starting_contact_id: int,
) -> list[dict]:
    client_id = int(client["ClientID"])
    staff_id = int(client["AssignedStaffID"])
    enrollment_date = parse_date(client["EnrollmentDate"])

    exit_date_text = client["ExitDate"].strip()
    end_date = parse_date(exit_date_text) if exit_date_text else TODAY

    contact_count = random.randint(
        MIN_CONTACTS_PER_CLIENT,
        MAX_CONTACTS_PER_CLIENT,
    )

    contact_dates = sorted(
        random_date(enrollment_date, end_date)
        for _ in range(contact_count)
    )

    contacts = []

    for offset, contact_date in enumerate(contact_dates):
        contact_type = random.choices(
            CONTACT_TYPES,
            weights=CONTACT_TYPE_WEIGHTS,
            k=1,
        )[0]

        outcome = choose_contact_outcome(contact_type)

        duration = ""
        follow_up_date = ""

        if outcome in SUCCESSFUL_OUTCOMES:
            duration = random.choice(
                [10, 15, 20, 30, 45, 60, 90]
            )

        if outcome in {
            "Successful",
            "Rescheduled",
            "No Answer",
            "Voicemail",
        }:
            follow_up_days = random.choice(
                [3, 7, 14, 21, 30]
            )
            calculated_follow_up = contact_date + timedelta(
                days=follow_up_days
            )

            if calculated_follow_up <= TODAY:
                follow_up_date = calculated_follow_up.isoformat()

        contacts.append(
            {
                "ContactID": starting_contact_id + offset,
                "ClientID": client_id,
                "StaffID": staff_id,
                "ContactDate": contact_date.isoformat(),
                "ContactType": contact_type,
                "ContactOutcome": outcome,
                "ContactDurationMinutes": duration,
                "FollowUpDate": follow_up_date,
                "ContactNotesCategory": random.choice(
                    CONTACT_NOTE_CATEGORIES
                ),
            }
        )

    return contacts


def main() -> None:
    project_folder = Path(__file__).resolve().parent.parent
    client_file = project_folder / "sample-data" / "client_data.csv"
    output_file = project_folder / "sample-data" / "contact_data.csv"

    clients = load_clients(client_file)

    all_contacts = []
    next_contact_id = 50001

    for client in clients:
        client_contacts = create_contacts_for_client(
            client,
            next_contact_id,
        )

        all_contacts.extend(client_contacts)
        next_contact_id += len(client_contacts)

    fieldnames = [
        "ContactID",
        "ClientID",
        "StaffID",
        "ContactDate",
        "ContactType",
        "ContactOutcome",
        "ContactDurationMinutes",
        "FollowUpDate",
        "ContactNotesCategory",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(all_contacts)

    print(f"Created {len(all_contacts)} fictional contacts.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()