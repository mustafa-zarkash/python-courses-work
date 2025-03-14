"""
A program that stores this book information
Title , Author
Year , ISBN

User can : 

view all records 
search an entry
Add entry
update entry
Delete
Close
"""

from tkinter import *
from backend import Database

db = Database("books.db")

def get_selected_row(event):
    global selected_tuple
    try :
            index = list1.curselection()[0]
            selected_tuple = list1.get(index)
            e1.delete(0,END)
            e1.insert(0,selected_tuple[1])
            
            e2.delete(0,END)
            e2.insert(0,selected_tuple[2])
            
            e3.delete(0,END)
            e3.insert(0,selected_tuple[3])
            
            e4.delete(0,END)
            e4.insert(0,selected_tuple[4])
    except IndexError : 
            pass

    
def view_command():
    list1.delete(0,END)
    for row in db.view(): 
        list1.insert(END , row)

def search_command():
    list1.delete(0,END)
    for row in db.search(title_text.get() , author_text.get() , year_text.get() , isbn_text.get()):
        list1.insert(END , row)

def add_command():
    db.insert(title_text.get() , author_text.get() , year_text.get() , isbn_text.get())
    view_command()

def delete_command():
    db.delete(selected_tuple[0])
    view_command()

def update_command():
    db.update(selected_tuple[0],title_text.get() , author_text.get() , year_text.get() , isbn_text.get())
    view_command()

#UI Creation : 
window = Tk()

#labels : 
l1 =Label(window , text = "Title")
l1.grid(row=0 , column = 0 )


l2 =Label(window , text = "Author")
l2.grid(row=0 , column = 2 )


l3 =Label(window , text = "Year")
l3.grid(row=1 , column = 0 )


l4 =Label(window , text = "ISBN")
l4.grid(row=1 , column = 2 )

#Entries : 
title_text = StringVar()
e1 = Entry(window , textvariable = title_text)
e1.grid(row = 0 , column =1 )

author_text = StringVar()
e2 = Entry(window , textvariable = author_text)
e2.grid(row = 0 , column =3 )

year_text = StringVar()
e3 = Entry(window , textvariable = year_text)
e3.grid(row = 1 , column =1 )

isbn_text = StringVar()
e4 = Entry(window , textvariable = isbn_text)
e4.grid(row = 1 , column =3 )

#listbox : 
list1 = Listbox(window , height = 6 , width = 35)
list1.grid (row = 2 , column = 0 , rowspan = 6 , columnspan =2)

sb1 = Scrollbar(window)
sb1.grid(row = 2 , column = 2 , rowspan = 6)

list1.configure(yscrollcommand = sb1.set)
sb1.configure(command = list1.yview)

list1.bind('<<ListboxSelect>>' , get_selected_row)

#buttons 
b1 = Button(window , text = "View all" , width = 12 , command = view_command)
b1.grid(row =2 , column = 3)

b1 = Button(window , text = "search entry" , width = 12 , command = search_command)
b1.grid(row =3 , column = 3)

b1 = Button(window , text = "add entry" , width = 12 ,command = add_command)
b1.grid(row =4 , column = 3)

b1 = Button(window , text = "update selected" , width = 12 , command = update_command)
b1.grid(row =5 , column = 3)

b1 = Button(window , text = "delete selected" , width = 12 , command = delete_command)
b1.grid(row =6 , column = 3)

b1 = Button(window , text = "close" , width = 12 , command = window.destroy)
b1.grid(row =7 , column = 3)

#----------------------------------

window.mainloop()