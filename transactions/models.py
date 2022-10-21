from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Item(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Item",
        help_text="Item's name",
    )
    description = models.CharField(
        max_length=512,
        verbose_name="description",
        help_text="Item description",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="price",
        help_text="price of item",
    )

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ("-id",)

    def __str__(self):
        return f"<{self.name}:{self.price}>"


class Account(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
        verbose_name="Account",
        help_text="User's account",
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="balance",
        help_text="User's account balance",
        validators=(
            MinValueValidator(
                Decimal(0.0),
                "Account balance can not be negative."
            ),
        )
    )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = ("-id",)
        constraints = (
            models.CheckConstraint(
                check=models.Q(balance__gte=Decimal(0.0)),
                name="Balance below zero is not allowed."
            ),
        )

    def __str__(self):
        return f"<{self.user.username} (account_id={self.pk})>"  # type:ignore


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        related_name="transactions",
        on_delete=models.CASCADE,
        verbose_name="Transaction",
        help_text="Transaction",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Money amount change",
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ("-id",)

    def __str__(self):
        return f"<{self.account}:{self.amount}>"
