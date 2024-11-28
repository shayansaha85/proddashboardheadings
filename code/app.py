from PIL import Image, ImageDraw, ImageFont
import sys

def create_text_image(text, font_path, output_path):
    canvas_width = 904
    canvas_height = 50
    font_color = (1, 173, 210, 255)
    font_size = 50
    image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    font = ImageFont.truetype(font_path, int(font_size))
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = bbox[2] - bbox[0]
    x = (canvas_width - text_width) // 2
    y = 0
    draw.text((x, y), text.upper(), font=font, fill=font_color)
    image.save(output_path, "PNG")

input_text = sys.argv[1]
font_file_path = 'font.ttf'
output_file_path = sys.argv[2]

create_text_image(input_text, font_file_path, output_file_path)
print(f"Image saved as {output_file_path}")
