import tesserocr
from PIL import Image
import tesserocr
from PIL import Image

img = Image.open("test.jpg")
print(tesserocr.image_to_text(img))