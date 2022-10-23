import os
from decimal import Decimal

from rest_framework import serializers

from .models import Account, Item, Transaction, User
from .utils import sign_transaction


class FloatDecimalField(serializers.Field):

    def to_representation(self, value):
        return float(value)


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price",)
        read_only_fields = ("id", "name", "description", "price",)


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    balance = FloatDecimalField()

    class Meta:
        model = Account
        fields = ("id", "user", "balance",)
        read_only_fields = ("id", "user", "balance",)


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    amount = FloatDecimalField()

    class Meta:
        model = Transaction
        fields = ("account", "amount",)
        read_only_fields = ("account", "amount",)


class AccountReplenishmentSerializer(serializers.Serializer):
    signature = serializers.CharField(min_length=40, max_length=40)
    transaction_id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)
    account_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal(0.01)
    )

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "User with provided id does not exists."
            )
        return value

    def validate_account_id(self, value):
        if not Account.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "Account with provided id does not exists."
            )
        return value

    def validate(self, data):
        private_key = os.getenv("TRANSACTION_SIGNATURE_SIGNING_KEY")
        generated_signature = sign_transaction(
            private_key,
            data.get("transaction_id"),
            data.get("user_id"),
            data.get("account_id"),
            data.get("amount")
        )

        if data.get("signature") != generated_signature:
            raise serializers.ValidationError("Signature does not match.")

        user = User.objects.get(pk=data.get("user_id"))
        provided_account = Account.objects.get(pk=data.get("account_id"))

        if provided_account not in user.accounts.all():  # type:ignore
            raise serializers.ValidationError(
                "Given user is not owner of provided account."
            )
        return data
