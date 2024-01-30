from src.services.lucky_draw.models import (
    Event, Participant, Result
)
from faker import Faker
from django.db.utils import IntegrityError
from django.utils import timezone
from random import choice

fake = Faker()


def __print_start(model_name):
    print()
    print(f"MODEL: {model_name} - data faker started.")
    print()


def __print_ended(model_name):
    print()
    print(f"MODEL: {model_name} - data faker ended.")
    print()


def load_events_and_participants():
    __print_start("Events, Participants, and Results")

    event_type = 'private'
    event_status = choice(['draft', 'published', 'completed', 'cancelled'])

    events = [
        {
            "name": "Lottery 1",
            "description": "A lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 2",
            "description": "Another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
        {
            "name": "Lottery 3",
            "description": "Yet another lottery event with cash prize for the winner.",
            "event_type": event_type,
            "status": event_status,
            "spun_on": timezone.now(),
        },
    ]

    for event_data in events:
        name = event_data["name"]
        description = event_data["description"]
        event_type = event_data["event_type"]
        status = event_data["status"]
        spun_on = event_data["spun_on"]

        try:
            event = Event.objects.create(
                name=name,
                description=description,
                event_type=event_type,
                status=status,
                spun_on=spun_on,
            )

            # Generating participants for the event
            for _ in range(10):  # Generating 100 participants for each event
                token_number = fake.uuid4()  # Generate a random UUID as token number
                Participant.objects.create(
                    token_number=token_number,
                    event=event,
                )

            # Randomly selecting a winner and creating a result entry
            winner = Participant.objects.filter(event=event).order_by('?').first()
            Result.objects.create(participant=winner, event=event)

            print(f"---- Event: {name} created with participants: {event.participant_set.count()} and winner {winner}")
        except IntegrityError as e:
            print(e.__str__())

    __print_ended("Events, Participants, and Results")


def main():
    load_events_and_participants()


if __name__ == '__main__':
    main()
