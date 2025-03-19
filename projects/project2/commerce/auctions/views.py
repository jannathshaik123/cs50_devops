from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Bid, Comment, Watchlist , Category


def index(request):
    return render(request, "auctions/index.html",
                  {"active_listings": AuctionListing.objects.filter(active=True)})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required(login_url="/login")    
def listing(request, listing_id):
    message = None
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.method == "POST":
        if "comment" in request.POST:
            text = request.POST["comment"]
            Comment.objects.create(text=text, user=request.user, item=listing)
        elif "bid" in request.POST or "watchlist" not in request.POST:
            amount = request.POST["bid"]
            if float(amount) > listing.max_bid_amount():
                message = "Bid placed successfully at"
                listing.max_bid = amount
                listing.max_bidder = request.user
                listing.save()
                Bid.objects.create(amount=amount, bidder=request.user, item_bid_on=listing)
            else:
                message = "Your bid must be higher than the current bid at"
        else:
            Watchlist.objects.get_or_create(watcher=request.user, listing=listing)
            return HttpResponseRedirect(reverse("watchlist"))
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "max_bid": listing.max_bid_amount(),
        "user": request.user,
        "comments": Comment.objects.filter(item=listing)
    })

@login_required(login_url="/login") 
def close(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    # try:
    if request.method == "POST":
        # listing = AuctionListing.objects.get(pk=request.POST["listing"])
        if listing.max_bid != 0:
            listing.active = False
            message = "Auction closed successfully at."
            listing.save()
        else:
            message = "You cannot close an auction without any bids."
        return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": message,
                "max_bid": listing.max_bid_amount(),
                "user": request.user,
                "comments": Comment.objects.filter(item=listing)
            })
        
@login_required(login_url="/login")
def watchlist(request):
    if request.method == "POST":
        Watchlist.objects.get(watcher=request.user, listing=AuctionListing.objects.get(pk=request.POST["listing"])).delete()
        return HttpResponseRedirect(reverse("watchlist"))
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(watcher=request.user)
    })