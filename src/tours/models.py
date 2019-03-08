from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model

class Place(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        return f"Place: {self.name}"

class Tour(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    value_adult = models.DecimalField(decimal_places=2, max_digits=10)
    value_children = models.DecimalField(decimal_places=2, max_digits=10)
    pub_date = models.DateField(auto_now_add=True)
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    places = models.ManyToManyField(Place, blank=True, related_name="tour_places")
    #destination = models.CharField(max_length=50)

    def __str__(self):
        return f"Tour: {self.name}"

    def get_absolute_url(self):
        return reverse('tour', kwargs={'pk':self.id})
