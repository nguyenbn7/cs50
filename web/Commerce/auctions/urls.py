from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/create", views.listing_create, name="auction_create"),
    path("auction/close/<int:auction_id>/",
         views.auction_close, name="auction_close"),
    path("category", views.category, name="category"),
    path("bid/<int:auction_id>/", views.bid, name="bid"),
    path("listing/<int:auction_id>/", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:auction_id>/",
         views.watchlist_add, name="watchlist_add"),
    path("comment/add/<int:auction_id>/",
         views.comment_add, name="comment_add")
]
