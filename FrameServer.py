from customtkinter import CTkFrame, CTkButton, CTkLabel
from tkinter import filedialog, messagebox
import os, socket, threading

def createLoadFile(self):
    frameLoadFile = self.frameLoadFile = CTkFrame(self.root)
    self.toNext(self.frameMenu, frameLoadFile)
    
    title = CTkLabel(frameLoadFile, text="Share mode", font=("Arial", 18))
    title.pack(pady=(10, 10))
    
    file_path = ""
    def shareFileRoute():
        nonlocal file_path
        file_path = filedialog.askopenfilename()
        file_name = file_path.split("/")[-1]
        if file_path:
            buttonLoadFile.configure(text=file_name)
        else:
            buttonLoadFile.configure(text="Click here to selesct a file")
        buttonConfirmFile.configure(state='normal' if file_path else 'disabled')
       
    # Button load file 
    buttonLoadFile = CTkButton(frameLoadFile, font=('Arial', 14), text="Click here to selesct a file", command=lambda: shareFileRoute())
    buttonLoadFile.pack(padx=10, expand=True, fill="x", ipady=5) 
    
    # Button back file
    buttonBack = CTkButton(frameLoadFile, font=('Arial', 14), text="< Back", command=lambda: self.toBack(frameLoadFile, self.frameMenu))
    buttonBack.pack(side='left', padx=10, ipady=5)
    
    # Button share file now
    buttonConfirmFile = CTkButton(frameLoadFile, font=('Arial', 14), text="Send ✔️", command=lambda: createServer(self, file_path), state='disabled')
    buttonConfirmFile.pack(side='right', pady=10, padx=10, ipady=5)
    

def createServer(self, file_path: str):
    frameServer = self.frameServer = CTkFrame(self.root)
    self.toNext(self.frameLoadFile, frameServer)
    
    labelTitle = CTkLabel(frameServer, text="", font=("Arial", 18))
    labelTitle.pack(pady=(15, 0), fill='x', ipady=5)
    
    labelInfo = CTkLabel(frameServer, text="Waiting connections...", font=("Arial", 14))
    labelInfo.pack(pady=(25, 10), fill='x')
    
    searchConnections_stop = False
    def cancel():
        nonlocal searchConnections_stop 
        searchConnections_stop = True
        self.toBack(frameServer, self.frameLoadFile)

    buttonCancel = CTkButton(frameServer, font=('Arial', 14), text="✖️ Cancel", command=lambda: cancel())
    buttonCancel.pack(side="bottom", pady=15, padx=10, ipady=5)
    
    host = socket.gethostbyname(socket.gethostname())
    labelTitle.configure(text=f"{socket.gethostname()} your IP is: {host}")
    
    
    def searchConnections(s):
        try:
            # Function to start the server        
            s.settimeout(1) 
            s.bind((host, self.port))
            s.listen()

            while True:
                try:
                    conn, address = s.accept()
                except socket.timeout:
                    if searchConnections_stop == True:
                        break
                    else:
                        continue
                
                host_name = conn.recv(1024).decode()
            
                res = messagebox.askyesno("Connection", f"Accept the connection from {host_name} ({address[0]})?")
                if res == True:
                    buttonCancel.configure(state='disabled')
                    labelInfo.configure(text=f"Sending file to {host_name} ({address[0]})")
                    
                    conn.send("1".encode())
                    
                    # Send the name file
                    file = open(file_path, 'rb')
                    conn.send(file_path.split("/")[-1].encode())
                    
                    # Send the file size
                    file_size = str( os.path.getsize(file.name)/1024 ) + ' KB'
                    conn.send(file_size.encode())
                    
                    # Send the file
                    conn.sendall(file.read())
                    
                    file.close()
                    conn.close()
                    
                    buttonCancel.configure(state='normal')
                    labelInfo.configure(text="The file was send succesfully")
                    buttonCancel.configure(text="Go to menu", command=lambda: self.toMenu())
                    break
                else:
                    conn.send("0".encode())
                    conn.close()
            
            s.close()          
        except Exception as e:
            messagebox.showerror("An error occurred", f"An error occurred: {e}")
          
    # Start the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threading.Thread(target=searchConnections, args=(s,)).start()
       