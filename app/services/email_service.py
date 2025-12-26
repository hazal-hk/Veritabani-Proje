from flask_mail import Message
from app import mail

def send_welcome_email(to_email, username):
    """welcome email for registered users"""
    subject = "Welcome!"
    body = f"""
    Hello {username},
    
    Your registration to the Smart Library system has been successfully completed. 
    You can now borrow books.

    Have a nice day!
    """
    
    #mail oluşturma
    msg = Message(subject=subject, recipients=[to_email], body=body)
    
    try:
        mail.send(msg) #hu komut mesajı terminale yazdırır
        print(f"\n[SYSTEM] A welcome email has been sent to '{to_email}'\n")
    except Exception as e:
        print(f"Mail error: {e}")

def send_loan_notification(to_email, username, book_title):
    """Information email sent to user who purchased the book"""
    subject = f"The book was borrowed: {book_title}"
    body = f"""
    Dear {username},

    You have borrowed the book titled '{book_title}'. 
    Please remember to return it within 15 days.

    Happy reading!
    """
    
    msg = Message(subject=subject, recipients=[to_email], body=body)
    
    try:
        mail.send(msg) #bu komut da yazdırır
        print(f"\n[SYSTEM] Book Information email sent to '{to_email}'\n")
    except Exception as e:
        print(f"Mail error: {e}")