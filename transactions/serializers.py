import os
from decimal import Decimal

from rest_framework import serializers

from .models import Account, Item, Transaction, User
from .utils import sign_transaction


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


class AccountReplenishmentSerializer(serializers.Serializer):
    signature = serializers.CharField(min_length=40, max_length=40)
    transaction_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)
    bill_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(0.01)
    )

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "User with provided id does not exists."
            )
        return value

    def validate(self, data):
        private_key = os.getenv("TRANSACTION_SIGNATURE_SIGNING_KEY")
        generated_signature = sign_transaction(
            private_key,
            data.get("transaction_id"),
            data.get("user_id"),
            data.get("bill_id"),
            data.get("amount")
        )
        if data.get("signature") != generated_signature:
            raise serializers.ValidationError("Signature does not match.")
        return data
