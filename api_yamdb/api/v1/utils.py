from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения YaMDb',
        message=(
            f'Здравствуйте, {user.username}!\n'
            f'Ваш confirmation_code: {confirmation_code}'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
