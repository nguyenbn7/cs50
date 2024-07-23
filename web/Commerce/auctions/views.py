from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Auction, Category, Bid, WatchList, Comment


def index(request):
    category = request.GET.get("category")
    context = {}
    context["auctions"] = []
    # logic for getting list auction based on category
    if category:
        auctions = Auction.objects.filter(
            category=Category.objects.get(name__iexact=category).id)
    else: # this one is not based on category
        auctions = Auction.objects.all()
    # add watchlist status to active listing
    for auction in auctions:
        last_bid = Bid.objects.filter(auction=auction).order_by("bid_price").last()
        if last_bid:
            auction.starting_price = last_bid.bid_price
        context["auctions"].append([auction, WatchList.objects.filter(auction=auction).count()])
    return render(request, "auctions/index.html", context=context)


def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })


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


@ login_required
def listing_create(request):
    if request.method == "POST":
        # get auction's title
        title = request.POST.get("title", "")

        # get auction's starting price
        starting_price = float(request.POST.get("price", "0"))

        # get auction's image url
        image_url = request.POST.get("image")
        if not image_url or image_url == "":
            image_url = "https://makitweb.com/demo/broken_image/images/noimage.png"

        # get auction's description
        description = request.POST.get("description", "")

        # get auction's category
        category = request.POST.get("category")
        if not category or category == "":
            category = "Unknown"

        # add page to db
        category = Category.objects.get(name__iexact=category)
        auction = Auction(title=title, starting_price=starting_price,
                          description=description, category=category, photo=image_url, listed_by=request.user)
        auction.save()

        # message for succeeding create auction
        messages.success(request, "Create successful!")

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


@login_required
def watchlist_add(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    wl = WatchList.objects.filter(auction=auction, user=request.user)
    # toggle logic watchlist
    if wl.exists():
        wl.delete()
    else:
        WatchList(auction=auction, user=request.user).save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def watchlist(request):
    context = {}
    context["auctions"] = []
    auctions = get_auctions(request.user)
    # replace staring price to highest bid
    for auction in auctions:
        last_bid = Bid.objects.filter(auction=auction).order_by("bid_price").last()
        if last_bid:
            auction.starting_price = last_bid.bid_price
        context["auctions"].append(auction)
    return render(request, "auctions/watchlist.html", context=context)


def listing(request, auction_id):
    # prepare context
    context = {}
    
    # pass auction oof current id to context
    context["auction"] = Auction.objects.get(id=auction_id)

    # count how far from request.user to who has highest bidder
    context["current_bidder_count"] = 0

    # if user login then user can add page to their watch list
    if request.user.is_authenticated:
        context["watchlist"] = WatchList.objects.filter(
            auction=context["auction"], user=request.user).exists()

    bids = Bid.objects.filter(auction=context["auction"]).order_by("-bid_price")

    # count how many bids have made for auction
    context["bids_count"] = len(bids)
    # variable for user who has highest bid
    context["current_bidder"] = None

    # if there is no any bids then use starting price
    if not bids:
        context["current_bid"] = context["auction"].starting_price
    else:
        # get user and price and check if that user is current the one who has highest bid
        context["current_bidder"] = bids[0].user
        context["current_bid"] = bids[0].bid_price
        for i, bid in enumerate(bids):
            if bid.user == request.user:
                break
            context["current_bidder_count"] += 1

    if not context["auction"].is_active:
        context["winner"] = bids[0].user if bids else context["auction"].listed_by

    context["comments"] = Comment.objects.filter(auction=context["auction"])

    return render(request, "auctions/listing.html", context=context)


@ login_required
def bid(request, auction_id):
    if request.method == "POST":

        bid_price = float(request.POST.get("bid", "0"))
        auction = Auction.objects.get(id=auction_id)
        bids = Bid.objects.filter(auction=auction).order_by("-bid_price")

        # prevent from getting empty bid
        if not bids:
            current_bid = auction.starting_price
        else:
            current_bid = bids[0].bid_price

        # check if price is less than or equal to current price
        if request.user != auction.listed_by and auction.is_active:
            if bid_price <= current_bid:
                messages.error(
                    request, "Bid price must be greater than current price")
            else:
                Bid(auction=auction,
                    bid_price=bid_price, user=request.user).save()
                messages.success(request, "Bid successful!")

        else:
            messages.error(request, "Error occurs. Please try again")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def auction_close(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    # auction can be closed which is active and owned by user who create
    if auction.listed_by == request.user and auction.is_active:
        auction.is_active = False
        auction.save()
        messages.success(request, "Close successful")
    else:
        messages.error(request, "Error occurs. Please try again")
    return HttpResponseRedirect(reverse("listing", args={auction_id,}))


@login_required
def comment_add(request, auction_id):
    if request.method == "POST":
        text = request.POST.get("comment", "")
        if len(text) == 0:
            messages.error(request, "Comment can not be blank")
        else:
            Comment(user=request.user, text=text,
                    auction=Auction.objects.get(id=auction_id)).save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# function return set of auction filter by user
def get_auctions(user: User):
    wl = WatchList.objects.filter(user=user)
    items = set()
    for w in wl:
        items.add(w.auction)
    return Auction.objects.none() | items
