# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#清除颜色
import tesserocr
from PIL import Image,ImageFilter,ImageEnhance
import pytesseract
image = Image.open('../test/3.png')

# 删除背景方法
def pngdelbackgroud(image,color):
    # 加载所以图片的像素点
    picdata = image.load()
    width,height=image.size
    # 循环每个像素点，去除浅色的
    for y in range(height):
        for x in range(width):
            if picdata[x,y] < color:
                picdata[x,y]=0
            else:
                picdata[x,y]=255
    return image

def delpoint(image):
    picdata = image.load()
    # 循环每个像素点，去除浅色的
    width,height=image.size
    for y in range(1,height-1):
        for x in range(1,width-1):
            count = 0
            # 判断上下左右点是否接近白色
            if picdata[x,y-1] > 240:
                count=count+1
            if picdata[x,y+1] > 240:
                count=count+1
            if picdata[x-1,y] > 240:
                count=count+1
            if picdata[x+1,y] > 240:
                count=count+1
            if count>2:
                picdata[x,y] = 255

    return image


# 强化(模糊小点)
# image = image.filter(ImageFilter.MedianFilter())
# 过滤
# enhance = ImageEnhance.Contrast(image)
# 限定像素
# image = enhance.enhance(2)
# 清除比较淡的颜色
# image = image.point(lambda x:0 if x <143 else 255)
# 转换为黑白色
# image = image.convert("1")
# 灰度处理
image = image.convert("L")
image = pngdelbackgroud(image,100)
image.save("2.jpg")
image = delpoint(Image.open("2.jpg"))
image = image.convert("1")
image.save("3.jpg")


result = tesserocr.image_to_text(image)
print(result)

# image.show()
