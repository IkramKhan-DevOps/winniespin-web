from django.core.exceptions import ValidationError
from django.db import models
from django_resized import ResizedImageField

EVENT_TYPE_CHOICES = (
    ('private', 'Private'),
)

EVENT_STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)

SPUN_SPEED_CHOICES = (
    ('10', '10'),
    ('50', '50'),
    ('100', '100'),
    ('200', '200'),
    ('500', '500'),
)

SPUN_TIME_CHOICES = (
    ('10', '10'),
    ('25', '25'),
    ('50', '50'),
    ('100', '100'),
    ('250', '250'),
    ('500', '500'),
)


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="Some description about this event")

    spun_speed = models.CharField(
        max_length=3, default=SPUN_SPEED_CHOICES[0][0],
        choices=SPUN_SPEED_CHOICES, help_text="Speed to move over names"
    )
    spun_time = models.CharField(
        max_length=3, default=SPUN_TIME_CHOICES[0][0],
        choices=SPUN_TIME_CHOICES, help_text="Speed time took to move"
    )

    event_type = models.CharField(
        max_length=25, choices=EVENT_TYPE_CHOICES, default=EVENT_TYPE_CHOICES[0][0],
        help_text="There is only one event for now 'Private'"
    )
    status = models.CharField(
        max_length=25, choices=EVENT_STATUS_CHOICES, default=EVENT_STATUS_CHOICES[0][0],
        help_text="[draft = not visible, published = visible online, completed = event ended]"
    )
    spun_on = models.DateTimeField(help_text="Spin/Lucky draw date and time", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class Participant(models.Model):
    token_number = models.CharField(max_length=1000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('token_number', 'event')

    def __str__(self):
        return self.token_number


class Result(models.Model):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    image = ResizedImageField(
        upload_to='results/winners/', null=True, blank=True, size=[250, 250], quality=75, force_format='PNG',
        help_text='size of logo must be 250*250 and format must be png image file', crop=['middle', 'center']
    )
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'WINNER: {self.participant} > {self.event}'


