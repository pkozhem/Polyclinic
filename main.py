import sqlite3
import tkinter as tk
import datetime
from tkinter import ttk


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Add patient', command=self.open_dialog, bg='#d7d8e0', bd=0.5,
                                    compound=tk.TOP, width=15)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_update_dialog = tk.Button(toolbar, text='Edit', command=self.open_update_dialog, bg='#d7d8e0', bd=0.5,
                                      compound=tk.TOP, width=15)
        btn_update_dialog.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Delete', command=self.delete_records, bg='#d7d8e0', bd=0.5,
                               compound=tk.TOP, width=15)
        btn_delete.pack(side=tk.LEFT)

        btn_search = tk.Button(toolbar, text='Search by Address', command=self.open_search_dialog, bg='#d7d8e0', bd=0.5,
                               compound=tk.TOP, width=15)
        btn_search.pack(side=tk.LEFT)

        btn_history = tk.Button(toolbar, text='Disease History', command=self.open_history_dialog, bg='#d7d8e0', bd=0.5,
                                compound=tk.TOP, width=15)
        btn_history.pack(side=tk.LEFT)

        label_title = tk.Label(self, text='Patient list')
        label_title.pack()

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Birth', 'Address'), height=15, show='headings')

        self.tree.column('ID', width=15, anchor=tk.CENTER)
        self.tree.column('Name', width=265, anchor=tk.CENTER)
        self.tree.column('Birth', width=100, anchor=tk.CENTER)
        self.tree.column('Address', width=265, anchor=tk.CENTER)

        self.tree.heading('ID', text="#")
        self.tree.heading('Name', text="Name")
        self.tree.heading('Birth', text="Birth")
        self.tree.heading('Address', text="Address")

        self.tree.pack()

    def records(self, name, year_birth, month_birth, day_birth, address, history):
        self.db.insert_data(name, year_birth, month_birth, day_birth, address, history)
        self.view_records()

    def update_record(self, name, year_birth, month_birth, day_birth, address, history):
        year = int(year_birth)
        month = int(month_birth)
        day = int(day_birth)
        date = datetime.date(year, month, day)
        self.db.curs.execute(
            '''UPDATE polyclinics SET name=?, birth=?, address=?, history=? WHERE ID=?''',
            (name, date, address, history, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.curs.execute('''SELECT * FROM polyclinics''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.curs.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.curs.execute('''DELETE FROM polyclinics WHERE ID=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, address):
        address = ('%' + address + '%',)
        self.db.curs.execute('''SELECT * FROM polyclinics WHERE address LIKE ?''', address)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.curs.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def open_history_dialog(self):
        History()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Add patient')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        values_day = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10', u'11', u'12', u'13', u'14',
                      u'15', u'16', u'17', u'19', u'20', u'21', u'22', u'23', u'24', u'25', u'26', u'27', u'28', u'29',
                      u'30', u'31']
        values_month = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10', u'11', u'12']

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=150, y=50, width=215)

        self.entry_birth_year = ttk.Entry(self)
        self.entry_birth_year.place(x=150, y=80, width=67)

        self.combobox_birth_month = ttk.Combobox(self, values=values_month)
        self.combobox_birth_month.place(x=224, y=80, width=67)

        self.combobox_birth_day = ttk.Combobox(self, values=values_day)
        self.combobox_birth_day.place(x=298, y=80, width=67)

        self.entry_address = ttk.Entry(self)
        self.entry_address.place(x=150, y=110, width=215)

        self.entry_history = ttk.Entry(self)
        self.entry_history.place(x=150, y=140, width=215)

        label_name = tk.Label(self, text='Name:')
        label_birth = tk.Label(self, text='Birth [YYYY-MM-DD]:')
        label_address = tk.Label(self, text='Address:')
        label_history = tk.Label(self, text='History Disease')
        label_name.place(x=10, y=50)
        label_birth.place(x=10, y=80)
        label_address.place(x=10, y=110)
        label_history.place(x=10, y=140)

        self.button_add = ttk.Button(self, text='Add')
        self.button_add.place(x=240, y=190)
        self.button_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                           self.entry_birth_year.get(),
                                                                           self.combobox_birth_month.get(),
                                                                           self.combobox_birth_day.get(),
                                                                           self.entry_address.get(),
                                                                           self.entry_history.get()))
        button_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        button_cancel.place(x=320, y=190)

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.init_edit()
        self.default_data()

    def init_edit(self):
        self.title('Edit')
        button_edit = ttk.Button(self, text='Edit')
        button_edit.place(x=240, y=190)
        button_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                             self.entry_birth_year.get(),
                                                                             self.combobox_birth_month.get(),
                                                                             self.combobox_birth_day.get(),
                                                                             self.entry_address.get(),
                                                                             self.entry_history.get()))
        self.button_add.destroy()

    def default_data(self):
        self.db.curs.execute('''SELECT * FROM polyclinics WHERE id=?''',
                             (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.curs.fetchone()
        my_date = row[2]
        curr = datetime.datetime.strptime(my_date, "%Y-%m-%d")
        self.entry_name.insert(0, row[1])
        self.entry_birth_year.insert(0, str(curr.year))
        self.combobox_birth_month.insert(0, str(curr.month))
        self.combobox_birth_day.insert(0, str(curr.day))
        self.entry_address.insert(0, row[3])
        self.entry_history.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Search by Address')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Search')
        label_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=155)

        btn_search = ttk.Button(self, text='Search')
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.place(x=50, y=50, width=70)

        btn_refresh = ttk.Button(self, text='Refresh', command=self.destroy)
        btn_refresh.bind('<Button-1>', lambda event: self.view.view_records())
        btn_refresh.place(x=120, y=50, width=70)

        btn_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        btn_cancel.place(x=190, y=50, width=70)


class History(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.init_history()

    def init_history(self):
        self.db.curs.execute('''SELECT * FROM polyclinics WHERE id=?''',
                             (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.curs.fetchone()

        self.title('Patients Disease History')
        self.geometry('400x400+400+300')
        self.resizable(False, False)

        label_disease_history = tk.Label(self, text='Disease History')
        label_disease_history.place(x=10, y=10)

        label_data_history = tk.Label(self, text=row[4])
        label_data_history.place(x=10, y=50)


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('polyclinics.db')
        self.curs = self.conn.cursor()
        self.curs.execute(
            '''CREATE TABLE IF NOT EXISTS polyclinics (id integer primary key, name text, birth date, address text, 
            history text)''')
        self.conn.commit()

    def insert_data(self, name, year_birth, month_birth, day_birth, address, history):
        year = int(year_birth)
        month = int(month_birth)
        day = int(day_birth)
        date = datetime.date(year, month, day)
        self.curs.execute(
            '''INSERT INTO polyclinics(name, birth, address, history) VALUES (?, ?, ?, ?)''',
            (name, date, address, history))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Polyclinic")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
