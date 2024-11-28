from PIL import Image, ImageDraw, ImageFont
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

def create_text_image(text, font_path, output_path):
    canvas_width = 904
    canvas_height = 50
    font_color = (1, 173, 210, 255)
    
    # Initial font size to start calculation
    font_size = 10  
    image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Dynamically adjust font size to fit the canvas
    while True:
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Check if the text fits within the canvas
        if text_width <= canvas_width and text_height < canvas_height-6:
            font_size += 1  # Increment font size
        else:
            font_size -= 1  # Revert to the last valid font size
            break
    
    # Use the adjusted font size
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (canvas_width - text_width) // 2
    y = 0
    
    # Draw the text
    draw.text((x, y), text.upper(), font=font, fill=font_color)
    image.save(output_path, "PNG")

input_text = sys.argv[1]
font_file_path = os.path.join(base_dir, "font.ttf")
output_file_path = sys.argv[2]

create_text_image(input_text, font_file_path, output_file_path)
print(f"Image saved as {output_file_path}")
