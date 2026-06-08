from django.db import models

class Reservation(models.Model):
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    RESERVATION_STATUS_CHOICES = {
        CONFIRMED: 'Confirmed',
        CANCELLED: 'Cancelled'
    }
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    showtime = models.ForeignKey('showtimes.Showtime', on_delete=models.CASCADE)
    status = models.CharField(choices=RESERVATION_STATUS_CHOICES, default=CONFIRMED, max_length=10)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reservation for {self.user} with status {self.status}."

class ReservationSeat(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='seats')
    seat = models.ForeignKey('cinemas.Seat', on_delete=models.CASCADE)
    showtime = models.ForeignKey('showtimes.Showtime', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('showtime', 'seat')
    
    def __str__(self):
        return f"{self.reservation} for seat {self.seat}."