import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
Image.MAX_IMAGE_PIXELS = None
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_image_path.delete(0, tk.END)
        entry_image_path.insert(0, file_path)

def split_image():
    image_path = entry_image_path.get()
    tile_width = int(entry_tile_width.get())
    tile_height = int(entry_tile_height.get())
    output_dir = entry_output_dir.get()

    # Ensure all inputs are provided
    if not (image_path and tile_width and tile_height and output_dir):
        messagebox.showerror("Error", "All fields are required")
        return

    # Split the image
    try:
        image = Image.open(image_path)
        img_width, img_height = image.size

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tile_number = 0
        for i in range(0, img_width, tile_width):
            for j in range(0, img_height, tile_height):
                box = (i, j, i + tile_width, j + tile_height)
                tile = image.crop(box)
                tile_filename = f'tile_{tile_number}.png'
                tile.save(os.path.join(output_dir, tile_filename))
                tile_number += 1
        
        messagebox.showinfo("Success", f"Image split into {tile_number} tiles successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Image Tile Splitter")

# Image selection
tk.Label(root, text="Image Path:").grid(row=0, column=0)
entry_image_path = tk.Entry(root, width=50)
entry_image_path.grid(row=0, column=1)
tk.Button(root, text="Browse", command=select_image).grid(row=0, column=2)

# Tile size inputs
tk.Label(root, text="Tile Width:").grid(row=1, column=0)
entry_tile_width = tk.Entry(root)
entry_tile_width.grid(row=1, column=1)
tk.Label(root, text="Tile Height:").grid(row=2, column=0)
entry_tile_height = tk.Entry(root)
entry_tile_height.grid(row=2, column=1)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=3, column=0)
entry_output_dir = tk.Entry(root, width=50)
entry_output_dir.grid(row=3, column=1)
tk.Button(root, text="Browse", command=lambda: entry_output_dir.insert(0, filedialog.askdirectory())).grid(row=3, column=2)

# Split button
tk.Button(root, text="Split Image", command=split_image).grid(row=4, column=1)

# Run the application
root.mainloop()
