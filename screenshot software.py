from tkinter import *
import pyautogui
import threading
import keyboard
import time
from PIL import ImageTk, Image, ImageDraw
from tkinter.filedialog import asksaveasfile


class notification:
    def __init__(self,master):
        self.master = master
        self.infoscreenshot()
        self.info = Label(self.master, text="Press 'Alt' on keyboard to take a screenshot!", font=("Arial", 25))
        self.info.pack()
    def infoscreenshot(self):
        def key_detect():
            while True:
                if keyboard.is_pressed("Alt"):
                    self.master.withdraw()
                    time.sleep(0.5)
                    root = Tk()
                    screenshotwindow(root)
                    root.mainloop()
                    break
        threading.Thread(target=key_detect).start()

class screenshotwindow:
    def __init__(self, master):
        self.master = master
        self.screenshot = None
        self.cords = [None,None]
        self.clicks = 0
        self.master.focus_force()
        self.topm = StringVar()
        self.topm.set("Click on the photo to make a blurring rectangle")
        self.blurtwindow()
        self.buttons()
    def buttons(self):
        self.clear = Button(master=self.master, command=self.clear, text="Clear all blurring rectangles")
        self.imgsave = Button(master=self.master, command=self.save, text="Save")
        self.newscreen = Button(master=self.master, command=self.new_screenshot, text="Take a new screenshot")
        self.clear.pack(side=BOTTOM)
        self.imgsave.pack(side=BOTTOM)
        self.newscreen.pack(side=BOTTOM)
    def new_screenshot(self):
        self.master.withdraw()
        root2 = Tk()
        notification(root2)
        root2.mainloop()
    def save(self):
        savefile = asksaveasfile(mode="w", filetypes = [("PNG IMAGE", "*.png")], defaultextension = [("PNG IMAGE", "*.png")])
        finalsave = savefile.name + ".png"
        img = Image.alpha_composite(self.screenshot,self.blank)
        img.save(finalsave)
    def clear(self):
        self.canv.delete("all")
        self.canv.create_image(0, 0, image=self.image, anchor=NW)
        self.blank = Image.new(mode="RGBA", size=(self.screenshot.size[0], self.screenshot.size[1]))
        self.draw = ImageDraw.Draw(self.blank)
    def cord(self,event):
        self.clicks += 1
        if self.clicks == 1:
            self.cords[0] = (event.x, event.y)
            self.info.config(text="First point set for blurring rectangle! Now click again to make the rectangle")
        if self.clicks == 2:
            self.clicks = 0
            self.info.config(text="Blurring rectangle set! click on the photo again for another one")
            self.cords[1] = (event.x, event.y)
            self.t = self.canv.create_rectangle(self.cords[0][0],self.cords[0][1], self.cords[1][0], self.cords[1][1], fill="black")
            self.draw.rectangle([(self.cords[0][0] * 1.3, self.cords[0][1] * 1.3), (self.cords[1][0] * 1.3, self.cords[1][1] * 1.3)], fill=(0,0,0))
    def blurtwindow(self):
        self.master.focus_force()
        self.info = Label(self.master, text = "Click on the photo to make a blurring rectangle", font=("Arial", 25))
        self.info.pack(side=TOP)
        self.screenshot = pyautogui.screenshot().convert("RGBA")
        self.blank = Image.new(mode="RGBA",size=(self.screenshot.size[0], self.screenshot.size[1]))
        self.draw = ImageDraw.Draw(self.blank)
        self.canv = Canvas(self.master, width=int(self.screenshot.size[0] / 1.3), height=int(self.screenshot.size[1] / 1.3), bg="white")
        self.canv.pack(fill=BOTH)
        self.resized_image = self.screenshot.resize((int(self.screenshot.size[0] / 1.3),int(self.screenshot.size[1] / 1.3)), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(master=self.canv, image=self.resized_image, width=100, height=100)
        self.canv.create_image(0,0,image=self.image,anchor=NW)
        self.canv.bind("<Button-1>", self.cord)


root2 = Tk()
notification(root2)
root2.mainloop()