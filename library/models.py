from django.db import models


class Book(models.Model):
    BookCoverChoices = [
        ("SOFT", "Soft"),
        ("HARD", "Hard"),
    ]
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100, choices=BookCoverChoices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
