from distutils.command.upload import upload
from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class auction(models.Model):
    Condition = [
        ('open','open'),
        ('close','close'),
    ]
    conditions =  models.CharField(max_length=5, choices=Condition, default='open')
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, default=None)
    describtion = models.CharField(max_length=64, default=None)
    current_price = models.IntegerField()
    image = models.URLField(max_length=200)
    category = models.CharField(max_length=64, default=None)
    winerid = models.CharField(max_length=64, default=None)
   

    def __str__(self) :
        return f"{self.username}     {self.title}"

class Watchlist1 (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(auction, related_name="item2")

    def __str__(self):
        return f"{self.user}'s watchlist{self.item}"

class Bid(models.Model):
    bid = models.IntegerField()
    username = models.CharField(max_length=64, default=None)
    auctionid = models.IntegerField()

    def __str__(self):
        return f"bid = {self.bid} _ username = {self.username}  _ auctionid = {self.auctionid}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(default=None)
    auction = models.IntegerField()
