from app.repositories import loan_repository, book_repository, fine_repository
from datetime import datetime
from app.services import email_service

# günlük gecikme cezası 
DAILY_FINE_AMOUNT = 5.0 

def borrow_book_service(user_id, book_id):
    #kitap var mı
    book = book_repository.get_book_by_id(book_id)
    if not book:
        raise ValueError("KThe book was not found")
    
    #peki kitap zaten kullanıcıda var mı
    if loan_repository.get_active_loan(user_id, book_id):
        raise ValueError("you already borrowed this book?? and haven't returned it")

    #gerekeni sağladıysa ödünç verdik - ilişkilere ihtiyaç olduğıu için json yok
    loan = loan_repository.create_loan(user_id, book_id)

    #maili tetikle
    email_service.send_loan_notification(loan.user.email, loan.user.username, loan.book.title)

    #şimdi jsona çevirebilirz
    return loan.to_json()

def return_book_service(user_id, book_id):
    #ödünç alıp da iade etmesi gereken bir kitabı var mı
    loan = loan_repository.get_active_loan(user_id, book_id)
    if not loan:
        raise ValueError("no active loan record was found to be returned")

    #iade işlemini veritabanına işler
    loan = loan_repository.return_loan_db(loan)

    
    #cezayı şöyle hesaplayacaq
    #eğer iade tarihi son teslim tarihinden büyükse
    if loan.return_date > loan.due_date:
        #geciken gün sayısını bulucak
        delta = loan.return_date - loan.due_date
        overdue_days = delta.days
        
        if overdue_days > 0:
            fine_amount = overdue_days * DAILY_FINE_AMOUNT
            reason = f"Late Payment Penalty: {loan.book.title} ({overdue_days} day)"
            
            fine_repository.create_fine(user_id, fine_amount, reason)
            
            return {
                "message": f"The book was returned, but a penalty of {fine_amount} TL was charged due to a delay of {overdue_days} days.",
                "fine_applied": True
            }

    return {"message": "The book was returned on time... Thank you!", "fine_applied": False}