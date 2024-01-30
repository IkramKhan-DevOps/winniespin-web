from django.db import models

EVENT_TYPE_CHOICES = (
    ('private', 'Private'),
)

EVENT_STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    event_type = models.CharField(
        max_length=25, choices=EVENT_TYPE_CHOICES, default=EVENT_TYPE_CHOICES[0][0],
        help_text="There is only one event for now 'Private'"
    )
    status = models.CharField(
        max_length=25, choices=EVENT_STATUS_CHOICES, default=EVENT_STATUS_CHOICES[0][0],
        help_text="[draft = not visible, published = visible online, completed = event ended]"
    )
    spun_on = models.DateTimeField(help_text="Spun on", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    token_number = models.CharField(max_length=1000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.token_number


class Result(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'WINNER: {self.participant} > {self.event}'
