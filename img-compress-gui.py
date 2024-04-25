import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os
from PIL import Image, ImageTk
import io

VERSION = "v1.0.0"

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        panel_image.original_image = ImageTk.PhotoImage(img)
        panel_image.config(image=panel_image.original_image)
        panel_image.file_path = file_path

def size_format(size):
    size = int(size)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return size

def server_addr():
    if not entry_server_addr.get().strip():
        messagebox.showerror("Error", "Please enter the server address!")
        return
    return entry_server_addr.get().strip()

def compress_and_download():
    if not hasattr(panel_image, 'file_path'):
        messagebox.showerror("Error", "Please select an image first!")
        return

    compression_quality = var_compression_quality.get()
    if compression_quality not in ["Light (better quality)", "Medium (good quality)", "High (quality ok)", "Extreme (terrible quality)"]:
        messagebox.showerror("Error", "Please select a compression quality!")
        return
    
    if compression_quality == "Light (better quality)":
        compression_quality = "Light"
    elif compression_quality == "Medium (good quality)":
        compression_quality = "Medium"
    elif compression_quality == "High (quality ok)":
        compression_quality = "High"
    elif compression_quality == "Extreme (terrible quality)":
        compression_quality = "Fat"

    files = {'file': open(panel_image.file_path, 'rb')}
    response = requests.post(server_addr(), files=files, params={'quality': compression_quality})
    
    if response.status_code == 200:
        compressed_size = size_format(response.headers.get('X-Compressed-Size'))
        original_size = size_format(response.headers.get('X-Original-Size'))
        compression_ratio = response.headers.get('X-Compression-Ratio-Percent')

        info_debug_quality.config(text=f"Quality: {response.headers.get('X-Compression-Quality')} %")
        info_debug_method.config(text=f"Method: {response.headers.get('X-Compression-Method')}")
        info_debug_platform_exec_time.config(text=f"Platform Exec Time: {response.headers.get('X-Compression-Execution-Time')}")
        info_debug_platform.config(text=f"Platform: {response.headers.get('X-Compression-Platform')}")
        info_debug_platform_version.config(text=f"Platform Version: {response.headers.get('X-Compression-Platform-Version')}")
        info_debug_processor_name.config(text=f"Processor Name: {response.headers.get('X-Processor-Processor-Name')}")
        
        label_info.config(text=f"Original Size: {original_size} bytes\n"
                               f"Compressed Size: {compressed_size} bytes\n"
                               f"Compression Ratio: {compression_ratio}")

        # Load the compressed image and display it
        compressed_img = Image.open(io.BytesIO(response.content))
        compressed_img.thumbnail((300, 300))
        panel_image.compressed_image = ImageTk.PhotoImage(compressed_img)
        panel_image.config(image=panel_image.compressed_image)

        # Save the compressed image
        file_name = os.path.basename(panel_image.file_path)
        file_name_no_ext, file_extension = os.path.splitext(file_name)
        new_file_name = file_name_no_ext + "-compressed" + file_extension

        output_path = filedialog.asksaveasfilename(defaultextension=file_extension,
                                                   filetypes=[("Image files", f"*{file_extension}")],
                                                   initialfile=new_file_name,
                                                   initialdir=os.path.dirname(panel_image.file_path))
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            messagebox.showinfo("Success", "Image compressed and saved successfully!")
    else:
        messagebox.showerror("Error", "Failed to compress the image! Please check the server address.")

# GUI Setup
root = tk.Tk()
root.title("Image Compressor " + VERSION)

label_server_addr = tk.Label(root, text="Server Address:")
label_server_addr.pack(pady=5, padx=10)
entry_server_addr = tk.Entry(root, width=50, textvariable=tk.StringVar(value="https://imgc1.col-pro.net/compress"))
entry_server_addr.pack(pady=5, padx=10)

label_compress_quality = tk.Label(root, text="Compression Quality:")
label_compress_quality.pack(pady=5, padx=10)

var_compression_quality = tk.StringVar(root)
var_compression_quality.set("Light")

option_menu = tk.OptionMenu(root, var_compression_quality, "Light (better quality)", "Medium (good quality)", "High (quality ok)", "Extreme (terrible quality)")
option_menu.pack(pady=5, padx=10)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

btn_open = tk.Button(frame, text="Open Image", command=open_file)
btn_open_label = tk.Label(frame, text="Input/Output Image")
btn_open.pack(fill=tk.X)

panel_image = tk.Label(frame)
panel_image.pack(pady=10)

btn_compress = tk.Button(frame, text="Compress and Download", command=compress_and_download)
btn_compress.pack(fill=tk.X)

label_info = tk.Label(frame, text="No compression data yet.")
label_info.pack(pady=10)

label_debug_info = tk.Label(frame, text="Debug Information:")
label_debug_info.pack(anchor="w", padx=1)

info_debug_quality = tk.Label(frame, text="Quality: ")
info_debug_quality.pack(anchor="w", padx=1)

info_debug_method = tk.Label(frame, text="Method: ")
info_debug_method.pack(anchor="w", padx=1)

info_debug_platform_exec_time = tk.Label(frame, text="Platform Exec Time: ")
info_debug_platform_exec_time.pack(anchor="w", padx=1)

info_debug_platform = tk.Label(frame, text="Platform: ")
info_debug_platform.pack(anchor="w", padx=1)

info_debug_platform_version = tk.Label(frame, text="Platform Version: ")
info_debug_platform_version.pack(anchor="w", padx=1)

info_debug_processor_name = tk.Label(frame, text="Processor Name: ")
info_debug_processor_name.pack(anchor="w", padx=1)

root.mainloop()
