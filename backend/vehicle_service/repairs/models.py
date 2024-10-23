from django.db import models
from django.utils import timezone

class Component(models.Model):
    name = models.CharField(max_length=255)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        return self.plate_number

class Issue(models.Model):
    REPAIR_TYPE_CHOICES = [
        ('repair', 'Repair'),
        ('purchase', 'New Purchase'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    repair_type = models.CharField(max_length=10, choices=REPAIR_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.repair_type == 'repair':
            self.price = self.component.repair_price
        else:
            self.price = self.component.purchase_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.component.name} ({self.repair_type})"
class Payment(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment for {self.issue}"

