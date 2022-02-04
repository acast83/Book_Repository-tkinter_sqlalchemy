from tkinter import *
from backend import Backend
window = Tk()
window.wm_title("Book Repository")

backend = Backend()


class Frontend:

    def get_selected_row(self, event):

        try:
            index = list1.curselection()[0]
            global selected_tuple
            selected_tuple = list1.get(index)
            global id
            id = selected_tuple[0]
            e1.delete(0, END)
            e1.insert(END, selected_tuple[1])
            e2.delete(0, END)
            e2.insert(END, selected_tuple[2])
            e3.delete(0, END)
            e3.insert(END, selected_tuple[3])
            e4.delete(0, END)
            e4.insert(END, selected_tuple[4])
        except IndexError:
            pass

    def view_command(self):
        list1.delete(0, END)
        for book in backend.view():
            list1.insert(END, [book.id, book.title,
                               book.author, book.year, book.isbn])

    def add_entry_command(self):
        backend.insert(title_text.get(), author_text.get(),
                       year_text.get(), isbn_text.get())
        list1.delete(0, END)
        list1.insert(END, [title_text.get(), author_text.get(),
                           year_text.get(), isbn_text.get()])

    def delete_command(self):
        backend.delete(id)
        self.view_command()

    def search_command(self):
        list1.delete(0, END)
        results = backend.search(
            title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        if results is not None:
            for row in results:
                list1.insert(
                    END, [row.id, row.title, row.author, row.year, row.isbn])
        else:
            return

    def update_command(self):
        backend.update(selected_tuple[0], title_text.get(
        ), author_text.get(), year_text.get(), isbn_text.get())
        self.view_command()


frontend = Frontend()

l1 = Label(window, text="Title")
l1.grid(row=0, column=0)

l1 = Label(window, text="Author")
l1.grid(row=0, column=2)

l1 = Label(window, text="Year")
l1.grid(row=1, column=0)

l1 = Label(window, text="ISBN")
l1.grid(row=1, column=2)

title_text = StringVar()
e1 = Entry(window, textvariable=title_text)
e1.grid(row=0, column=1)

author_text = StringVar()
e2 = Entry(window, textvariable=author_text)
e2.grid(row=0, column=3)

year_text = StringVar()
e3 = Entry(window, textvariable=year_text)
e3.grid(row=1, column=1)

isbn_text = StringVar()
e4 = Entry(window, textvariable=isbn_text)
e4.grid(row=1, column=3)

list1 = Listbox(window, height=6, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)
list1.bind("<<ListboxSelect>>", frontend.get_selected_row)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

b1 = Button(window, text="View All", width=12, command=frontend.view_command)
b1.grid(row=2, column=3)

b2 = Button(window, text="Search Entry", width=12,
            command=frontend.search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add Entry", width=12,
            command=frontend.add_entry_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update", width=12, command=frontend.update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete", width=12, command=frontend.delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop()
