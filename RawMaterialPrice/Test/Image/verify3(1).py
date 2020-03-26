import tesserocr
from PIL import Image

# 二值化处理s
from pytesseract import pytesseract

#
# def two_value():
#     for i in range(1, 5):
#         # 打开文件夹中的图片
#         image = Image.open('1.jpg')
#         # 灰度图
#         lim = image.convert('L')
#         # 灰度阈值设为165，低于这个值的点全部填白色
#         threshold = 165
#         table = []
#
#         for j in range(256):
#             if j < threshold:
#                 table.append(0)
#             else:
#                 table.append(1)
#
#         bim = lim.point(table, '1')
#         bim.save('2.jpg')

# two_value()
# 去除干扰线
im = Image.open('2.jpg')
# 图像二值化
data = im.getdata()
w, h = im.size
black_point = 0

for x in range(1, w - 1):
    for y in range(1, h - 1):
        mid_pixel = data[w * y + x]  # 中央像素点像素值
        if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
            top_pixel = data[w * (y - 1) + x]
            left_pixel = data[w * y + (x - 1)]
            down_pixel = data[w * (y + 1) + x]
            right_pixel = data[w * y + (x + 1)]

            # 判断上下左右的黑色像素点总个数
            if top_pixel < 10:
                black_point += 1
            if left_pixel < 10:
                black_point += 1
            if down_pixel < 10:
                black_point += 1
            if right_pixel < 10:
                black_point += 1
            if black_point < 1:
                im.putpixel((x, y), 255)
            # print(black_point)
            black_point = 0
    im.save('3.jpg')

# 去除干扰线
im = Image.open('3.jpg')
# 图像二值化
data = im.getdata()
w, h = im.size
black_point = 0

for x in range(1, w - 1):
    for y in range(1, h - 1):
        if x < 2 or y < 2:
            im.putpixel((x - 1, y - 1), 255)
        if x > w - 3 or y > h - 3:
            im.putpixel((x + 1, y + 1), 255)

im.save('4.jpg')
image = Image.open('4.jpg')
content = pytesseract.image_to_string(image)  # 解析图片
print(content)