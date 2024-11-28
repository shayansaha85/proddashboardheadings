import sys
from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter import StringVar
from PIL import Image, ImageDraw, ImageFont
import base64
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS

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

def generate_image():
    input_text = text_var.get().strip()
    if not input_text:
        messagebox.showerror("Error", "Please enter some text!")
        return

    outputFileName = generateFileName(input_text)
    dirName = generateFolderName(input_text)

    try:
        os.mkdir(dirName)
    except FileExistsError:
        print("*** FOLDER EXISTS ***")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create folder: {e}")
        return

    font_file_path = os.path.join(base_dir, "font.ttf")
    if not os.path.exists(font_file_path):
        messagebox.showerror("Error", "Font file not found!")
        return

    output_file_path = os.path.join(dirName, outputFileName)

    create_text_image(input_text, font_file_path, output_file_path)

    mdcontent = (
        f"![{input_text}](data:image/png;base64,{image_to_base64(output_file_path)})"
    )
    with open(os.path.join(dirName, "content.md"), "w") as mdfile:
        mdfile.write(mdcontent)

    messagebox.showinfo("Success", f"Image & Markdown Generated")

app = Tk()
app.title("NR Heading Generator")
app.geometry("500x200")
app.configure(bg="#2b2b2b")

icon_path = os.path.join(base_dir, "favicon.ico")
if os.path.exists(icon_path):
    app.iconbitmap(icon_path)
else:
    print("Favicon not found, please provide a valid 'favicon.ico'.")

text_var = StringVar()

Label(
    app, text="ENTER YOUR HEADING", font=("Calibri", 11, "bold"), bg="#2b2b2b", fg="#ffffff"
).pack(pady=10)

text_entry = Entry(app, textvariable=text_var, width=30, font=("Calibri", 12), bg="#3b3b3b", fg="#ffffff", insertbackground="#ffffff", relief="flat")
text_entry.pack(pady=5)

generate_button = Button(
    app,
    text="Generate",
    font=("Calibri", 11, "bold"),
    bg="#005f87",
    fg="#ffffff",
    activebackground="#007caf",
    activeforeground="#ffffff",
    command=generate_image,
)
generate_button.pack(pady=10)

footer_label = Label(
    app,
    text="Developed by ICC",
    font=("Calibri", 10, "italic"),
    bg="#2b2b2b",
    fg="#aaaaaa"
)
footer_label.pack(side="bottom", pady=10)

app.mainloop()
