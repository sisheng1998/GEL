# Folder Name: Great Eastern Life
# Place folder at the same directory with this file

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
import os.path
from os import path

FONT= ("Verdana", 12)
SMALL_FONT= ("Verdana", 8)

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
            self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
            self._hits = []
            self._hit_index = 0
            self.position = 0
            self.bind('<KeyRelease>', self.handle_keyrelease)
            self['values'] = self._completion_list

    def autocomplete(self, delta=0):
            """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
            if delta:
                    self.delete(self.position, tk.END)
            else:
                    self.position = len(self.get())

            _hits = []
            for element in self._completion_list:
                    if element.lower().startswith(self.get().lower()): # Match case insensitively
                            _hits.append(element)

            if _hits != self._hits:
                    self._hit_index = 0
                    self._hits=_hits

            if _hits == self._hits and self._hits:
                    self._hit_index = (self._hit_index + delta) % len(self._hits)

            if self._hits:
                    self.delete(0,tk.END)
                    self.insert(0,self._hits[self._hit_index])
                    self.select_range(self.position,tk.END)

    def handle_keyrelease(self, event):

            if event.keysym == "BackSpace":
                    self.delete(self.index(tk.INSERT), tk.END)
                    self.position = self.index(tk.END)
            if event.keysym == "Left":
                    if self.position < self.index(tk.END):
                            self.delete(self.position, tk.END)
                    else:
                            self.position = self.position-1
                            self.delete(self.position, tk.END)
            if event.keysym == "Right":
                    self.position = self.index(tk.END)
            if len(event.keysym) == 1:
                    self.autocomplete()

global createCustomerFolder
def createCustomerFolder(name, policy_no):
    path = "Great Eastern Life/" + name
    os.mkdir(path)

    createPolicyNoFolder(name, policy_no)

global createPolicyNoFolder
def createPolicyNoFolder(name, policy_no):
    path = "Great Eastern Life/" + name + "/" + policy_no
    os.mkdir(path)

    folderList = ["New Business", "Easi-Payment", "Hospital Claim", "Nominee", "Sign", "Letter", "Promotion", "Misc"]
    for i in range(len(folderList)):
        path = "Great Eastern Life/" + name + "/" + policy_no + "/" + folderList[i]
        os.mkdir(path)

global openFolder
def openFolder(name):
    path = os.path.abspath("./Great Eastern Life/" + name)
    os.startfile(path)

global folderList
global folderName
folderList = []
for folderName in os.listdir("Great Eastern Life/"):
    folderList.append(folderName)

global updateFolderList
def updateFolderList(name):
    if name not in folderList:
        folderList.append(name)
        drop['values'] = folderList

class GreatEasternLife(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

# Home Page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="\n\nHome Page\n-------------", font=SMALL_FONT)
        label.pack()

        label1 = tk.Label(self, text="Select Functions Below:", font=FONT)
        label1.pack(pady=10)

        button = tk.Button(self, text="Create New Customer Folder",
                            command=lambda: controller.show_frame(PageOne), padx=50, pady=10)
        button.pack(pady=10)

        button2 = tk.Button(self, text="Add New Policy (Existing Customer)",
                            command=lambda: controller.show_frame(PageTwo), padx=30, pady=10)
        button2.pack(pady=10)

        button3 = tk.Button(self, text="Open Customer Folder",
                            command=lambda: controller.show_frame(PageThree), padx=65, pady=10)
        button3.pack(pady=10)

        button4 = tk.Button(self, text="Exit",
                            command=exit, padx=45, pady=5)
        button4.pack(pady=10)

# Create New Customer Folder
class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        def create_new_customer():
            validate = False
            name = entry1.get()
            policy_no = entry2.get()

            regex = re.compile('[\\\\<>:"/|?*]')

            if name == "" or policy_no == "":
                messagebox.showwarning("Warning", "Name/Policy Number cannot be empty!")

            elif not (regex.search(name) == None):
                messagebox.showwarning("Warning", "Name cannot contain < > : \" / \\ | ? *")

            #elif not policy_no.isdigit():
            #    messagebox.showwarning("Warning", "Policy Number contain non-number!")

            else:
                validate = True

            if validate:
                if path.isdir("Great Eastern Life/" + name):
                    messagebox.showerror("Error", "Customer folder already exist!")

                else:
                    createCustomerFolder(name, policy_no)
                    updateFolderList(name)
                    messagebox.showinfo("Message", "Folder Created Successful!")
                    entry1.delete(0, tk.END)
                    entry2.delete(0, tk.END)

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="\n\nCreate New Customer Folder\n----------------------------------", font=SMALL_FONT)
        label.pack()

        label1 = tk.Label(self, text="\nCustomer's Name:", font=FONT)
        label1.pack()

        entry1 = tk.Entry(self, width=30, borderwidth=3)
        entry1.pack(pady=10)

        label2 = tk.Label(self, text="\nPolicy Number:", font=FONT)
        label2.pack()

        entry2 = tk.Entry(self, width=30, borderwidth=3)
        entry2.pack(pady=10)

        button1 = tk.Button(self, text="Create",
                            command=create_new_customer, padx=45, pady=5)
        button1.pack(pady=(30,10))

        button2 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage), padx=50, pady=5)
        button2.pack(pady=10)

# Add New Policy (Existing Customer)
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        def create_new_policy():
            validate = False
            name = drop.get()
            policy_no = entry1.get()

            if name == "":
                messagebox.showwarning("Warning", "Please select a customer!")

            elif policy_no == "":
                messagebox.showwarning("Warning", "Policy Number cannot be empty!")

            #elif not policy_no.isdigit():
            #    messagebox.showwarning("Warning", "Policy Number contain non-number!")

            else:
                validate = True

            if validate:
                if not path.isdir("Great Eastern Life/" + name):
                    messagebox.showerror("Error", "Customer folder not exist!")

                elif path.isdir("Great Eastern Life/" + name + "/" + policy_no):
                    messagebox.showerror("Error", "Policy number already exist!")

                else:
                    createPolicyNoFolder(name, policy_no)
                    messagebox.showinfo("Message", "New Policy Added Successful!")
                    entry1.delete(0, tk.END)

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="\n\nAdd New Policy (Existing Customer)\n----------------------------------------", font=SMALL_FONT)
        label.pack()

        label1 = tk.Label(self, text="\nCustomer's Name:", font=FONT)
        label1.pack()

        global drop
        drop = AutocompleteCombobox(self)
        drop.set_completion_list(folderList)
        drop.pack(pady=10)

        label2 = tk.Label(self, text="\nPolicy Number:", font=FONT)
        label2.pack()

        entry1 = tk.Entry(self, width=30, borderwidth=3)
        entry1.pack(pady=10)

        button1 = tk.Button(self, text="Create",
                            command=create_new_policy, padx=45, pady=5)
        button1.pack(pady=(30,10))

        button2 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage), padx=50, pady=5)
        button2.pack(pady=10)
        
# Open Customer Folder
class PageThree(tk.Frame):

    def __init__(self, parent, controller):

        def open_folder():
            validate = False
            name = drop.get()

            if name == "":
                messagebox.showwarning("Warning", "Please select a customer!")

            #elif not policy_no.isdigit():
            #    messagebox.showwarning("Warning", "Policy Number contain non-number!")

            else:
                validate = True

            if validate:
                if not path.isdir("Great Eastern Life/" + name):
                    messagebox.showerror("Error", "Customer folder not exist!")

                else:
                    openFolder(name)

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="\n\nOpen Customer Folder\n----------------------------------------", font=SMALL_FONT)
        label.pack()

        label1 = tk.Label(self, text="\nCustomer's Name:", font=FONT)
        label1.pack()

        global drop
        drop = AutocompleteCombobox(self)
        drop.set_completion_list(folderList)
        drop.pack(pady=10)

        button1 = tk.Button(self, text="Open",
                            command=open_folder, padx=45, pady=5)
        button1.pack(pady=(30,10))

        button2 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage), padx=50, pady=5)
        button2.pack(pady=10)

app = GreatEasternLife()
app.title("Great Eastern Life")
app.geometry("500x400")
app.mainloop()
