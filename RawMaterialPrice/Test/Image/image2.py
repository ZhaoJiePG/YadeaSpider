# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#清除颜色
from PIL import Image,ImageFilter,ImageFont,ImageDraw
import pytesseract
myjpg = Image.open('meinv.jpg')
# 缩略图
savejpg = myjpg.filter(ImageFilter.GaussianBlur)
savejpg.save('smallmeinv.jpg')

savejpg.show()

ttFont = ImageFont.truetype("")

