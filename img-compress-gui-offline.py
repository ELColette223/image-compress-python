import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Function to compress the image locally
def compress_image(image_path, quality):
    image = Image.open(image_path)
    output_path = os.path.splitext(image_path)[0] + "-compressed.jpg"
    image.save(output_path, quality=quality)
    return output_path

# Function to open an image file
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        panel_image.original_image = ImageTk.PhotoImage(img)
        panel_image.config(image=panel_image.original_image)
        panel_image.file_path = file_path

# Function to save the compressed image
def save_compressed_image(compressed_img, original_format):
    initial_dir = os.path.dirname(panel_image.file_path) if hasattr(panel_image, 'file_path') else os.getcwd()
    
    default_filename = os.path.splitext(os.path.basename(panel_image.file_path))[0] + "-compressed." + original_format
    save_path = filedialog.asksaveasfilename(defaultextension=f".{original_format}", initialdir=initial_dir, initialfile=default_filename)

    if save_path:
        save_path = os.path.splitext(save_path)[0] + "-compressed." + original_format
        compressed_img.save(save_path)
        return save_path
    
    return None

# Function to format the size in bytes
def size_format(size):
    size = int(size)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return size

# Function to compress and download the image
def compress_and_save():
    if not hasattr(panel_image, 'file_path'):
        messagebox.showerror("Error", "Please select an image first!")
        return

    quality_str = var_compression_quality.get()
    quality = 80

    print(quality_str)

    if quality_str == "Light (better quality)":
        quality = 80
    elif quality_str == "Medium (good quality)":
        quality = 67
    elif quality_str == "High (quality ok)":
        quality = 48
    else:
        quality = 14

    compressed_path = compress_image(panel_image.file_path, quality)
    
    # Get the original image format
    original_format = panel_image.file_path.split('.')[-1]

    # Calculate file sizes
    original_size = os.path.getsize(panel_image.file_path)
    compressed_size = os.path.getsize(compressed_path)

    # Calculate compression ratio
    compression_ratio_percent = 100 - (compressed_size * 100 / original_size)

    # Update the interface with compression data
    label_info.config(text=f"Original Size: {size_format(original_size)} bytes\n"
                           f"Compressed Size: {size_format(compressed_size)} bytes\n"
                           f"Compression Ratio: {compression_ratio_percent:.2f} %")

    # Save the compressed image in the same format
    compressed_image = Image.open(compressed_path)
    saved_path = save_compressed_image(compressed_image, original_format)

    if saved_path:
        label_info_save.config(text=f"Image compressed successfully and saved to path!")
        label_info_save_path.config(text=f"Saved Path: {saved_path}")
    else:
        label_info_save.config(text="Failed to save compressed image")

# GUI configuration
root = tk.Tk()
root.title("Image Compressor")

label_compress_quality = tk.Label(root, text="Compression Quality:")
label_compress_quality.pack(pady=5, padx=10)

var_compression_quality = tk.StringVar(root)
var_compression_quality.set("High (quality ok)")

option_menu = tk.OptionMenu(root, var_compression_quality, "Light (better quality)", "Medium (good quality)", "High (quality ok)", "Extreme (terrible quality)")
option_menu.pack(pady=5, padx=10)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

btn_open = tk.Button(frame, text="Open Image", command=open_file)
btn_open_label = tk.Label(frame, text="Input/Output Image")
btn_open.pack(fill=tk.X)

panel_image = tk.Label(frame)
panel_image.pack(pady=10)

btn_compress = tk.Button(frame, text="Compress and Download", command=compress_and_save)
btn_compress.pack(fill=tk.X)

label_info = tk.Label(frame, text="No compression data yet.")
label_info.pack(pady=10)

label_info_save = tk.Label(frame, text="No save data yet.")
label_info_save.pack(pady=10)

label_info_save_path = tk.Label(frame, text="")
label_info_save_path.pack(pady=10)

root.mainloop()
