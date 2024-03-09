from customtkinter import CTk, CTkFrame
from FrameMenu import createMenu

class menu:
    port = 12345
    
    def __init__(self):
        self.root = CTk()
        self.root.title("File sharer")
        self.root.geometry("500x230")
        self.root.resizable(False, False)
        
        createMenu(self)
    
    
    def toMenu(self):
        for widget in self.root.winfo_children():
            print(widget)
            if isinstance(widget, CTkFrame) and widget != self.frameMenu:
                widget.destroy()
                     
        self.frameMenu.pack(pady=10, padx=10, fill='both', expand=True)
    
    def toNext(self, frameCurrent: CTkFrame, frameNext: CTkFrame):
        frameCurrent.pack_forget()
        frameNext.pack(pady=10, padx=10, fill='both', expand=True)
    
    def toBack(self, frameCurrent: CTkFrame, framePrevious: CTkFrame):
        frameCurrent.destroy()
        framePrevious.pack(pady=10, padx=10, fill='both', expand=True)
    
    def run(self):
        self.root.mainloop()
     
menu().run()       
