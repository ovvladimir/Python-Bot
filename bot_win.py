import sqlite3
import tkinter as tk
from textblob import TextBlob
import random
import pyttsx3

WIDTH = 600
HEIGHT = 300
languages = 'ru'
lst = ['red', 'light gray']

conn = sqlite3.connect('txt.db')
cur = conn.cursor()
cur.execute('create table if not exists tbl(quest text, answ text)')
# dump
with open('txt_dump.sql', 'w') as file_dump:
    for line in conn.iterdump():
        file_dump.write('%s\n' % line)

engine = pyttsx3.init(driverName='sapi5')


def closing():
    conn.close()
    root.destroy()
    exit()


def flash_lng():
    lst.reverse()
    l3.configure(fg=lst[0])
    l3.after(250, flash_lng)


def voiсe(ramdom_answer):
    engine.say(ramdom_answer)
    engine.runAndWait()


def enter_on(e):
    global a, b
    if e.keysym == 'Return':
        if i == 1:
            a = entry.get().lower()
        elif i == 2:
            b = entry.get().lower()
        lf.destroy()
        lf.quit()


def input_txt(txt):
    global entry, l3, lf
    lf = tk.LabelFrame(root, width=WIDTH, height=HEIGHT)
    lf.pack()
    lf1 = tk.LabelFrame(lf, font='arial 20 bold', text=txt,
                        width=WIDTH, height=HEIGHT/2)
    lf1.pack_propagate(False)
    lf1.pack()
    l3 = tk.Label(lf1, font='arial 12 bold', fg='green3', text=languages)
    l3.pack(anchor=tk.NE, padx=5)
    if languages != 'ru':
        l3.after_idle(flash_lng)
    entry = tk.Entry(lf1, font='arial 20 bold', fg='green', relief=tk.SUNKEN)
    entry.focus_force()
    entry.pack(fill=tk.X, pady=5)
    if i == 3:
        if '?' in a:
            entry.insert(0, a)
        else:
            entry.insert(0, f'{a}?')
        txt = 'Ответ: '
        lf2 = tk.LabelFrame(lf, font='arial 20 bold', text=txt,
                            width=WIDTH, height=HEIGHT/2)
        lf2.pack_propagate(False)
        lf2.pack()
        l4 = tk.Label(lf2, image=img)
        l4.place(x=0, y=0)
        ramdom_answer = random.choice(answers)
        l1 = tk.Label(lf2, font='arial 30 bold', fg='blue',
                      text=ramdom_answer).pack()
        l2 = tk.Label(lf2, font='arial 10', fg='red',
                      text='Для продолжения нажмите Enter').pack()
        lf.update()
        voiсe(ramdom_answer)
    lf.mainloop()


root = tk.Tk()
root.title('Python Bot')
img = tk.PhotoImage(file='ico.png')
root.iconphoto(False, img)
root.geometry(f'{WIDTH}x{HEIGHT}+1+1')
root.protocol('WM_DELETE_WINDOW', closing)
root.bind('<Key>', enter_on)

while True:
    i = 1
    input_txt('Введите вопрос (Enter - выход): ')
    if not a:
        break
    languages = TextBlob(a).detect_language()
    if languages != 'ru':
        continue
    cur.execute('select answ from tbl where quest==?', (a,))
    answers = [j[0] for j in cur.fetchall()]
    if not answers:
        while True:
            i = 2
            input_txt('Введите ответ (Enter - выход): ')
            if not b:
                break
            cur.execute('insert into tbl values(?,?)', (a, b))
            conn.commit()
    else:
        i = 3
        input_txt('Вопрос: ')

closing()
