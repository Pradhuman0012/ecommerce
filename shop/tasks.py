from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(user_email, order_id, product_name, quantity, payment_method, amount):
    subject = 'Order Confirmation'
    message = (
        f'Dear Customer,\n\n'
        f'Your order for "{product_name}" with ID "{order_id}" has been placed successfully!\n\n'
        f'Payment Method: {payment_method}\n'
        f'Quantity: {quantity}\n'
        f'Total Amount: ₹{amount}/-\n\n'
        f'Thank you for shopping with us!\n\n'
        f'Best regards,\n'
        f'Team Ecommerce'
    )

    try:    
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

@shared_task
def test_task():
    print("Test task executed")