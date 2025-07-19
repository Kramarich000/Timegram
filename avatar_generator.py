from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def generate_avatar(path="avatar.jpg"):
    now = datetime.now().strftime("%H:%M")
    img = Image.new('RGB', (512, 512), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()

    draw.text((130, 200), now, font=font, fill=(255, 255, 255))
    img.save(path)
    return path
