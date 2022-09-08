from modulefinder import packagePathMap
from certifi import contents
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import User, auction,Watchlist1,Bid,Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import sys
from time import sleep

#-------------------------------------------------------------------------------

def index(request):
    book = auction.objects.all()
    cate = ["car","book","flower"]
    return render(request, "auctions/index.html",
    {"books": book, "Cate":cate})
    
 #---------------------------------------------------------   
@login_required
def book(request):
    Message = "Please Login First"
    cate = ["car","book","flower"]
    if request.user.is_authenticated:
        if request.method == "POST":
            Username = request.user
            title = request.POST["title"]
            describtion = request.POST["describtion"]
            current = request.POST["current_price"]
            image = request.POST["image"]
            category= request.POST["category"]
           
            Auction = auction()
            Auction.username = Username
            Auction.title = title
            Auction.describtion = describtion
            Auction.current_price = current
            Auction.image = image
            Auction.category = category
            Auction.winerid=''
            Auction.save()
            return HttpResponseRedirect(reverse("index"))
        
        else : return render(request, "auctions/book.html",{
            "Cate" : cate
        })
    else : return render(request, "auctions/login.html",{
            "message" : Message
        })

#--------------------------------------------------------------------

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


#---------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#---------------------------------------------------------------

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


#---------------------------------------------------------------------------

@login_required
def add_watchlist(request, listing_id):
    item1 = get_object_or_404(auction, id = listing_id)
    if Watchlist1.objects.filter(user = request.user , item = listing_id).exists():
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("index"))
    user_list, created = Watchlist1.objects.get_or_create(user=request.user)
    user_list.item.add(item1)
    wach = Watchlist1.objects.get(user = request.user)
    wach1 = wach.item.all()
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse('Listing', args=[listing_id]))


#-----------------------------------------------------------------------------

@login_required
def watchlist(request):
    if Watchlist1.objects.filter(user = request.user).exists():
        wach = Watchlist1.objects.get(user = request.user)
        wach1 = wach.item.all().values()
    else:
        wach1 = []

    return render(request, 'auctions/watchlist.html',{
        "watchlist":wach1,
    })  

#------------------------------------------------------------------------------


def Listing(request,auction_id):
    Lsting_auction = auction.objects.get(pk=auction_id)
    x = 'current_price'
    z = 'winerid'
    winerid = getattr(Lsting_auction,z)
    auction_price = getattr(Lsting_auction,x)
    cate = ["car","book","flower"]

    com = Comment.objects.filter(auction = auction_id)
    if request.user.is_authenticated:
        t =0
        if  Watchlist1.objects.filter(user = request.user,item = auction_id).exists():
            x= 1
        if auction.objects.filter(id = auction_id, username = request.user).exists():
            ls = auction.objects.get(id = auction_id, username = request.user)
            p = 'conditions'
            Con = getattr(ls,p)
            if Con == "open":
                t=1
            
        if winerid == request.user.username:
            messages.add_message(request, messages.ERROR, "You won this auction")
        if request.method == "POST":
            biD= int(request.POST["bid"])
            if biD > auction_price:
                user = request.user
                id = auction_id
                BID = Bid()
                BID.bid = biD
                BID.username = user
                BID.auctionid = id
                BID.save()
                t = auction.objects.get(pk=auction_id)
                t.current_price = biD
                t.save()

                return HttpResponseRedirect(reverse('Listing', args=[auction_id]))
            else :  
                messages.add_message(request, messages.ERROR, "Your bid shoud be bigger than current price")
                return HttpResponseRedirect(reverse('Listing', args=[auction_id]))
        return render(request, "auctions/Listing.html",
        {"Listing":  Lsting_auction, "y":x, "T":t, "comments":com,"Cate":cate
        })  
    else : return render(request, "auctions/login.html",{
        "message": "Please login first"
    })


#----------------------------------------------------------------------------------
@login_required
def remove_watchlist(request,listing_id):
    act = Watchlist1.objects.get(user = request.user)
    attendee = auction.objects.get(pk = listing_id)
    act.item.remove(attendee)
    messages.add_message(request, messages.ERROR, "Remove Successfully")
    return HttpResponseRedirect(reverse('Listing', args=[listing_id]))

#----------------------------------------------------------------------------------

def category(request,Categ):
    auc = auction.objects.filter(category = Categ)
    cate = ["car","book","flower"]
    return render(request, "auctions/index.html",
    {"books": auc,"Cate":cate
    })

#-----------------------------------------------------------------------------------
@login_required
def close(request,auction_id):
    t = auction.objects.get(pk=auction_id)
    x = 'current_price'
    auction_price = getattr(t,x)
    mess = Bid.objects.get(auctionid = auction_id, bid = auction_price)
    z = 'username'
    User = getattr(mess,z)
    t.winerid = User
    t.conditions = 'close'
    t.save()
    return HttpResponseRedirect(reverse('Listing', args=[auction_id]))

#------------------------------------------------------------------------------------
@login_required
def comment(request,auction_id):
    if request.method == "POST":
        com= request.POST["comment"]
        c = Comment()
        c.user = request.user
        c.comment = com
        c.auction = auction_id
        c.save()
        messages.add_message(request, messages.ERROR, "add comment Successfully")
    return HttpResponseRedirect(reverse('Listing', args=[auction_id]))
