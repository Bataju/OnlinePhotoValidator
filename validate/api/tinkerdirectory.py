import tkinter
from tkinter import filedialog
import os


def opendialogForDirectory(type):
    root = tkinter.Tk()
    currdir = os.getcwd()
    if type == 'folder':
        dirname = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')

    else:
        dirname = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title="Select file",
                                                     filetypes=[('all files', '.*'),

                                                                ('image files', ('.png', '.jpg','.JPG','.JPEG','.PNG')),
                                                                ]
                                                     )
    root.withdraw()
    
    return dirname
