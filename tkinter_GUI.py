
import tkinter as tk
from tkinter import messagebox as mb
import customtkinter as ctk
import numpy as np


try:
    # Bypassing the unicode escape error by reading clean formatting
    D = np.load('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/data.npy', allow_pickle=True)[0]
except Exception:
    # Fallback structure if the data file doesn't exist yet
    D = {}

opened = None

# --- CONFIGURE THEME ENGINE ---
ctk.set_appearance_mode("Dark")    
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("750x550")
root.minsize(650, 480)
root.title("AI Code Reviewer Workspace")

# CORE FUNCTIONAL LOGIC

def go(tops2, filename_entry):
    global opened
    filename = filename_entry.get().strip()
    
    if filename == '':
        mb.showwarning("Warning", "Can't accept this file name / filename is empty")
        return
        
    if len(D.keys()) >= 20:
        mb.showwarning('Warning', 'You have exceeded the maximum of 20 files. Please delete some.')
        return
        
    if filename in D.keys():
        response = mb.askquestion('Warning', 'This file name has been used. Do you want to overwrite it?')
        if response == 'yes':
            opened = filename
            texts = program.get('1.0', 'end-1c')
            D[opened] = texts.split()
            tops2.destroy()
            la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))
            np.save('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/data.npy', np.array([D]))
            rebuild_menus()
    else:
        opened = filename
        texts = program.get('1.0', 'end-1c')
        D[opened] = texts.split()
        tops2.destroy()
        la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))
        np.save('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/data.npy', np.array([D]))
        rebuild_menus()

def saveas():
    tops2 = ctk.CTkToplevel(root)
    tops2.title("Save As")
    tops2.geometry("380x180")
    tops2.attributes("-topmost", True) # Keep alert window on top
    
    lbl_info = ctk.CTkLabel(
        tops2, 
        text='This is saved as appdata and not as a raw text file.\nNote: Only 20 entries can be kept safe.',
        wraplength=320,
        justify="center"
    )
    lbl_info.pack(pady=(15, 10))
    
    entry_frame = ctk.CTkFrame(tops2, fg_color="transparent")
    entry_frame.pack(fill="x", padx=20, pady=5)
    
    lbl_name = ctk.CTkLabel(entry_frame, text='Enter name:', font=('Sans-Serif', 13))
    lbl_name.pack(side="left", padx=(10, 10))
    
    filename = ctk.CTkEntry(entry_frame, width=200, placeholder_text="my_dataset_v1")
    filename.pack(side="left", fill="x", expand=True)
    
    btn_go = ctk.CTkButton(tops2, text='Go', width=100, command=lambda: go(tops2, filename))
    btn_go.pack(pady=(15, 10))

def save(opened_file):
    if opened_file not in D.keys() or opened_file is None:
        mb.showinfo('Warning', 'Try "Save As" with a valid unique file name first.')
    else:
        D[opened_file] = program.get('1.0', 'end-1c').split()
        np.save('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/data.npy', np.array([D]))
        output_box.configure(state="normal")
        output_box.insert("end", f"\n[System]: Progress autosaved safely for '{opened_file}'")
        output_box.configure(state="disabled")

def start():
    global opened
    if opened is not None:
        if opened not in D.keys():
            re = mb.askquestion('Warning', 'Save current file before creation of a new instance?')
            if re == 'no':
                opened = 'file 1'
                la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))
                program.delete('1.0', 'end')
                clear_output()
        else:
            opened = 'file 1'
            la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))
            program.delete('1.0', 'end')
            clear_output()
    else:
        opened = 'file 1'
        la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))
        program.delete('1.0', 'end')
        clear_output()

def load(k):
    global opened
    opened = k
    program.delete('1.0', 'end')
    texts = D[k]
    # Build loaded block seamlessly
    program.insert('end', " ".join(texts))
    la.configure(text=f"Active: {opened}", font=('Sans-Serif', 11, 'bold'))

def remove(k):
    global opened
    resp = mb.askquestion("Confirm", f"Do you permanently want to delete workspace entry: {k}?")
    if resp == 'yes':
        if opened == k:
            program.delete('1.0', 'end')
            clear_output()
            la.configure(text="No instance open", font=('Sans-Serif', 11, 'italic'))
            opened = None
        if k in D:
            del D[k]
        np.save('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/data.npy', np.array([D]))
        rebuild_menus()

def clear_output():
    output_box.configure(state="normal")
    output_box.delete('1.0', 'end')
    output_box.insert("1.0", "System ready. Load an instance or click run...")
    output_box.configure(state="disabled")

# APP LAYOUT ARCHITECTURE

# 1. Top Control Bar
top_bar = ctk.CTkFrame(root, height=50, corner_radius=0)
top_bar.pack(fill="x", side="top", ipady=5)

startbtn = ctk.CTkButton(
    top_bar, 
    text='➕  Create New Instance', 
    font=('Sans-Serif', 12, 'bold'),
    fg_color="#3B7597", 
    hover_color="#4B5694",
    command=start
)
startbtn.pack(side="left", padx=20, pady=10)

# Main container for inputs/outputs
workspace_frame = ctk.CTkFrame(root, fg_color="transparent")
workspace_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

workspace_frame.columnconfigure(0, weight=1, uniform="group1")
workspace_frame.columnconfigure(1, weight=1, uniform="group1")
workspace_frame.rowconfigure(1, weight=1) # Makes editing text environment take up rest of row window

#  Sub Header controls
header_left = ctk.CTkFrame(workspace_frame, fg_color="transparent")
header_left.grid(row=0, column=0, sticky='ew', pady=(0, 10))

la = ctk.CTkLabel(header_left, text="No instance open", font=('Sans-Serif', 11, 'italic'), text_color="#a1a1aa")
la.pack(side='left', anchor='w')

btrun = ctk.CTkButton(
    workspace_frame, 
    text='▶  Run Program', 
    font=('Sans-Serif', 11, 'bold'), 
    fg_color="#3B7597", 
    hover_color="#4B5694"
)
btrun.grid(row=0, column=1, sticky='e', pady=(0, 10))

# Code Fields Layout
# Input Field
input_container = ctk.CTkFrame(workspace_frame)
input_container.grid(row=1, column=0, sticky='nsew', padx=(0, 10))

la1 = ctk.CTkLabel(input_container, text='INPUT DATASET / PROMPT CONTEXT', font=('Sans-Serif', 10, 'bold'), text_color="#a1a1aa")
la1.pack(anchor="w", padx=15, pady=(10, 5))

program = ctk.CTkTextbox(input_container, font=('Consolas', 12), border_width=1, border_color="#3f3f46")
program.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# Output Field
output_container = ctk.CTkFrame(workspace_frame)
output_container.grid(row=1, column=1, sticky='nsew', padx=(10, 0))

la2 = ctk.CTkLabel(output_container, text='OUTPUT CONSOLE / METRIC RESULTS', font=('Sans-Serif', 10, 'bold'), text_color="#a1a1aa")
la2.pack(anchor="w", padx=15, pady=(10, 5))

output_box = ctk.CTkTextbox(output_container, font=('Consolas', 12), border_width=1, border_color="#3f3f46", text_color="#a1a1aa")
output_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# Lock initial console text output state
output_box.insert("1.0", "System ready. Load an instance or click run...")
output_box.configure(state="disabled")

# MENUBAR SYSTEM BUILDER

menu = tk.Menu(root)
saved = tk.Menu(menu, tearoff=0)
delete = tk.Menu(menu, tearoff=0)
filemenu = tk.Menu(menu, tearoff=0)

menu.add_cascade(label='Load', menu=saved)
menu.add_cascade(label='Delete', menu=delete)
menu.add_cascade(label='File', menu=filemenu)
root.config(menu=menu)

def rebuild_menus():
    saved.delete(0, 'end')
    delete.delete(0, 'end')
    filemenu.delete(0, 'end')
    
    for k in D.keys():
        saved.add_command(label=str(k), command=lambda k=k: load(k))
    for k in D.keys():
        delete.add_command(label=str(k), command=lambda k=k: remove(k))
        
    filemenu.add_command(label='Save As', command=saveas)
    filemenu.add_command(label='Save', command=lambda: save(opened))

rebuild_menus()

try:
    root.iconbitmap('C:/Users/rosee/OneDrive/Desktop/LLM finetuning/rose.ico')
except Exception:
    pass 

root.mainloop()