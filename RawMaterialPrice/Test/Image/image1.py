# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#清除颜色
from PIL import Image,ImageFilter,ImageEnhance
import pytesseract
image = Image.open('1.jpg')


# 强化(模糊小点)
# image = image.filter(ImageFilter.MedianFilter())
# 过滤
# enhance = ImageEnhance.Contrast(image)
# 限定像素
# image = enhance.enhance(2)
# 清除比较淡的颜色
# image = image.point(lambda x:0 if x <143 else 255)
# 转换为黑白色
image = image.convert("1")
image.save("2.jpg")
