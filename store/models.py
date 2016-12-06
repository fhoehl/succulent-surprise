from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATES = (('S', 'Submitted'), ('P', 'Paid'),
              ('D', 'Dispatched'), ('E', 'Error'))

    updated_at = models.DateTimeField('Date created')
    state = models.CharField(max_length=1, choices=STATES, blank=True)

    stripe_tx = models.CharField('Stripe tx', max_length=100)

    from_first_name = models.CharField('Sender first name', max_length=60)
    from_last_name = models.CharField('Sender last name', max_length=60)
    from_email = models.CharField('Sender email', max_length=100)

    to_first_name = models.CharField('Recipient first name', max_length=60)
    to_last_name = models.CharField('Recipient last name', max_length=60)

    delivery_company_name = models.CharField('Company name', max_length=60, blank=True)
    delivery_first = models.CharField('Address line 1', max_length=100)
    delivery_second = models.CharField('Address line 2', max_length=100, blank=True)
    delivery_third = models.CharField('Address line 3', max_length=100, blank=True)
    delivery_postcode = models.CharField('Postcode', max_length=10)
    delivery_note = models.CharField('Gift note', max_length=200, blank=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return "[%s] %s %s for %s %s - %s" % (self.get_state_display(),
                                              self.from_first_name, self.from_last_name,
                                              self.to_first_name, self.to_last_name,
                                              self.delivery_postcode)
