from django.db.models import F
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Account, Item, Transaction
from .serializers import (AccountSerializer, ItemSerializer,
                          TransactionSerializer)


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(methods=["POST"], detail=False, url_path="buy")
    def buy(self, request):
        item_id = request.data.get("id")
        item = get_object_or_404(Item, pk=item_id)
        accounts = get_list_or_404(Account, user=self.request.user)
        account = max(accounts, key=lambda account: account.balance)
        transaction = Transaction.objects.create(
            account=account, amount=item.price
        )
        # can be implemented at "save" method of Transaction model
        account.balance = F("balance") - transaction.amount
        account.save()
        account.refresh_from_db()
        # account.update(balance=F("balance") - transaction.amount)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(
            user=self.request.user
        ).select_related("user").all()
