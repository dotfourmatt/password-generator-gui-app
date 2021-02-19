import os, json, ast
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modules.generator import passwordGenerator

class rootApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Copy password to clipboard widget
        self.copy = ttk.Button(self, text = "Copy Password", command = self.copyToClipboard, width = 30)
        self.copy.grid(column = 2, row = 0, columnspan = 3, rowspan = 2, sticky = 'nesw', pady = 2)

        # Length of password widgets
        self.lengthVar = tk.IntVar(value=8)
        self.spin = ttk.Spinbox(self, textvariable = self.lengthVar, wrap = True, width = 20, from_ = 8, to = 50, increment = 1)
        self.spin.grid(column = 0, row = 0, columnspan = 2, rowspan = 2, sticky = 'nesw', pady = 4)
        # Is there a better way to limit the scale?
        self.length = Limiter(self, variable = self.lengthVar, orient = 'vertical', precision = 0, from_ = 8, to = 50)
        self.length.grid(column = 0, row = 2, rowspan = 10, columnspan = 2, sticky = 'nesw')

        # Option widgets
        self.lc = tk.BooleanVar()
        self.lowerCase = ttk.Checkbutton(self, text = "Lower Case", offvalue = False, onvalue = True, variable = self.lc)
        self.lowerCase.grid(row = 2, column = 2, columnspan = 3, rowspan = 2, sticky = 'w')
        self.uc = tk.BooleanVar()
        self.upperCase = ttk.Checkbutton(self, text = "Upper Case", offvalue = False, onvalue = True, variable = self.uc)
        self.upperCase.grid(row = 4, column = 2, columnspan = 3, rowspan = 2, sticky = 'w')
        self.n = tk.BooleanVar()
        self.numbers = ttk.Checkbutton(self, text = "Numbers", offvalue = False, onvalue = True, variable = self.n)
        self.numbers.grid(row = 6, column = 2, columnspan = 3, rowspan = 2, sticky = 'w')
        self.s = tk.BooleanVar()
        self.symbols = ttk.Checkbutton(self, text = "Symbols", offvalue = False, onvalue = True, variable = self.s)
        self.symbols.grid(row = 8, column = 2, columnspan = 3, rowspan = 2, sticky = 'w')
        self.save = tk.BooleanVar()
        self.saveCheckbox = ttk.Checkbutton(self, text = "Save password?", offvalue = False, onvalue = True, variable = self.save)
        self.saveCheckbox.grid(row = 10, column = 2, columnspan = 3, rowspan = 2, sticky = 'w')

        # Displays generated password
        self.password = tk.Text(self, width = 20, height = 1)
        self.password.grid(row = 12, column = 0, columnspan = 5, rowspan = 2, sticky = 'nesw', pady = 2, padx = 2)

        # Opens a new window to view stored passwords
        self.viewSavedPasswords = ttk.Button(self, text="View Saved Passwords", command = self.viewSavedPasswordsWindow)
        self.viewSavedPasswords.grid(column = 0, row = 14, columnspan = 5, rowspan = 2, sticky = 'nesw', pady = 2, padx = 2)

        # Generates password
        self.generate = ttk.Button(self, text = "Generate", command = self.generatePassword)
        self.generate.grid(column = 0, row = 16, columnspan = 5, rowspan = 2, sticky = 'nesw', pady = 2, padx = 2)

    # Function generates the password
    def generatePassword(self):
        # Checks what options are selected
        options = [self.lc.get(), self.uc.get(), self.n.get(), self.s.get()]

        # Checks if options are selected
        noSel = 0
        for opt in options:
            if opt:
                noSel += 1
        if noSel == 0:
            tk.messagebox.showerror(title="Error!", message="Please select some options!")
        
        # Will run if requirements are met
        else:
            password = passwordGenerator(self.lengthVar.get(), options, self.save.get())
            #tk.messagebox.showinfo(title="Success", message="Password has been generated!")
            self.password.delete("1.0", "end-1c")
            self.password.insert(tk.END, password)
            self.parent.update() # How can I update the secondary window when a password is generated?

    # Secondary window for viewing saved passwords in JSON file
    def viewSavedPasswordsWindow(self):
        if os.path.exists('passwords.json') == False:
            temp_db = {}
            f = open("passwords.json", 'x+')
            f.write(json.dumps(temp_db))
            f.close()
            tk.messagebox.showerror(title="Error!", message="You don't have any saved passwords!")

        else:
            with open("passwords.json", "r") as file:    
                for line in file:
                    record = line
            passwords = ast.literal_eval(record)

            if len(passwords) < 1:
                tk.messagebox.showerror(title="Error!", message="You don't have any saved passwords!")

            else:
                window = tk.Toplevel(self.parent)
                window.title("Saved Passwords")
                window.iconbitmap('img/logo.ico')
                window.resizable(False, False)
                self.viewSavedPasswords.config(state='disable')

                for date, password in passwords.items(): # Howto add scroll bar if window size become bigger than screen?
                    entry = tk.Text(window, height = 1)
                    entry.grid()
                    entry.insert(tk.END, f"{date}: {password}")

                def on_closing():
                    window.destroy()
                    self.viewSavedPasswords.config(state='normal')

                window.protocol("WM_DELETE_WINDOW", on_closing)
        
    def copyToClipboard(self):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.password.get("1.0", "end-1c"))
        self.parent.update()

# Source: https://www.stackoverflow.com/questions/54186639/tkinter-control-ttk-scales-increment-as-with-tk-scale-and-a-tk-doublevar
class Limiter(ttk.Scale):
    """ ttk.Scale subclass that limits the precision of values. """

    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')
        self.chain = kwargs.pop('command', lambda *a: None)
        super(Limiter, self).__init__(*args, command=self._value_changed, **kwargs)
    
    def _value_changed(self, newvalue):
        newvalue = round(float(newvalue), self.precision) # Is there a way this can just be an integer, and not a float?
        self.winfo_toplevel().globalsetvar(self.cget('variable'), (newvalue))
        self.chain(newvalue)