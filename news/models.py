from django.db import models
from decimal import Decimal

class NewsArticle(models.Model):
    stock_symbol = models.CharField(max_length=10)
    headline = models.TextField()
    sentiment = models.CharField(max_length=10)
    published_at = models.DateTimeField()
    impact_on_stock = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.headline} ({self.sentiment})"
