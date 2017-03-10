from __future__ import unicode_literals

from django.db import models
from django.forms.models import model_to_dict
from django.utils.functional import cached_property
from datetime import datetime, date, timedelta
from statistics import mean
from math import isnan

# Create your models here.
class StockIndex(models.Model):
    "Object containing all stocks listed on an index"
    index_code = models.CharField(max_length=10)

class Stock(models.Model):
    "Object containing daily prices of a stock. To add groups later"
    stock_code = models.CharField(max_length=5)
    listed_index = models.ForeignKey(StockIndex, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

class DailyPrice(models.Model):
    "Daily price containing all information"
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, db_index=True)
    "Price fields"
    close_date = models.DateTimeField('Close Date', db_index=True)
    open_price = models.IntegerField(default=0)
    close_price = models.IntegerField(default=0)
    avg_price = models.IntegerField(default=0)
    floor_price = models.IntegerField(default=0)
    ceiling_price = models.IntegerField(default=0)
    highest = models.IntegerField(default=0)
    lowest = models.IntegerField(default=0)
    oscillate = models.IntegerField(default=0)
    "Other integer fields"
    dividend = models.IntegerField(default=0)
    eps = models.IntegerField(default=0)
    buy_redundancy = models.IntegerField(default=0)
    sell_redundancy = models.IntegerField(default=0)
    bvps = models.IntegerField(default=0)
    capital_level = models.IntegerField(default=0)
    curr_room = models.IntegerField(default=0)
    klcplh = models.BigIntegerField(default=0)
    klcpny = models.BigIntegerField(default=0)
    "Volume"
    avg_vol = models.IntegerField(default=0)
    trading_vol = models.BigIntegerField(default=0)
    total_vol = models.BigIntegerField(default=0)
    "Decimals"
    beta = models.DecimalField(max_digits=10, decimal_places=5)
    dec_pb = models.DecimalField(max_digits=20, decimal_places=10)
    dec_pe = models.DecimalField(max_digits=20, decimal_places=10)
    fw_pe = models.DecimalField(max_digits=20, decimal_places=10)
    "Raw data"
    raw_json = models.CharField(max_length=1024)

    @cached_property
    def oscillate_percent(self):
        "Returns oscillate as percentage"
        if self.close_price == 0:
            return 0
        else:
            return round(float(self.oscillate) * 100 / float(self.close_price), 2)

    @cached_property
    def weekday(self):
        return self.close_date.weekday()

    @cached_property
    def variation(self):
        return self.close_price - self.open_price
    
    # Moving average
    @cached_property
    def moving_average(self):
        AVERAGE_LIMIT=5 #MA of 5
        queryset = DailyPrice.objects.filter(stock=self.stock,
                close_date__date__lte=self.close_date.date()).order_by('close_date').only('close_price')[:AVERAGE_LIMIT]
        avg = mean([float(o.close_price) for o in list(queryset) if o.close_price ])
        return avg if not isnan(avg) else 0

    # Previous
    @cached_property
    def previous_close_price(self):
        try:
            query = DailyPrice.objects.filter(stock=self.stock,
                    close_date__date__lt=self.close_date.date()).only('close_price').latest('close_date')
            return query.close_price
        except:
            return self.close_price
    
    @cached_property
    def is_event(self):
        THRESHOLD = -0.1 # 10% price shock to indicate an event
        return 1 if ((float(self.close_price) - float(self.previous_close_price)) / float(self.close_price)) <= THRESHOLD else 0

    # T+3 properties
    @cached_property
    def close_price_t3(self):
        "Returns close price from T+3"
        t3date = self.close_date + timedelta(days=3)
        queryset = DailyPrice.objects.filter(stock=self.stock, close_date__date__gte=t3date.date()).only('close_price')
        result = queryset.first()
        if result is None:
            return 0
        else:
            return result.close_price
    
    @cached_property
    def oscillate_t3(self):
        t3price = self.close_price_t3
        if t3price == 0:
            return 0
        else:
            return t3price - self.close_price
    
    @cached_property
    def oscillate_percent_t3(self):
        if self.close_price == 0:
            return 0
        else:
            return round(float(self.oscillate_t3) * 100 / float(self.close_price), 2)

class ErrorLog(models.Model):
    date = models.DateTimeField('Date')
    dest_url = models.CharField(max_length=500)
    raw_json = models.CharField(max_length=1024)

class Scaler(models.Model):
    date = models.DateTimeField()
    data = models.BinaryField()

class LearnModel(models.Model):
    scaler = models.ForeignKey(Scaler, on_delete=models.CASCADE)
    model_type = models.IntegerField(default=0)
    data = models.BinaryField()
    date = models.DateTimeField()
    accuracy = models.DecimalField(max_digits=10, decimal_places=8)
