from django.contrib import admin

from .models import Account, Item, Transaction


class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance",)
    list_select_related = ("user",)
    empty_value = "--empty--"


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price",)
    empty_value = "--empty--"


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "amount",)
    list_select_related = ("account",)
    empty_value = "--empty--"


admin.site.register(Account, AccountAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transaction, TransactionAdmin)
