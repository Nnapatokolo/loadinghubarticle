from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def resize_image(input_path, output_dir, sizes):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the original image
    with Image.open(input_path) as img:
        for size in sizes:
            # Resize the image
            resized_img = img.resize(size, Image.LANCZOS)
            
            # Define the output path
            size_str = f"{size[0]}x{size[1]}"
            output_path = os.path.join(output_dir, f"resized_image_{size_str}.jpg")
            
            # Save the resized image
            resized_img.save(output_path)
            print(f"Image resized to {size_str} and saved to {output_path}")

def select_file_and_resize():
    input_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if not input_path:
        return
    
    output_dir = filedialog.askdirectory()
    if not output_dir:
        return
    
    sizes = [
        (640, 480),  # Size 1
        (800, 600),  # Size 2
        (1024, 768), # Size 3
        (1280, 720), # Size 4
        (1920, 1080),# Size 5
        (2048, 1536),# Size 6
        (3840, 2160) # Size 7
    ]

    try:
        resize_image(input_path, output_dir, sizes)
        messagebox.showinfo("Success", "Images resized and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Main code
if __name__ == "__main__":
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()

    select_file_and_resize()
