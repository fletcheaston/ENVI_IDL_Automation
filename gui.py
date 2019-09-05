# Created by Fletcher Easton
from tkinter import *
import tkfilebrowser
import tkinter.filedialog
import sys
import settings


class Redir(object):
    # This is what we're using for the redirect, it needs a text box
    def __init__(self, textbox):
        self.textbox = textbox
        self.textbox.config(state=NORMAL)
        self.fileno = sys.stdout.fileno

    def write(self, message):
        # When you set this up as redirect it needs a write method as the
        # stdin/out will be looking to write to somewhere!
        self.textbox.insert(END, str(message))


# Gets the text from the textbox and puts it into a list. Redirects output to the system stdout.
def retrieveInput():
    global textbox
    input = textbox.get("1.0","end-1c")
    settings.allFlightDirs = input.strip(" \n").split("\n")
    global root
    root.destroy()
    sys.stdout = sys.__stdout__


# Allows the user to select multiple directories at once.
def askDirs():
    dirs = tkfilebrowser.askopendirnames(title="Select Flight Data", foldercreation=False)
    return(dirs)


# Allows the user to select a directory.
def askDir(title):
    root = tkinter.Tk()
    directory = tkfilebrowser.askopendirname(title=title, foldercreation=True)
    root.withdraw()
    if(directory == ""):
        tkinter.messagebox.showerror("Error", "No directory selected for saving data. Exiting program.")
        sys.exit(1)
    return(directory)


# Prints the dirs to stdout.
def printDirs():
    dirs = askDirs()
    for dir in dirs:
        if(dir not in settings.allFlightDirs):
            print(dir)
            settings.allFlightDirs.add(dir)


# Destroys the window and erases flight directory paths. 
# We can't system exit here, tkinter will throw some error.
def killAll():
    global root
    root.destroy()
    settings.allFlightDirs = []


# Creates the main gui for selecting flight data directories.
def selectFlightData():
    font = ("Helvetica", 16)
    global root
    root = Tk()
    root.title("Select Flight Data Directories")

    # Adds all of the buttons to the window.
    cancelButton = Button(root, text="Cancel", font=font, command=killAll)
    cancelButton.grid(row=1, column=0)
    selectButton = Button(root, text="Select Flight Data", font=font, command=printDirs)
    selectButton.grid(row=1, column=1)
    confirmButton = Button(root, text="Done", font=font, command=retrieveInput)
    confirmButton.grid(row=1, column=2)

    # Adds a vertical scrollbar.
    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.grid(row=2, column=3, sticky=N+S+E)

    # Adds the textbox for file paths.
    global textbox
    textbox = Text(root, font=font, state=NORMAL, yscrollcommand=scrollbar.set, wrap=WORD)
    textbox.grid(row=2, column=0, columnspan=3, sticky=N+S+W+E)

    # Configures the scrollbar to work with the textbox.
    scrollbar.config(command=textbox.yview)

    # Redirect stdout and stderr, where the standard messages are ouput.
    stdre = Redir(textbox)
    sys.stdout = stdre
    sys.stderr = stdre

    root.wait_window(root)
