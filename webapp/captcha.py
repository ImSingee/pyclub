from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random

# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def generate_verification_code():

    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('./static/fonts/Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    strings = ''
    for t in range(4):
        char = rndChar()
        draw.text((60 * t + 10, 10), char, font=font, fill=rndColor2())
        strings += char
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('./static/image/code/'+'code_img.jpg', 'jpeg')
    return 'code_img.jpg', strings
    
print(generate_verification_code())
# import cStringIO
#     tmps = cStringIO.StringIO()
#     image.save(tmps, "jpeg")
#     res = Response()
#     res.headers.set("Content-Type", "image/JPEG;charset=UTF-8")
#     res.set_data(tmps.getvalue())
#     return res

#  <img id="verficode" src="./verficode">
#  <img id="verficode" src="./verficode" onclick="window.location.reload()">
#  <img id="verficode" src="./verficode" onclick="this.src='./verficode?d='+Math.random();" />