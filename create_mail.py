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
    message = (' Image Link -> (https://drive.google.com/file/d/1GNdkUrEkQuLapItjbv54qKjQhpKZBY9L/view?usp=sharing) '
               ' Source Code -> (https://github.com/Rahulsati22/SeleniumTask/tree/main) '
               ' Resume Link -> (https://drive.google.com/file/d/1mpr5M5nCDwW7ZbGhnWDCEPwekBKCErbz/view?usp=sharing) '
               ' Portfolio Link -> (https://portfolio-new-six-delta.vercel.app/) '
               ' Yes i am available to work anytime '
               ' Approach -> (Firstly i inspected the code for google drive where i noticed each of the input tag has the same class name and the address field has different classname. So i targeted the class wrote down my input values and then using selenium went to the targeted website and filled all the values. After that I targeted the button with the text->Submit and then clicked on the button using selenium. After that i used django to send the email to the required user.)')
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['rahulsati2003@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    print("✅ Simple email sent successfully!")

# ---------------- HTML Email ----------------
def send_html_email():
    subject = "Welcome!"
    html_content = """
    <h2></h2>
    <p></p>
    <p></p>
    <p></p>
    <p></p>
    <p></p>
    """
    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        ['rahulsati2003@gmail.com']
    )
    email.content_subtype = "html"
    email.send()
    print("✅ HTML email sent successfully!")

if __name__ == "__main__":
    send_simple_email()
    # send_html_email()
