import base64, uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    _ , str_image = data.split(';base64')
    # _ = data: image/png in the file (like a header)
    # str_image = the image we want to decode and make into image of 'png'
    decoded_img = base64.b64decode(str_image)
    img_name = str(uuid.uuid4())[:10] + '.png'
    data = ContentFile(decoded_img, name=img_name)
    return data
