from django.contrib import admin

# Register your models here.
from .models import Auction, Category, Comment, Bid, User


class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created']
    pass


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created']


class BidAdmin(admin.ModelAdmin):
    readonly_fields = ['created']


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
