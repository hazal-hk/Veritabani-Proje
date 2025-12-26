from app.repositories import fine_repository, user_repository

def create_fine_service(user_id, amount, reason):
    #kitap iade servisinii çağırır (şüpheli)
    return fine_repository.create_fine(user_id, amount, reason)

def get_my_fines_service(user_id):
    fines = fine_repository.get_user_fines(user_id)
    return [f.to_json() for f in fines]

def pay_fine_service(user_id, fine_id, card_details):
    # ceza var mı ve bu kişiye mi ait
    fine = fine_repository.get_fine_by_id(fine_id)
    if not fine:
        raise ValueError("No fine found")
    
    if str(fine.user_id) != str(user_id):
        raise ValueError("this fine is not yours!?")

    if fine.is_paid:
        raise ValueError("this fine has already been paid")

    # ödeme simülasyonu
    if not card_details.get('card_number') or len(card_details['card_number']) < 16:
        raise ValueError("Invalid credit card number")

    return fine_repository.pay_fine_db(fine).to_json()