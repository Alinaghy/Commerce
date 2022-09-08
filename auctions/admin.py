from django.contrib import admin
from .models import User, auction,Watchlist1,Bid,Comment

# Register your models here.
admin.site.register(auction)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
