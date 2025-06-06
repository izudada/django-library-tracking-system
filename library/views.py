from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Author, Book, Member, Loan
from .serializers import (
    AuthorSerializer, 
    BookSerializer, 
    MemberSerializer, 
    LoanSerializer,
    ExtendLoanDueDateSerializer
)
from rest_framework.decorators import action
from django.utils import timezone
from .services import LoanService
from .tasks import send_loan_notification

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(available_copies__gte=0)
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def loan(self, request, pk=None):
        response = LoanService.create_loan(
            member_id=request.data.get('member_id'),
            book=self.get_object()
        )
        return Response(response)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()
        member_id = request.data.get('member_id')
        try:
            loan = Loan.objects.get(book=book, member__id=member_id, is_returned=False)
        except Loan.DoesNotExist:
            return Response({'error': 'Active loan does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        loan.is_returned = True
        loan.return_date = timezone.now().date()
        loan.save()
        book.available_copies += 1
        book.save()
        return Response({'status': 'Book returned successfully.'}, status=status.HTTP_200_OK)

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post'], url_path='extend_due_date')
    def extend_due_date(self, request, pk=None):
        loan = self.get_object()
        serializer = ExtendLoanDueDateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid number of days"}, status=status.HTTP_400_BAD_REQUEST)
        
        extension_days = serializer.validated_data.get("additional_days")
        loan = LoanService.extend_loan_due_date(
            loan=loan,
            extension_days=extension_days
        )
        return Response(
            {"message": f"Due date extended by {extension_days} days.", "new_due_date": loan.due_date},
            status=status.HTTP_200_OK
        )
