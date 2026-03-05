from rest_framework import serializers

from borrowing.models import Borrowing
from library.models import Book
from library.serializers import BookSerializer


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Borrowing
        fields = ("id", "book", "book_title", "expected_return_date")

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("This book is out of stock.")
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        book = validated_data["book"]

        book.inventory -= 1
        book.save(update_fields=["inventory"])

        borrowing = Borrowing.objects.create(
            user=request.user,
            **validated_data,
        )
        return borrowing
