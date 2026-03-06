import os

import cv2
import numpy
import PIL.Image as PImage
from PIL import ImageFont, ImageDraw

from idcard_generator import utils

# 资源目录（相对于本文件的绝对路径，不依赖运行目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
asserts_dir = os.path.join(BASE_DIR, 'asserts')


def _change_background(img_bgra, img_back_bgra, zoom_size, center):
    """通过 HSV 颜色检测自动抠图，将头像合成到背景卡片上"""
    img = cv2.resize(img_bgra, zoom_size)
    rows, cols = img.shape[:2]

    # 取 BGR 三通道做 HSV 转换（去掉 alpha 通道）
    img_bgr = img[:, :, :3]
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # 以左上角像素颜色为基准，生成背景色 mask
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = numpy.array(gb - diff)
    upper_blue = numpy.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 腐蚀膨胀去噪
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 将前景像素覆盖到背景上
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0 = 非背景像素
                img_back_bgra[center[0] + i, center[1] + j] = img[i, j]

    return img_back_bgra


def _get_addr_lines(addr):
    """将住址按显示宽度分行（中文字符占 2 位宽）"""
    addr_lines = []
    start = 0
    while start < utils.get_show_len(addr):
        show_txt = utils.get_show_txt(addr, start, start + 22)
        addr_lines.append(show_txt)
        start += 22
    return addr_lines


def generate_id_card(data, avatar_file, use_matting=True):
    """
    生成身份证图片。

    Args:
        data: dict，包含 name/sex/nation/year/month/day/addr/idn/org/life
        avatar_file: 文件对象（file-like object），头像图片
        use_matting: bool，是否自动抠图

    Returns:
        (color_image, bw_image): 两张 PIL Image（彩色、黑白）
    """
    avatar = PImage.open(avatar_file)
    empty_image = PImage.open(os.path.join(asserts_dir, 'empty.png'))

    # 确保模板为 RGBA
    if empty_image.mode != 'RGBA':
        empty_image = empty_image.convert('RGBA')

    # 加载字体
    name_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 72)
    other_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/hei.ttf'), 64)
    birth_date_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/fzhei.ttf'), 60)
    id_font = ImageFont.truetype(os.path.join(asserts_dir, 'fonts/ocrb10bt.ttf'), 90)

    draw = ImageDraw.Draw(empty_image)

    # 正面信息
    draw.text((630, 690), data.get('name', ''), fill=(0, 0, 0), font=name_font)
    draw.text((630, 840), data.get('sex', ''), fill=(0, 0, 0), font=other_font)
    draw.text((1030, 840), data.get('nation', ''), fill=(0, 0, 0), font=other_font)
    draw.text((630, 975), data.get('year', ''), fill=(0, 0, 0), font=birth_date_font)
    draw.text((950, 975), data.get('month', ''), fill=(0, 0, 0), font=birth_date_font)
    draw.text((1150, 975), data.get('day', ''), fill=(0, 0, 0), font=birth_date_font)

    # 住址（自动换行）
    addr_loc_y = 1115
    for addr_line in _get_addr_lines(data.get('addr', '')):
        draw.text((630, addr_loc_y), addr_line, fill=(0, 0, 0), font=other_font)
        addr_loc_y += 100

    # 身份证号
    draw.text((900, 1475), data.get('idn', ''), fill=(0, 0, 0), font=id_font)

    # 背面信息
    draw.text((1050, 2750), data.get('org', ''), fill=(0, 0, 0), font=other_font)
    draw.text((1050, 2895), data.get('life', ''), fill=(0, 0, 0), font=other_font)

    # 合成头像
    if use_matting:
        # 确保头像为 RGBA
        if avatar.mode != 'RGBA':
            avatar = avatar.convert('RGBA')
        avatar_cv = cv2.cvtColor(numpy.asarray(avatar), cv2.COLOR_RGBA2BGRA)
        bg_cv = cv2.cvtColor(numpy.asarray(empty_image), cv2.COLOR_RGBA2BGRA)
        bg_cv = _change_background(avatar_cv, bg_cv, (500, 670), (690, 1500))
        empty_image = PImage.fromarray(cv2.cvtColor(bg_cv, cv2.COLOR_BGRA2RGBA))
    else:
        avatar = avatar.resize((500, 670))
        avatar = avatar.convert('RGBA')
        empty_image.paste(avatar, (1500, 690), mask=avatar)

    bw_image = empty_image.convert('L')
    return empty_image, bw_image
