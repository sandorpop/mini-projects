from django.db import models
import string
import math

class Seat(models.Model):
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1)
    number = models.IntegerField(null=False)
    
    class Meta:
        unique_together = ('cinema', 'row', 'number')
    
    def __str__(self):
        return f"{self.cinema}, row {self.row}, number {self.number}."

class Cinema(models.Model):
    name = models.CharField(max_length=255, unique=True)
    total_seats = models.IntegerField(null=False)
    
    def generate_seats(self):
        total_seats = self.total_seats
        
        if total_seats <= 80:
            seats_per_row = 8
        elif total_seats <= 150:
            seats_per_row = 10
        elif total_seats <= 250:
            seats_per_row = 12
        else:
            seats_per_row = 16
        
        num_rows = math.ceil(total_seats / seats_per_row)
        letters = string.ascii_uppercase
        row_labels = letters[:num_rows]
        seats = [
            Seat(cinema=self, row=row_labels[row], number=seat)
            for row in range(num_rows)
            for seat in range(1, seats_per_row + 1)
        ][:total_seats]
        
        Seat.objects.bulk_create(seats)
    
    def __str__(self):
        return self.name