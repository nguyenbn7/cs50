from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator, MinValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Auction(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=512)

    starting_price = models.FloatField(
        validators=[MinValueValidator(0.0, message="price can not below 0")])

    description = models.TextField(blank=True)

    photo = models.CharField(
        max_length=1024, validators=[URLValidator], blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True)

    listed_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Auctions"

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bids"

    def __str__(self):
        return f"{self.user}: {self.bid_price} {self.created}"


class Comment(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.auction}, {self.user}: {self.text}"


class WatchList(models.Model):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auctions")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users")

    class Meta:
        verbose_name_plural = "WatchList"

    def __str__(self):
        return f"{self.auction}: {self.user}"
