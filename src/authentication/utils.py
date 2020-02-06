from datetime import datetime, timedelta
import jwt


from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


def send_activation_email(user):
    """Send email with link (token) to activate user

    Arguments:
        user {User} -- inactive user

    Returns:
        int -- number of successfully delivered messages (0 or 1 since it can only send 1 message)
    """
    subject = "Welcome to MyC4 community"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    token = generate_token(user)
    path_ = reverse('auth:activation', kwargs={"token": token})

    full_path = "http://" + settings.URL_DOMAIN + path_

    message = 'Thanks for subscribe. Glad you are with us.'
    html_message = f"""
        <div class="container">
            <p class="text-center">Hello {user.username}. Welcome to MyC4</p>
            <p>Click on <a href="{full_path}">this link</a> to activate your account. Only then you will be able to play connect 4.</p>
            <h6>This link is active only for 15 minutes</h6>
        </div>
    """
    sent_mail = send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
        html_message=html_message
    )
    print("sent")
    return sent_mail


def generate_token(user):
    """Generate token containing user's username / email with secret key and algorithm

    Arguments:
        user {User} -- inactive user

    Returns:
        str -- generated token
    """
    payload = {
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(seconds=settings.TOKEN_EXPIRATION_DELTA)
    }
    key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    token = jwt.encode(payload, key, algorithm=algorithm).decode('utf-8')
    return token


def decode_token(token, verify=True):
    """Decode token

    Arguments:
        token {str} -- token
        leeway {int} -- part of expiration time during which expired token still can be decoded

    Returns:
        dict -- decoded_data
    """
    key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    data = jwt.decode(token, key, leeway=30, algorithms=[algorithm], verify=verify)
    return data
