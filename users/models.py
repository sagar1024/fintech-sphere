from django.db import models
from django.contrib.auth.models import User
import yfinance as yf
from .utils import get_stock_price
from decimal import Decimal

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return self.user.username

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=4)
    shares = models.DecimalField(max_digits=10, decimal_places=4)
    invested_at = models.DateTimeField(auto_now_add=True)

    def current_value(self):
        stock_price = get_stock_price(self.stock_symbol)
        return self.shares * stock_price

    def profit_or_loss(self):
        current_value = self.current_value()
        return current_value - self.amount_invested
    