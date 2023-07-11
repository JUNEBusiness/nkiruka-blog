import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from .extensions import mail
from .models import User

# saves pictures and resize uploaded pictures to the filesystem
def save_picture(form_picture):
    # creates a random 8 bit hex
    random_hex = secrets.token_hex(8)
    # split the extension from the file name
    _, f_ext = os.path.splitext(form_picture.filename)
    # create a new filename with the extension and the hex
    picture_fn = random_hex + f_ext
    # create a piture path up until the package
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # set the piture dimension
    output_size = (125, 125)
    # open the image
    i = Image.open(form_picture)
    # set its size based on the dimension given
    i.thumbnail = (output_size)
    # save it to the root path created
    i.save(picture_path)
    return picture_fn


# removes profile pictures that are not needed
def delete_picture(previous_picture):
    # trace the piture path up until the package
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', previous_picture)
    # delete/remove picture from filesystem
    os.remove(picture_path)

    return 0


# handles sending mail to authenticate user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@tchelberwrites.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('views.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
