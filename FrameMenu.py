from customtkinter import CTkFrame, CTkButton, CTkLabel
from FrameServer import createLoadFile
from FrameClient import createSearchServer

def createMenu(self):
    frameMenu = self.frameMenu = CTkFrame(self.root)
    frameMenu.pack(pady=10, padx=10, fill='both', expand=True)  
    frameMenu.pack_propagate(False)
    
    # Label for the title
    title = CTkLabel(frameMenu, text="Choice an option", font=("Arial", 18))
    title.pack(pady=(25, 10))
    
    # Button share file
    buttonShareFile = CTkButton(frameMenu, font=('Arial', 14), text="Share file", command=lambda: createLoadFile(self))
    buttonShareFile.pack(pady=20, padx=20, fill="x", ipady=5)
    
    # Button receive file
    buttonReceiveFile = CTkButton(frameMenu, font=('Arial', 14), text="Receive file", command=lambda: createSearchServer(self))
    buttonReceiveFile.pack(padx=20, fill="x", ipady=5)