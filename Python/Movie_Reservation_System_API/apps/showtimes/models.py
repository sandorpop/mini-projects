from django.db import models

class Showtime(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    cinema = models.ForeignKey('cinemas.Cinema', on_delete=models.CASCADE)
    starts_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movie} at {self.cinema}, start time: {self.starts_at}"