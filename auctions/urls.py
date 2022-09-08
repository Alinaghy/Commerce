from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("book",views.book,name="book"),
    path("<int:auction_id>",views.Listing,name="Listing"),
    path("add_watchlist/<int:listing_id>/", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist/<int:listing_id>/", views.remove_watchlist, name="remove_watchlist"),
    path("category/<str:Categ>/", views.category, name="category"),
    path("<int:auction_id>/close",views.close,name="close"),
    path("<int:auction_id>/comment",views.comment,name="comment")
]
