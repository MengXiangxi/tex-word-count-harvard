from main import read_cfg, main
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import os
import re
import webbrowser

window = tk.Tk()
window.title("tex-word-count-harvard")
window.geometry("500x220")

config_path = "config"
with open(config_path, "rt") as f:
    lines = f.read().split(os.linesep)
for each_line in lines:
    m = re.match(r"Version:(.+)", each_line)
    if m:
        version = m.group(1)
        break


def import_cfg(config_path):
    global entry_tex, entry_bib
    tex_path, bib_path = read_cfg(config_path)
    entry_tex.insert(0, tex_path)
    entry_bib.insert(0, bib_path)


def refresh_entries():
    global tex_path, bib_path, entry_tex, entry_bib
    entry_tex.delete(0, "end")
    entry_bib.delete(0, "end")
    entry_tex.insert(0, tex_path)
    entry_bib.insert(0, bib_path)


def read_entries():
    global tex_path, bib_path, entry_tex, entry_bib
    tex_path = entry_tex.get()
    bib_path = entry_bib.get()


def save_entries():
    global entry_tex, entry_bib, config_path
    tex_path = entry_tex.get()
    bib_path = entry_bib.get()
    template = '''tex path = %s
bib path = %s

# Please note that your path cannot contain spaces.


##### Do not modify anything below #####
Version: 1.0
Date: 2018-05-07
'''
    content = template % (tex_path, bib_path)
    with open(config_path, "wt") as f:
        f.write(content)


def ask_path_tex():
    global tex_path
    tex_path = tkinter.filedialog.askopenfilename(title = "Select tex file", filetypes = (("tex files","*.tex"),("all files","*.*")))
    refresh_entries()


def ask_path_bib():
    global bib_path
    bib_path = tkinter.filedialog.askopenfilename(title = "Select bib file", filetypes = (("bib files","*.bib"),("all files","*.*")))
    refresh_entries()


def click_for_wc():
    global result, string_button_wc, tex_path, bib_path
    read_entries()
    try:
        wc_result = main(tex_path, bib_path)
        result.set(wc_result)
        string_button_wc.set("Refresh the word count")
    except FileNotFoundError:
        tkinter.messagebox.showerror(title="File Not Found", \
        message="\nFile not found! \nPlease ensure you enter the correct path. ")


# <!--------------- Frame: Settings --------------->
frame_settings = tk.Frame(window)
frame_settings.pack()

# line for tex
button_tex = tk.Button(frame_settings, 
    text="tex", 
    width=4,height=1, 
    command=ask_path_tex)
button_tex.grid(row=0, column=0)

entry_tex = tk.Entry(frame_settings, show=None, width=45)
entry_tex.grid(row=0, column=1)


# line for bib
button_bib = tk.Button(frame_settings, 
    text="bib", 
    width=4,height=1, 
    command = ask_path_bib)
button_bib.grid(row=1, column=0)

entry_bib = tk.Entry(frame_settings, show=None, width=45)
entry_bib.grid(row=1, column=1)

# button: click to save paths
button_cfg = tk.Button(frame_settings, 
    text="Save", 
    width=4,height=1, 
    command = save_entries)
button_cfg.grid(row=2, column=0)

# button: click to count words
string_button_wc = tk.StringVar()
string_button_wc.set("Print the word count")
button_wc = tk.Button(frame_settings, 
    textvariable=string_button_wc, 
    width=43,height=1, 
    command = click_for_wc)
button_wc.grid(row=2, column=1)


# <!--------------- Frame: Word count --------------->
frame_wc = tk.Frame(window)
frame_wc.pack()

# Show the result of word count
result = tk.StringVar()
label_wc = tk.Label(frame_wc, 
    textvariable = result, 
    borderwidth = 2, 
    relief="groove", 
    font=("Arial", 14), 
    width=59, height=6)
label_wc.grid(row=0, column=0)

# footer
# footer = tk.Label(frame_wc, text = "https://github.com/xudong-yang/tex-word-count-harvard")
# footer.grid(row=4, column=0,columnspan=2)


# <!--------------- Menu bar --------------- >
menubar = tk.Menu(window)


def about():
    tkinter.messagebox.showinfo(title="About", \
    message="\ntex-word-count-harvard\nXudong Yang\n")


# File
menu_file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=menu_file)
menu_file.add_command(label="Import from Config", command=refresh_entries)
menu_file.add_command(label="Save to Config", command=save_entries)
menu_file.add_separator()
menu_file.add_command(label="Exit", command=window.destroy)

# Edit

# text_editor.pack_forget()
menu_edit = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=menu_edit)
menu_edit.add_command(label="Cut")

# Use CLI via os.system()
# Windows: echo "content" | clip
# Mac OS:  echo "content" | pbcopy
# Linux:   echo "content" | xsel


# Help
menu_help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=menu_help)
about_text = '''
tex-word-count-harvard

Version : %s
Author: Xudong Yang
''' % (version)
menu_help.add_command(label="About", command=lambda title="About": tkinter.messagebox.showerror(title=title, message=about_text))
menu_help.add_command(label="View Source on GitHub", command=lambda url="https://github.com/xudong-yang/tex-word-count-harvard": webbrowser.open_new(url))

window.config(menu=menubar)

import_cfg("config")
window.mainloop()