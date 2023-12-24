from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'from@example.com',  # Email address to send from
    ['to@example.com'],  # List of recipient email addresses
    fail_silently=False,
)
