"""
!brew install zbar
!pip install pyqrcode
!pip install pyzbar

from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('horn.png'))
print(data[0][0].decode("utf-8"))

Aptfile:#need buildpack apt
libzbar0
libzbar-dev

"""


from pyzbar.pyzbar import decode
from PIL import Image
import sys
sys.path.append("..")
def qr_code_decode(pic):
    try:
        data = decode(Image.open(pic))
        info = data[0][0].decode("utf-8")
        print("已偵測到QR Code")
    except IndexError:
        info = ""
        print("未偵測到QR Code")
    return info



