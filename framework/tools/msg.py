#! /usr/bin/python3
# -*- coding:utf-8 -*-

from tkinter import messagebox
import tkinter as tk

def error_box(title, message):
    r = tk.Tk()
    r.withdraw()
    messagebox.showerror(title, message)
    r.destroy()

def warning_box(title, message):
    r = tk.Tk()
    r.withdraw()
    messagebox.showwarning(title, message)
    r.destroy()


class MessageWindow():
    def __init__(self,timeout =60000, **kwargs):
        self.root = tk.Tk()
        self.root.geometry("+100+300")
        self.timeout = timeout
        if kwargs:
            title=kwargs.pop('title')
        self.data = None
    def entryBox(self,label):
        wFrame = tk.Frame(self.root, background="black", padx=20, pady=20)  #background="light yellow"
        wFrame.pack()
        ###################
        wLabel = tk.Label(wFrame, background="cyan", text = label,font=("Helvetica",20),justify = "left",wraplength = 600) #background = "yellow"
        wLabel.pack(side = "top",pady=10,fill = "x")
        wEntryBox = tk.Entry(wFrame, background="white", width=60,font=("Helvetica",20))
        wEntryBox.focus_force()
        wEntryBox.pack()
        ####################################
        def fin():
            self.data = str(wEntryBox.get())
            self.root.destroy()
        wSubmitButton = tk.Button(wFrame, text='OK', font=("Helvetica",20),pady=5,command=fin, default='active',width =10)
        wSubmitButton.pack(side = "bottom", pady=20)
        ## optionnal extra code in order to have a stroke on "Return" equivalent to a mouse click on the OK button
        def fin_R(event):
            fin()
        self.root.bind("<Key-Return>", fin_R)

        self.root.after(self.timeout, self.root.destroy) # This is the KEY INSTRUCTION that destroys the dialog box after the given timeout in millisecondsd
        self.root.mainloop()
    def get_entry(self,label):
        self.entryBox(label)
        return self.data
        ##########################
    
    def lableBox(self,label):
        # self.root.geometry("800x400+100+300")
        wFrame = tk.Frame(self.root, background="black", padx=20, pady=20)  #background="light yellow"
        wFrame.pack(fill = "x")
        ###################
        wLabel = tk.Label(wFrame, pady=10, padx=10, background="cyan", text = label,font=("Helvetica",30),justify = "left",wraplength = 600) #background = "yellow"
        wLabel.pack(side = "top",pady=10,fill = "x")
        ####################################
        def fin():
            self.root.destroy()
        wSubmitButton = tk.Button(wFrame, text='OK', font=("Helvetica",20),pady=5,command=fin, default='active',width =10)
        wSubmitButton.pack(side = "bottom", pady=20)
        wSubmitButton.focus_force()
        ## optionnal extra code in order to have a stroke on "Return" equivalent to a mouse click on the OK button
        def fin_R(event):
            fin()
        self.root.bind("<Key-Return>", fin_R)

        self.root.after(self.timeout, self.root.destroy) # This is the KEY INSTRUCTION that destroys the dialog box after the given timeout in millisecondsd
        self.root.mainloop()
    def get_label(self,label):
        self.lableBox(label)
        return self.data
        ##########################

    def yesnoBox(self,label):
        self.root.focus_force()
        wFrame = tk.Frame(self.root, background="black", padx=20, pady=20)
        wFrame.pack(fill = "x")
        ###################
        wLabel = tk.Label(wFrame, pady=10,background="cyan",text = label,font=("Helvetica",20),justify = "center",wraplength = 1000)
        wLabel.pack(side = "top", fill = "x",pady=10)
        ###############
        def fin():
            self.root.destroy()
        def return_yes():
            self.data = True
            fin()
        def return_no():
            self.data = False
            fin()
        def key_no(event):
            return_no()
        def key_yes(event):
            return_yes()
        wSubmitButton_Y = tk.Button(wFrame, text='YES', command=return_yes, default='active',width =30)
        wSubmitButton_Y.pack(side= 'left')
        wSubmitButton_N = tk.Button(wFrame, text='NO', command=return_no, default='active',width =30)
        wSubmitButton_N.pack(side= 'right')

        self.root.bind("y",key_yes)
        self.root.bind("n",key_no)

        self.root.mainloop()

    def get_yesno(self,label):
        self.yesnoBox(label)
        return self.data

    def show_result(self,Result):
        self.root.focus_force()
        txt_color = ("green2","P A S S") if Result else ("red","F A I L")
        wFrame = tk.Frame(self.root, background= txt_color[0], padx =200, pady =50)# padx=20, pady=20)
        wFrame.pack()
        wLabel = tk.Label(wFrame, pady=20,fg="white",background= txt_color[0], text = txt_color[1],font=("Helvetica",100))
        wLabel.pack()
        ###################
        def fin():
            self.root.destroy()
        wSubmitButton_Y = tk.Button(wFrame, background= "light yellow",text='OK', command=fin, default='active',width =30)
        wSubmitButton_Y.pack(side= 'bottom')
        def fin_R(event):
            fin()
        self.root.bind("<Return>", fin_R)

        self.root.mainloop()