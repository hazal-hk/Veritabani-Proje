from app.repositories import loan_repositories
from app.utils.email_sender import send_email
from datetime import date, timedelta

def send_due_date_reminders_service():
    tomorrow = date.today() + timedelta(days=1)
    upcoming_loans = loan_repository.find_loans_by_due_date(tomorrow)

    for loan in upcoming_loans:
        user = loan.user
        book = loan.book

        html_body = f"""
        <h3> Hi {user.username}, </h3>
        <p><b>{book.title}</b> is the last day to return. </p>
        <p> Please don't forget to return the book on time. </p>
        """

        send_email(user.email, "Book Return Remainder", html_body)
    
    print(f"{len(upcoming_loans)}reminder emails were sent.")
