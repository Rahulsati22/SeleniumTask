import django
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

# ---------------- Django Email Configuration ----------------
settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER='rahulsati9969@gmail.com',
    EMAIL_HOST_PASSWORD='dktl gwqa wujq jplc',
)

django.setup()

# ---------------- Plain Text Email ----------------
def send_simple_email():
    subject = 'Hello from Django'
    message = 'This is a test email sent using Django and Gmail SMTP.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['rahulsati2003@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    print("✅ Simple email sent successfully!")

# ---------------- HTML Email ----------------
def send_html_email():
    subject = "Welcome!"
    html_content = """
    <h2>Hello from Django</h2>
    <p>This is an <b>HTML email</b> sent using Gmail SMTP.</p>
    """
    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        ['recipient@example.com']
    )
    email.content_subtype = "html"
    email.send()
    print("✅ HTML email sent successfully!")

if __name__ == "__main__":
    send_simple_email()
    send_html_email()

