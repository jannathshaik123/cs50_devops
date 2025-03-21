from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # it inherits from the the AbstractUser (so it already have the username password and email!)
    image = models.URLField(default="https://image.ibb.co/jw55Ex/def_face.jpg")

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    max_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="possible_winner", blank=True, null=True)
    max_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    ## winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listings", blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def max_bid_amount(self):
        if self.max_bid == 0:
            return self.starting_bid
        return self.max_bid
    
    def winner(self):
        if self.active:
            return None
        return self.max_bidder

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioner")
    item_bid_on = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    

    def __str__(self):
        return f"{self.bidder} bid {self.amount} on {self.item_bid_on.title}"
    
class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="itemcomments")
    timepost = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented {self.text} on {self.item}"
    
class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="active_watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.watcher} - {self.listing}"
    
