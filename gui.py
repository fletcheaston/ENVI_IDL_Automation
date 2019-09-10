# Created by Fletcher Easton
from tkinter import *
import tkfilebrowser
import tkinter.filedialog
import sys
import settings
import time


class FlightDataRow:
    def __init__(self, root, path):
        self.root = root
        self.path = path
        settings.allFlightDirs.add(path)

        self.frame = Frame(root)
        self.frame.grid(columnspan=3, sticky=N+W) 
        self.close_button = Button(self.frame, text="Delete", font=settings.font, command=self.quit)
        self.close_button.grid(row=0, column=1, sticky=N)
        self.label = Label(self.frame, text=path, font=settings.font) 
        self.label.grid(row=0, column=2, columnspan=2, sticky=N)        
    
        # Configures the scrollbar to work with the textbox.
        #scrollbar.config(command=self.textbox.yview)

    
    def quit(self):
        settings.allFlightDirs.remove(self.path)
        self.frame.destroy()



# Allows the user to select multiple directories at once.
def askDirs():
    dirs = tkfilebrowser.askopendirnames(title="Select Flight Data", foldercreation=False)
    return(dirs)


# 
def addFlightData():
    global root
    dirs = askDirs()
    for dir in dirs:
        if(dir not in settings.allFlightDirs):
            settings.allFlightDataRows.append(FlightDataRow(root, dir))



#
def deleteFlightData():
    pass

# Allows the user to select a directory.
def askDir(title):
    root = tkinter.Tk()
    directory = tkfilebrowser.askopendirname(title=title, foldercreation=True)
    root.withdraw()
    if(directory == ""):
        tkinter.messagebox.showerror("Error", "No directory selected for saving data. Exiting program.")
        sys.exit(1)
    return(directory)


# Destroys the window and erases flight directory paths. 
# We can't system exit here, tkinter will throw some error.
def killAll():
    global root
    root.destroy()
    settings.allFlightDirs = []


def finish():
    global root
    root.destroy()
    settings.allFlightDirs = list(settings.allFlightDirs)

# Creates the main gui for selecting flight data directories.
def selectFlightData():
    global root
    root = Tk()
    root.resizable(False, False)
    root.title("Select Flight Data Directories")


    # Adds all of the buttons to the window.
    cancelButton = Button(root, text="Cancel", font=settings.font, command=killAll)
    cancelButton.grid(row=0, column=0, sticky=N)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    selectButton = Button(root, text="Add Flight Data", font=settings.font, command=addFlightData)
    selectButton.grid(row=0, column=1, sticky=N)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    confirmButton = Button(root, text="Done", font=settings.font, command=finish)
    confirmButton.grid(row=0, column=2, sticky=N)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Adds a vertical scrollbar.
    #global scrollbar
    #scrollbar = Scrollbar(root, orient=VERTICAL)
    #scrollbar.grid(row=2, column=3, sticky=N+S+E)
    
    #scrollbar.config(command=overallFrame.yview)



    root.wait_window(root)
