import stripe
from config.settings import STRIPE_API_KEY
from education.models import Payment


stripe.api_key = STRIPE_API_KEY


def create_payment_data(amount):
    pay = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        automatic_payment_methods={"enabled": True,
                                   "allow_redirects": "never"}
    )

    return pay


def retrieve_payment_data(stripe_id):
    return stripe.PaymentIntent.retrieve(
        stripe_id,
    )


def confirm_payment(stripe_id):
    try:
        response = stripe.PaymentIntent.confirm(
            stripe_id,
            payment_method="pm_card_visa",
        )

        return response

    except Exception as error:
        print(error)


def check_payment():
    for pay in Payment.objects.filter(status__isnull=False):
        if pay.status != "succeeded":
            response = retrieve_payment_data(pay.stripe_id)
            if response["status"] == "succeeded":
                pay.status = "succeeded"
                pay.save()
            else:
                confirm_payment(pay.stripe_id)
