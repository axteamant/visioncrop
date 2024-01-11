import pyautogui
import tkinter as tk
from openai import OpenAI
from tkinter import scrolledtext, filedialog
import os
import argparse
import numpy as np
import cv2
from google.oauth2 import service_account
from google.cloud import vision
import argparse
import cv2
from tkinter import scrolledtext
import io
import argparse
from enum import Enum
from google.cloud import vision
from PIL import Image, ImageDraw
from google.cloud import vision
from PIL import Image, ImageDraw
import os
from screeninfo import get_monitors

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tkinter import Tk, Canvas


class ImageCropper:
    def __init__(self, image_path):
        self.image_path = image_path
        self.fig, self.ax = plt.subplots(1)
        self.rect = Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
        self.ax.add_patch(self.rect)
        self.ax.imshow(plt.imread(image_path))
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.is_cropping = False
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        plt.show()

    def on_press(self, event):
        if event.inaxes == self.ax:
            if self.start_x is None:
                self.start_x = event.xdata
                self.start_y = event.ydata
                self.is_cropping = True
            else:
                self.end_x = event.xdata
                self.end_y = event.ydata
                self.crop_image()
                self.fig.canvas.mpl_disconnect(self.cid_press)  # Disconnect press event
                self.fig.canvas.mpl_disconnect(self.cid_move)   # Disconnect move event after cropping

    def on_move(self, event):
        if self.is_cropping:
            self.end_x = event.xdata
            self.end_y = event.ydata
            self.update_rectangle()

    def update_rectangle(self):
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        self.rect.set_xy((x, y))
        self.rect.set_width(width)
        self.rect.set_height(height)

        self.fig.canvas.draw()

    def crop_image(self):
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        image = plt.imread(self.image_path)
        cropped_image = image[int(y):int(y + height), int(x):int(x + width)]
        plt.imsave('out/cropped_image.png', cropped_image)
        # Display the cropped image
        plt.imshow(cropped_image)
        plt.close()


def capture_screen(screen_index,half):
    monitors = get_monitors()
    selected_monitor = monitors[screen_index]
    screen_width, screen_height = selected_monitor.width, selected_monitor.height
    print(f"half value {half} , {half==1}")
    max_screen_width, max_screen_height = pyautogui.size()

    if(half==1):
        screen_width= screen_width // 2
    capture_region = (0, 0, min(screen_width, max_screen_width), min(screen_height, max_screen_height))
    
    image = pyautogui.screenshot(region=capture_region)
    file_name = "out/output.png"
   
    image.save(file_name)
    return file_name

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

def draw_boxes(image, bounds, color):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
        )
    return image

def get_document_bounds(image_file, feature):
    client = vision.ImageAnnotatorClient()

    bounds = []

    with open(image_file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds, document.text

def render_doc_text(filein, fileout,file_name):
    image = Image.open(filein)
    bounds, extracted_text = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, "yellow")
    print("Extracted Text (WORD):", extracted_text)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(extracted_text)
   

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()
    return extracted_text
def cropAndSaveOut(half, image_path="out/output.png"):
    if image_path =="out/output.png":
        capture_screen(0,half)
    cropper = ImageCropper(image_path)
    return render_doc_text("out/cropped_image.png", "out/bounded.png","out/default.txt")

import time
def button1_click():
    print(check_mark_var_addScreen.get())
    if check_mark_var_addScreen.get() == False:
        text_edit.delete("1.0", tk.END)
    root.iconify()
    if check_mark_var.get():
        pyautogui.alert('Start screenshotProcess half screen')
        time.sleep(1)
    else:
        pyautogui.alert('Start screenshotProcess full  screen')
        time.sleep(1)
    text_edit.insert(tk.END,   cropAndSaveOut( check_mark_var.get()))
    root.deiconify()

def buttonAI_click():
    text_edit_out.delete("1.0", tk.END)
    print("qui non dovrei entrare mai")
    text_value = text_edit.get("1.0", tk.END)  # Recupera il valore del testo
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[

    {"role": "user","content": text_value}
    ]
)   
    for x in completion.choices:

        text_edit_out.insert(tk.END, x.message.content)
        text_edit_out.insert(tk.END,"""
                             
############################################
                             
""")
def button2_click():
    print(check_mark_var_addScreen.get())
    if check_mark_var_addScreen.get()== False:
        text_edit.delete("1.0", tk.END)
    text_edit.config(state=tk.NORMAL)
    # Apre una finestra di dialogo per la selezione di un file
    file_path = filedialog.askopenfilename(title="Seleziona un immagine", filetypes=[("immagine", "*.*")])
    text_edit.insert(tk.END,   cropAndSaveOut( check_mark_var.get(), image_path=file_path))

root = tk.Tk()
root.title("VisionCrop v0.1")
api_key= ""
# Set the environment variable
os.environ['OPENAI_API_KEY'] = api_key
client = OpenAI()
check_mark_var = tk.BooleanVar()
check_mark_var.set(False)
check_mark_var_addScreen = tk.BooleanVar()
check_mark_var_addScreen.set(False)
frame = tk.Frame(root)
frame.pack()
button1 = tk.Button(frame, text="ScreenShot", command=button1_click)
button1.pack(side=tk.LEFT, pady=10, padx=10)
button2 = tk.Button(frame, text="Load from File", command=button2_click)
button2.pack(side=tk.LEFT, pady=10, padx=10)
check_mark = tk.Checkbutton(frame, text="Half screen", variable=check_mark_var)
check_mark.pack(side=tk.LEFT, padx=10)
check_mark_1 = tk.Checkbutton(frame, text="append content", variable=check_mark_var_addScreen)
check_mark_1.pack(side=tk.LEFT, padx=10)
# Creazione del pulsante 2
text_edit = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10, state=tk.NORMAL)

text_edit.pack(pady=10)
text_edit_out = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10, state=tk.NORMAL)
text_edit_out.insert(tk.END,   "risposta AI")
text_edit_out.pack(pady=10)
button3 = tk.Button(frame, text="Ask to AI", command=buttonAI_click)
button3.pack(side=tk.LEFT, pady=10, padx=10)
# Esecuzione della finestra
root.mainloop()