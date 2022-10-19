from rest_framework import serializers

from .models import Account, Item, Transaction


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price",)


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ("id", "user", "balance",)
        read_only_fields = ("id", "user", "balance",)


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = ("account", "amount",)
        read_only_fields = ("account", "amount",)
