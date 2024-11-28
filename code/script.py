from PIL import Image, ImageDraw, ImageFont
import sys
import base64
import os
import keyboard

base_dir = os.path.dirname(os.path.abspath(__file__))


def generateFileName(name):
    name_sgts = name.split()
    fileName = ""
    fileName += name_sgts[0].lower().strip()
    for i in range(1, len(name_sgts)):
        fileName += name_sgts[i][0].upper() + name_sgts[i][1:].lower()
    return fileName + ".png"


def generateFolderName(name):
    name_sgts = name.split()
    folderName = ""
    for names in name_sgts:
        folderName += names.strip().upper() + "_"
    folderName = folderName[0 : len(folderName) - 1]
    return folderName


def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_string = base64.b64encode(image_data).decode("utf-8")
            return base64_string
    except FileNotFoundError:
        return "Image file not found."
    except Exception as e:
        return f"An error occurred: {e}"


def create_text_image(text, font_path, output_path):
    canvas_width = 904
    canvas_height = 50
    font_color = (1, 173, 210, 255)
    font_size = 10
    image = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    while True:
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), text.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= canvas_width and text_height < canvas_height - 6:
            font_size += 1
        else:
            font_size -= 1
            break

    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (canvas_width - text_width) // 2
    y = 0

    draw.text((x, y), text.upper(), font=font, fill=font_color)
    image.save(output_path, "PNG")


textVal = input("Enter the text : ")
outputFileName = generateFileName(textVal)


input_text = textVal
dirName = generateFolderName(input_text)
try:
    os.mkdir(dirName)
except:
    print("*** FOLDER EXISTS ***")
font_file_path = os.path.join(base_dir, "font.ttf")
output_file_path = os.path.join(dirName, outputFileName)


create_text_image(input_text, font_file_path, output_file_path)
print(f"Image saved | Path : {output_file_path}")
mdcontent = (
    f"![{input_text}](data:image/png;base64,{image_to_base64(output_file_path)})"
)
mdfile = open(os.path.join(dirName, "content.md"), "w")
mdfile.write(mdcontent)
mdfile.close()

print("\nPress any key to exit...")
keyboard.read_event()
sys.exit()
