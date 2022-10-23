from django.db import transaction
from django.db.models import F
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account, Item, Transaction, User
from .serializers import (AccountReplenishmentSerializer, AccountSerializer,
                          ItemSerializer, TransactionSerializer)


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(methods=["POST"], detail=False, url_path="buy")
    def buy(self, request):
        """
        Transaction will be created using account with max balance for user.
        """
        item = get_object_or_404(Item, pk=request.data.get("id"))
        accounts = self.request.user.accounts.all()  # type:ignore
        account = max(accounts, key=lambda account: account.balance)
        try:
            with transaction.atomic():
                account.balance = F("balance") - item.price
                account.save()
                account_transaction = Transaction.objects.create(
                    account=account, amount=-item.price
                )
        except IntegrityError:
            account.refresh_from_db()
            account_serializer = AccountSerializer(account)
            return Response(
                account_serializer.data,
                status=status.HTTP_403_FORBIDDEN
            )
        transaction_serializer = TransactionSerializer(account_transaction)
        return Response(
            transaction_serializer.data, status=status.HTTP_201_CREATED
        )


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(
            user=self.request.user
        ).select_related("user").all()


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            account__user=self.request.user
        ).select_related("account__user")


class AccountReplenishmentViewSet(viewsets.ViewSet):

    def partial_update(self, request):
        serializer = AccountReplenishmentSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data.get("user_id")
            account_id = serializer.data.get("account_id")
            amount = serializer.data.get("amount")

            user = get_object_or_404(User, pk=user_id)
            account = get_object_or_404(user.accounts, pk=account_id)  # type:ignore

            try:
                with transaction.atomic():
                    account.balance = F("balance") + amount
                    Transaction.objects.create(
                        account=account, amount=amount
                    )
                    account.save()
            except IntegrityError:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            account.refresh_from_db()
            account_serializer = AccountSerializer(account)
            return Response(account_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
