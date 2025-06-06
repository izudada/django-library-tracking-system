from datetime import timedelta

from rest_framework import status

from .models import Book, Loan, Member

class LoanService:

    @classmethod
    def create_loan(cls, member_id, book):
        from .tasks import send_loan_notification

        try:
            member = Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            return {'error': 'Member does not exist.'}, status.HTTP_400_BAD_REQUEST
        loan = Loan.objects.create(book=book, member=member)
        book.available_copies -= 1
        book.save()
        send_loan_notification.delay(loan.id)
        return {"message": "Record created successfully"}, 200

    @classmethod
    def extend_loan_due_date(cls, loan, extension_days):
        loan.due_date += timedelta(
            days=extension_days
        )
        loan.save()
        return loan
