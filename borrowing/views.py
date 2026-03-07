from datetime import date

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Borrowing.objects.select_related("user", "book")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(user=user)

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user__id=user_id)

        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset.distinct()

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        book = borrowing.book

        if not borrowing.actual_return_date:
            borrowing.actual_return_date = date.today()
            book.inventory += 1
            book.save()
            borrowing.save()
            return Response("Returned", status=status.HTTP_200_OK)
        else:
            return Response("Already returned", status=status.HTTP_400_BAD_REQUEST)
