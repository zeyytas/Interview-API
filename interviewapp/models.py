
from django.db import models


class Interviewer(models.Model):
    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.email)


class Candidate(models.Model):
    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.email)


class Interview(models.Model):
    slot_choices = [(9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'),
                    (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18')]

    slot = models.CharField(choices=slot_choices, max_length=2)
    interviewer = models.ManyToManyField(Interviewer, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {}'.format(self.slot, self.interviewer, self.is_scheduled)
