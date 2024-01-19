import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
from datetime import datetime
import threading





Image.MAX_IMAGE_PIXELS = None 





class ImageTileSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Tile Splitter")

        # Instance variables
        self.auto_create_dir = tk.BooleanVar()

        # Setup the GUI
        self.setup_gui()

    def setup_gui(self):
        # Image selection
        tk.Label(self.root, text="Image Path:").grid(row=0, column=0)
        self.entry_image_path = tk.Entry(self.root, width=50)
        self.entry_image_path.grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.select_image).grid(row=0, column=2)
        # progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        # Tile size inputs
        tk.Label(self.root, text="Tile Width:").grid(row=1, column=0)
        self.entry_tile_width = tk.Entry(self.root)
        self.entry_tile_width.grid(row=1, column=1)
        tk.Label(self.root, text="Tile Height:").grid(row=2, column=0)
        self.entry_tile_height = tk.Entry(self.root)
        self.entry_tile_height.grid(row=2, column=1)

        # Output directory selection
        tk.Label(self.root, text="Output Directory:").grid(row=3, column=0)
        self.entry_output_dir = tk.Entry(self.root, width=50)
        self.entry_output_dir.grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=lambda: self.entry_output_dir.insert(0, filedialog.askdirectory())).grid(row=3, column=2)

        # Checkbox for auto-creating output directory
        tk.Checkbutton(self.root, text="Auto-create Output Directory", variable=self.auto_create_dir).grid(row=4, column=0)

        # Split button
        tk.Button(self.root, text="Split Image", command=self.split_image).grid(row=4, column=1)

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, file_path)

    def split_image(self):
        image_path = self.entry_image_path.get()
        tile_width = int(self.entry_tile_width.get())
        tile_height = int(self.entry_tile_height.get())
        output_dir = self.entry_output_dir.get()
        threading.Thread(target=self.process_image, args=(image_path, tile_width, tile_height, output_dir), daemon=True).start()
        
       
    def process_image(self, image_path, tile_width, tile_height, output_dir):
        try:
            # Open the image and get its size
            image = Image.open(image_path)
            img_width, img_height = image.size

            total_tiles = (img_width // tile_width) * (img_height // tile_height)
            self.progress['maximum'] = total_tiles

            tile_number = 0
            for i in range(0, img_width, tile_width):
                for j in range(0, img_height, tile_height):
                    box = (i, j, i + tile_width, j + tile_height)
                    tile = image.crop(box)

                    # If auto-create directory is selected
                    if self.auto_create_dir.get() and tile_number == 0:
                        output_dir = os.path.join("output_tiles", datetime.now().strftime("%Y%m%d_%H%M%S"))
                        os.makedirs(output_dir, exist_ok=True)

                    tile_filename = f'tile_{tile_number}.png'
                    tile.save(os.path.join(output_dir, tile_filename))

                    # Update progress bar
                    tile_number += 1
                    self.update_progress(tile_number)

            messagebox.showinfo("Success", f"Image split into {tile_number} tiles successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def update_progress(self, value):
        def _update():
            self.progress['value'] = value
        self.root.after(0, _update)


            
# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTileSplitterApp(root)
    root.mainloop()
