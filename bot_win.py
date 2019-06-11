import sqlite3
import random
import tkinter as tk
import sys

WIDTH = 600
HEIGHT = 300

conn = sqlite3.connect('txt.db')
cur = conn.cursor()
cur.execute('create table if not exists tbl(quest text, answ text)')


def closing():
    conn.close()
    sys.exit(0)


def returned(e):
    global a, b
    if e.keysym == 'Return':
        if i == 1:
            a = entry.get()
        elif i == 2:
            b = entry.get()
        root.destroy()


def input_(txt):
    global entry, root
    root = tk.Tk()
    root.title('Python Bot')
    root.iconphoto(True, tk.PhotoImage(file='ico.png'))
    root.geometry(f'{WIDTH}x{HEIGHT}+0+0')
    root.protocol("WM_DELETE_WINDOW", closing)
    root.bind('<Key>', returned)
    lf1 = tk.LabelFrame(root, font='arial 20 bold', text=txt,
                        width=WIDTH, height=HEIGHT/2)
    lf1.pack_propagate(False)
    lf1.pack()
    entry = tk.Entry(lf1, font='arial 20 bold', fg='green', relief=tk.SUNKEN)
    entry.focus_force()
    entry.pack(fill=tk.X, expand=True)
    if i == 3:
        if '?' in a:
            entry.insert(0, a)
        else:
            entry.insert(0, f'{a}?')
        txt = 'Ответ: '
        lf2 = tk.LabelFrame(root, font='arial 20 bold', text=txt,
                            width=WIDTH, height=HEIGHT/2)
        lf2.pack_propagate(False)
        lf2.pack()
        l1 = tk.Label(lf2, font='arial 30 bold', fg='blue',
                      text=random.choice(answers))
        l2 = tk.Label(lf2, font='arial 10', fg='red',
                      text='Для продолжения нажмите Enter')
        l1.pack()
        l2.pack()
    tk.mainloop()


while True:
    i = 1
    input_('Введите вопрос (Enter - выход): ')
    if not a:
        break
    cur.execute('select answ from tbl where quest==?', (a,))
    answers = [j[0] for j in cur.fetchall()]
    if not answers:
        while True:
            i = 2
            input_('Введите ответ (Enter - выход): ')
            if not b:
                break
            cur.execute('insert into tbl values(?,?)', (a, b))
            conn.commit()
    else:
        i = 3
        input_('Вопрос: ')

closing()
