from rrumble import app
from PIL import Image
import secrets
import os

def photo_update(new_photo):
    phex= secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_photo.filename)
    new_name = phex + f_ext
    new_loc = os.path.join(app.root_path, 'static/media/profphot', new_name)
    output = (640, 462)
    i = Image.open(new_photo)
    i.thumbnail(output)
    i.save(new_loc)
   
    return new_name

# def photo_update(new_photo):
#     with open(str(new_photo), 'rb') as readble: 
#         new_loc = os.path.join(app.root_path, 'static/media/profphot', new_photo)
#         output = (640, 462)
#         i = Image.open(readble)
#         i.thumbnail(output)
#         i.save(new_loc)
    
#         return new_photo


# def photo_update(new_photo):
#     with open(str(new_photo), 'rb') as readble: 
#         new_loc = os.path.join(app.root_path, 'static/media/profphot', readble)
#         readble.save(new_loc)
    
#         return new_photo