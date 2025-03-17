# Register models to be displayed in the Django admin interfaces
import django.contrib.admin
from .models import User, AuctionListing, Bid, Comment, Watchlist, Category

# Register your models here.
django.contrib.admin.site.register(User)
django.contrib.admin.site.register(AuctionListing)
django.contrib.admin.site.register(Bid)
django.contrib.admin.site.register(Comment)
django.contrib.admin.site.register(Watchlist)
django.contrib.admin.site.register(Category)