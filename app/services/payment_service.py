from app.repositories import fine_repository, user_repository

def create_fine_service(user_id, amount, reason):
    # Bu fonksiyonu genelde "Kitap İade" servisi çağırır
    return fine_repository.create_fine(user_id, amount, reason)

def get_my_fines_service(user_id):
    fines = fine_repository.get_user_fines(user_id)
    return [f.to_json() for f in fines]

def pay_fine_service(user_id, fine_id, card_details):
    # 1. Ceza var mı ve bu kullanıcıya mı ait?
    fine = fine_repository.get_fine_by_id(fine_id)
    if not fine:
        raise ValueError("Ceza bulunamadı.")
    
    if str(fine.user_id) != str(user_id):
        raise ValueError("Bu ceza size ait değil!")

    if fine.is_paid:
        raise ValueError("Bu ceza zaten ödenmiş.")

    # 2. Ödeme Simülasyonu (Burada normalde Iyzico/Stripe olur)
    if not card_details.get('card_number') or len(card_details['card_number']) < 16:
        raise ValueError("Geçersiz kredi kartı numarası!")

    return fine_repository.pay_fine_db(fine).to_json()