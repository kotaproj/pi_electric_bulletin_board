import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import webcolors


# フォント
ttfontname = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
# 表示位置
top_shift = 0
# 色種別
rain_colors = ["red", "green", "blue", "cyan", "white", "magenta", "yellow"]

def regist_job(job_id: str, msg: str, color: str, fontsize: int) -> None:
    # 画像サイズ，背景色を設定
    canvasSize = (32*(len(msg)+2), 32)
    backgroundRGB = webcolors.name_to_rgb("black")

    # 文字を描く画像の作成
    img  = PIL.Image.new('RGB', canvasSize, backgroundRGB)
    draw = PIL.ImageDraw.Draw(img)

    # 用意した画像に文字列を描く
    x_off, y_off = fontsize, 0

    font = PIL.ImageFont.truetype(ttfontname, fontsize)

    for cnt, moji in enumerate(msg):
        textWidth, textHeight = draw.textsize(moji, font=font)
        textTopLeft = (x_off, top_shift)
        if color in ["rainbow", "primary"]:
            rgb = webcolors.name_to_rgb(rain_colors[cnt%len(rain_colors)])
        else:
            rgb = webcolors.name_to_rgb(color)
        draw.text(textTopLeft, moji, fill=rgb, font=font)
        x_off += textWidth

    # crop
    img = img.crop((0, 0, x_off+32, 32))
    img.save((job_id + ".png"))


import board
import neopixel
import time
import numpy as np
import cv2

is_running_pixel = False
stop_flag_pixel = False
pixel_pin = board.D18
num_pixels = 32*32
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.010, auto_write=False, pixel_order=ORDER
)

def show32x32_pixel(np_rgb):
    global pixels

    for cnt in range(32):
        if cnt%2 == 0:
            # [D],[C]エリア - 偶数行の並べ替え
            for scnt, val in enumerate(np_rgb[cnt,:16,]):
                pixels[1023 - cnt*16 - scnt] = (val[0], val[1], val[2])
            # [A],[B]エリア - 偶数行の並べ替え
            for scnt, val in enumerate(np_rgb[cnt,16:,]):
                pixels[cnt*16 + 16 - 1 - scnt] = (val[0], val[1], val[2])
        else:
            # [D],[C]エリア - 奇数行の並べ替え
            for scnt, val in enumerate(np_rgb[cnt,:16:,]):
                pixels[1024 - (cnt+1)*16 + scnt] = (val[0], val[1], val[2])
            # [A],[B]エリア - 奇数行の並べ替え
            for scnt, val in enumerate(np_rgb[cnt,16:,]):
                pixels[cnt*16 + scnt] = (val[0], val[1], val[2])
    pixels.show()
    return

def show_job(job_id: str, bright: float, interval: float) -> None:
    global stop_flag_pixel
    global is_running_pixel

    if is_running_pixel:
        stop_flag_pixel = True
        time.sleep(1)
    is_running_pixel = True

    # 消灯
    pixels.fill((0, 0, 0))
    pixels.show()
    
    # 明るさの指定
    pixels.brightness = 0.200 * bright

    img_path = job_id + ".png"

    cap = cv2.VideoCapture(img_path)
    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        h, w, _ = frame.shape
        # スクロール表示
        for srt in range(w-32):
            # 中断
            if stop_flag_pixel:
                stop_flag_pixel = False
                return
            show32x32_pixel(cv2.cvtColor(frame[:,srt:srt+32,:], cv2.COLOR_BGR2RGB))
            if 0.0 < interval:
                time.sleep(interval)
    time.sleep(0.1)

    # LED消灯
    pixels.fill((0, 0, 0))
    pixels.show()
    stop_flag_pixel = False
    is_running_pixel = False


def do_job(job_id: str, msg: str, color: str, fontsize: int, bright: int, interval: float) -> None:
    regist_job(job_id, msg, color, fontsize)
    show_job(job_id, bright, interval)
