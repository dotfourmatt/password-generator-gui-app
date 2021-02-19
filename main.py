if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox
    from modules.gui import rootApp

    root = tk.Tk()

    # Source: https://www.semicolonworld.com/question/44508/how-do-i-handle-the-window-close-event-in-tkinter
    def on_closing():
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            root.destroy()
    
    # Source: https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
    w = 400
    h = 440

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.title("Password Generator")
    root.iconbitmap(r'img/logo.ico')
    root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
    #root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(False, False)
    rootApp(root).pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()