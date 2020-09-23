import sqlite3
import tkinter as tk
import random
import pyttsx3
import os
import warnings
warnings.filterwarnings("ignore")
try:
    from textblob import TextBlob
except ImportError:
    pass

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'db.db')
dump = os.path.join(path, 'dump.sql')
icon = os.path.join(path, 'ico.png')

WIDTH = 600
HEIGHT = 300
i = [True]
answers = []
id_ = [None]
get_input_old = ['']
lst = ['red', 'light gray']

con = sqlite3.connect(db)
cur = con.cursor()
cur.execute('create table if not exists tbl(quest text, answ text)')
# dump
with open(dump, 'w', encoding='utf-8') as file_dump:
    for line in con.iterdump():
        file_dump.write('%s\n' % line)


def closing():
    con.close()
    root.destroy()
    exit(0)


def clear():
    l1['text'] = ''
    l1.update()
    entry.delete(0, tk.END)


def flash_lng():
    lst.reverse()
    l3.configure(fg=lst[0])
    id_[0] = l3.after(250, flash_lng)


def speak(random_answer):
    engine.say(random_answer)
    engine.runAndWait()


def enter_on(e):
    if e.keysym == 'Escape':
        closing()
    if e.keysym == 'Return':
        main()


def main():
    get_input = get_input_old[0]
    if i[0]:
        get_input = entry.get().lower()
        if '?' not in get_input:
            entry.insert(tk.END, '?')
        else:
            get_input = get_input.replace('?', '')
        if not get_input:
            clear()
            return
        languages = TextBlob(get_input).detect_language()
        if languages != 'ru':
            l3.after_idle(flash_lng)
            return
        else:
            l3.after_cancel(id_[0])
            l3['fg'] = 'green'
            l3.update()
    cur.execute('select answ from tbl where quest==?', (get_input,))
    answers.clear()
    for j in cur.fetchall():
        answers.append(*j)
    if len(answers) == 0 or not i[0]:
        i[0] = False
        lf1['text'] = ' Введите ответ: '
        l2['text'] = 'Для выхода из режима записи очистите поле ввода и нажмите Enter'
        root.update()
        get_output = entry.get().lower().replace('?', '')
        get_input_old[0] = get_input
        if not get_output:
            lf1['text'] = ' Введите вопрос: '
            l2['text'] = 'Для продолжения нажмите Enter'
            root.update()
            get_input_old[0] = ''
            i[0] = True
            clear()
            return
        if get_input == get_output or get_output in answers:
            clear()
            return
        cur.execute('insert into tbl values(?,?)', (get_input, get_output))
        con.commit()
        clear()
    else:
        lf1['text'] = ' Введите вопрос: '
        l3['text'] = languages
        random_answer = random.choice(answers)
        l1['text'] = random_answer
        root.update()
        speak(random_answer)
        get_input_old[0] = get_input


engine = pyttsx3.init(driverName='sapi5')

root = tk.Tk()
img = tk.PhotoImage(file=icon)
root.iconphoto(False, img)
root.title('Python Bot')
root.geometry('+1+1')
root.protocol('WM_DELETE_WINDOW', closing)
root.bind('<Key>', enter_on)

lf1 = tk.LabelFrame(root, font='arial 20 bold', text=' Введите вопрос: ')
lf1.pack(fill=tk.X)
l3 = tk.Label(lf1, font='arial 12 bold', fg='green')
l3.pack(anchor=tk.NE, padx=5)
entry = tk.Entry(lf1, font='arial 20 bold', fg='green', relief=tk.SUNKEN)
entry.focus_force()
entry.pack(fill=tk.X)
lf2 = tk.LabelFrame(root, font='arial 20 bold', text=' Ответ: ')
lf2.pack(ipady=5)
l1 = tk.Label(lf2, font='arial 20 bold', fg='blue', wraplength=700, width=40)
l1.pack(padx=70)
l2 = tk.Label(lf2, font='arial 10', fg='red', text='Для продолжения нажмите Enter')
l2.pack()
l4 = tk.Label(lf2, image=img)
l4.place(anchor=tk.NW)

id_[0] = l3.after(250, flash_lng)

root.mainloop()
