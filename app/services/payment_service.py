from app.repositories import fine_repository, user_repository
import iyzipay

# iyzico Ayarları
API_KEY = "sandbox-NcMvyxu7KFT6nl9dKw2Q5U7P3CX7xod3"
SECRET_KEY = "YKi6hVvrWW6jhnlvbuOCoNt2mRbAvJrD"
BASE_URL = "https://sandbox-api.iyzipay.com"

def get_iyzico_options():
    options = iyzipay.Options()
    options.api_key = API_KEY
    options.secret_key = SECRET_KEY
    options.base_url = BASE_URL
    return options

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

    #kullanıcı bilgileri
    user = fine.user

    #iyzico ödeme isteği
    request = {
        'locale': 'tr',
        'conversationId': str(fine.id),
        'price': str(fine.amount),
        'paidPrice': str(fine.amount), # indirim yoksa aynısı
        'currency': 'TRY',
        'basketId': f"FINE-{fine.id}",
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "https://www.merchant.com/callback", # API modunda önemsiz
        "paymentCard": {
            'cardHolderName': card_details.get('card_holder_name', 'Misafir'),
            'cardNumber': card_details['card_number'],
            'expireMonth': card_details['expire_month'],
            'expireYear': card_details['expire_year'],
            'cvc': card_details['cvc'],
            'registerCard': '0'
        },
        "buyer": {
            'id': str(user.id),
            'name': "Hazal", # gerçek projede user.first_name
            'surname': "Karayigit", # gerçek projede user.last_name
            'gsmNumber': '+905350000000',
            'email': user.email,
            'identityNumber': '11111111110',
            'lastLoginDate': '2015-10-05 12:43:35',
            'registrationDate': '2013-04-21 15:12:09',
            'registrationAddress': 'Karadeniz Teknik Universitesi',
            'ip': '85.34.78.112',
            'city': 'Trabzon',
            'country': 'Turkey',
            'zipCode': '61000'
        },
        "shippingAddress": {
            'contactName': "Hazal Karayigit",
            'city': 'Trabzon',
            'country': 'Turkey',
            'address': 'Of Teknoloji Fakultesi',
            'zipCode': '61000'
        },
        "billingAddress": {
            'contactName': "Hazal Karayigit",
            'city': 'Trabzon',
            'country': 'Turkey',
            'address': 'Of Teknoloji Fakultesi',
            'zipCode': '61000'
        },
        "basketItems": [
            {
                'id': f"FINE-{fine.id}",
                'name': fine.reason,
                'category1': 'Library Fine',
                'itemType': 'VIRTUAL',
                'price': str(fine.amount)
            }
        ]
    }

    #iyzicoya gönder
    payment = iyzipay.Payment().create(request, get_iyzico_options())
    payment_result = payment.read().json()

    #sonucu kontrol et
    if payment_result['status'] == 'success':
        #ödeme başarılıysa veritabanında ödendi olarak işaretler
        updated_fine = fine_repository.pay_fine_db(fine)
        return {
            'status': 'success',
            'system_time': payment_result['systemTime'],
            'transaction_id': payment_result['paymentId'],
            'fine': updated_fine.to_json()
        }
    else:
        #ödeme başarısızsa hata mesajını döndür
        error_message = payment_result.get('errorMessage', 'Payment failed')
        raise ValueError(f"Payment failed: {error_message}")

    return fine_repository.pay_fine_db(fine).to_json()