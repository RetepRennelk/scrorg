#!python3.5
import os
import tkinter as tk  # This is Python 3.x. For Python 2.x import Tkinter
from PIL import Image, ImageTk, ImageGrab
from datetime import datetime, timezone

class ScrOrg(tk.Tk):
    '''
    Screenshot tool for Emacs' org-mode
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.bind_keys()
        self.attributes('-fullscreen', True)
        self.rect = None
        self.take_screenshot()
        self.focus_force()

    def take_screenshot(self):
        self.source_image = ImageGrab.grab()
        mask = Image.new("RGB", self.source_image.size, "gray")
        self.masked_image = Image.blend(self.source_image, mask, 0.65)
        self.tk_im = ImageTk.PhotoImage(self.masked_image)
        self.ci = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def bind_keys(self):
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<ButtonPress-3>", self.on_button_press3)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<Return>", self._save_segment)
        self.bind('<Escape>', self.close)

    def close(self, event):
        print("")
        self.destroy()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(0, 0, 1, 1, width=2.0, outline="red")

    def on_move_press(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

        bbox = self.canvas.bbox(self.rect)
        bbox_image = self.source_image.crop(bbox)

        masked_image = self.masked_image.copy()
        masked_image.paste(bbox_image, bbox)
        tk_im = ImageTk.PhotoImage(masked_image)
        self.canvas.itemconfig(self.ci, image=tk_im)
        self.tk_im = tk_im

    def _get_new_filename(self):
        utc = datetime.now(timezone.utc)  # UTC time
        now = utc.astimezone()  # local time
        filename = now.strftime('%Y-%m-%dT%H-%M-%S%z') + '.png'
        return filename

    def _save_segment(self, event):
        if self.rect:
            bbox = self.canvas.bbox(self.rect)
            bbox_image = self.source_image.crop(bbox)
            filename = self._get_new_filename()
            if not os.path.isdir('./img'):
                os.mkdir('./img')
            filename = './img/' + filename
            bbox_image.save(filename)
            print(filename)
            self.destroy()

    def on_button_press3(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

if __name__ == "__main__":
    app = ScrOrg()
    app.mainloop()
