from tkinter import *
from tkinter import messagebox as mb
import pickle
import hashlib
import os
import win32api
import winreg

user_id, session, attempts = 0, 0, 0
win = Tk()

with open('lab.pickle', 'rb') as file:
    data = pickle.load(file)


def quit_app():
    win.destroy()
    file.close()
    exit()


def ValidPass(password) -> bool:
    valid = [False, False, False]
    for s in password:
        if re.search('[a-z]', s):
            valid[0] = True
        elif re.search('[а-я]', s):
            valid[1] = True
        elif s in ',.-!?":;':
            valid[2] = True
        else:
            return False

    if valid[0] and valid[1] and valid[2]:
        return True

    return False


def LimitationsUserChild(user, login, com):
    with open('lab.pickle', 'wb') as fw:
        if com == "block":
            if login not in data.get('Block'):
                data.get('Block').append(login)
            else:
                mb.showwarning("Внимание", "Аккаунт уже заблокирован!")
        else:
            if login in data.get('Block'):
                data.get('Block').pop(data.get('Block').index(login))
            else:
                mb.showwarning("Внимание", "Аккаунт разблокирован!")
        pickle.dump(data, fw)

    user.destroy()


def LimitationsUser():
    child_limit = Toplevel()
    child_limit.title("Блокировка пользователя")
    child_limit.geometry("354x150+500+350")
    child_limit.resizable(False, False)

    Label(child_limit, text="Логин пользователя:", font=("Arial 32", 12)).place(x=20, y=10)
    block_user = Entry(child_limit, width=43, textvariable=StringVar(), highlightthickness=1, relief=GROOVE, font=("Arial 32", 10))
    block_user.place(x=24, y=36)

    Button(child_limit, text="Заблокировать", font=("Arial 32", 11), width=13, relief=FLAT, background="#34506b", foreground="#ccc",
           command=lambda: LimitationsUserChild(child_limit, block_user.get(), "block")).place(x=200, y=73)

    Button(child_limit, text="Разблокировать", font=("Arial 32", 11), width=13, relief=FLAT,  background="#34506b", foreground="#ccc",
           command=lambda: LimitationsUserChild(child_limit, block_user.get(), "unblock")).place(x=30, y=73)


def BlockUserChild(user, login):
    same = False
    for i in data.get('Block'):
        if i == login:
            mb.showwarning("Внимание", "Аккаунт уже заблокирован!")
            same = True
            break

    if not same:
        data.get('Block').append(login)
        with open('lab.pickle', 'wb') as fw:
            pickle.dump(data, fw)

        fw.close()

    user.destroy()


def BlockUser():
    child_block = Toplevel()
    child_block.title("Блокировка пользователя")
    child_block.geometry("354x150+500+350")
    child_block.resizable(False, False)

    Label(child_block, text="Логин пользователя:", font=("Arial 32", 12)).place(x=20, y=10)

    block_user = Entry(child_block, width=43, textvariable=StringVar(), highlightthickness=1, relief=GROOVE, font=("Arial 32", 10))
    block_user.place(x=24, y=36)

    button = Button(child_block, text="Заблокировать", font=("Arial 32", 11), width=13, relief=FLAT, background="#34506b",
                    foreground="#ccc",
                    command=lambda: BlockUserChild(child_block, block_user.get()))
    button.place(x=200, y=73)


def ListUser():
    child_list = Toplevel()
    child_list.title("Список пользователей")
    child_list.geometry("450x250")
    child_list.resizable(False, False)

    Label(child_list, text="№", font=("Arial 32", 12)).place(x=40, y=0)
    Label(child_list, text="Логин", font=("Arial 32", 12)).place(x=190, y=0)
    Label(child_list, text="Блокировка", font=("Arial 32", 12)).place(x=330, y=0)

    for index, element in enumerate(data.get('Login')):
        Label(child_list, text=index + 1, font=("Arial 32", 12)).place(x=43, y=(index + 1) * 25)
        Label(child_list, text=element, font=("Arial 32", 12)).place(x=190, y=(index + 1) * 25)
        if element in data.get('Block'):
            Label(child_list, text="Yes", font=("Arial 32", 12)).place(x=357, y=(index + 1) * 25)
        else:
            Label(child_list, text="No", font=("Arial 32", 12)).place(x=360, y=(index + 1) * 25)



def ChangePass(child, oldpass, newpass, confirmpass):
    global data
    same = False

    if newpass:
        if newpass == confirmpass:
            for i in data.get('Password'):
                if i == oldpass:
                    if ValidPass(confirmpass):
                        data.get('Password')[data.get('Password').index(i)] = confirmpass
                        mb.showinfo("Успешно", "Пароль успешно изменен!")
                        same = True
                        break
                    else:
                        mb.showerror("Ошибка", "Ваш пароль очень слабый, используйте символы латиницы, кириллицы и знаки препинания!")
                        win_ChangePass()
                        same = True


            if not same:
                mb.showerror("Ошибка", "Старый пароль введён не верно!")
                win_ChangePass()

            with open('lab.pickle', 'wb') as filew:
                pickle.dump(data, filew)
        else:
            mb.showwarning("Внимание", "Пароли не совпадают, попробуйте еще раз!")
            win_ChangePass()

        child.destroy()
    else:
        mb.showwarning("Внимание", "Пожалуйста, введите новый пароль!")


def win_ChangePass():
    child_change = Toplevel()
    child_change.title("Изменение пароля")
    child_change.geometry("354x230")
    child_change.resizable(False, False)

    msg_oldpass = Label(child_change, text="Старый пароль:", font=("Arial 32", 12))
    msg_oldpass.place(x=20, y=10)
    entry_oldpass = Entry(child_change, width=43, textvariable=StringVar(), highlightthickness=1, relief=GROOVE, font=("Arial 32", 10))
    entry_oldpass.place(x=24, y=36)

    msg_newpass = Label(child_change, text="Новый пароль:", font=("Arial 32", 13))
    msg_newpass.place(x=20, y=85)
    entry_newpass = Entry(child_change, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1, font=("Arial 32", 10))
    entry_newpass.place(x=24, y=111)

    msg_confirmpass = Label(child_change, text="Повторите пароль:", font=("Arial 32", 13))
    msg_confirmpass.place(x=20, y=135)
    entry_confirmpass = Entry(child_change, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1, font=("Arial 32", 10))
    entry_confirmpass.place(x=24, y=159)

    button = Button(child_change, text="Изменить", font=("Arial 32", 11), width=10, relief=FLAT, background="#34506b", foreground="#ccc",
                    command=lambda: ChangePass(child_change, entry_oldpass.get(), entry_newpass.get(), entry_confirmpass.get()))
    button.place(x=230, y=193)


def win_panel(objects):
    for items in objects:
        items.destroy()

    win.geometry("504x350+{0}+{1}".format(int(win.winfo_screenwidth() / 2) - 225, int(win.winfo_screenheight() / 2) - 225))
    Label(win, text="Панель управления", font=("Arial 32", 22), bg='White', fg="Black", width=30, height=1).place(relx=0, rely=0)

    status = NORMAL if session == 2 else DISABLED

    Button(win, text="Изменить пароль", font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black",  command=win_ChangePass).place(relx=0, rely=0.15)

    Button(win, text="Список пользователей", state=status, font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black", command=ListUser).place(relx=0, rely=0.28)

    Button(win, text="Добавить пользователя", state=status, font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black", command=Registration).place(relx=0, rely=0.40)

    Button(win, text="Заблокировать пользователя", state=status, font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black", command=BlockUser).place(relx=0, rely=0.52)

    Button(win, text="Вкл/выкл ограничений", state=status, font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black", command=LimitationsUser).place(relx=0, rely=0.64)

    Button(win, text="Выход", font=("Arial 32", 11), width=55, height=2, relief=FLAT, background="White", foreground="Black", command=quit_app).pack(side=BOTTOM)


def cmd_entry(login, password, objects):
    global attempts, session
    user = False
    if login:
        for j in data.get('Block'):
            if login == j:
                mb.showwarning("Внимание", "Аккаунт заблокирован!")
                quit_app()

        if login == 'admin':
            session = 2

        for i in range(len(data.get('Password'))):
            if login == data.get('Login')[i] and password == data.get('Password')[i]:
                win_panel(objects)
                user = True
                break

        if not user and attempts < 3:
            mb.showwarning("Внимание", "Неверный логин/пароль, попробуйте еще раз!\nИли нажмите 'Регистрация' чтоб создать аккаунт!\n\nКоличество попыток для входа {}".format(3 - attempts))
            attempts += 1
        elif attempts == 3:
            mb.showerror("Ошибка", "Вы изчерпали все возможные попытки\nПопробуйте в другой раз!")
            quit_app()
    else:
        mb.showwarning("Внимание", "Пожалуйста, введите имя аккаунта!")

    print(data.get('Login'))
    print(data.get('Password'))
    print(data.get('Block'))


def check_pass(child_window, login, entry_password, repeat_password):
    global data
    same = False

    if entry_password == repeat_password:
        for i in data.get('Login'):
            if i == login:
                mb.showwarning("Внимание", "Пользователь с таким именем существует!")
                Registration()
                same = True
                break
        if ValidPass(repeat_password):
            if not same:
                data.get('Login').append(login)
                data.get('Password').append(repeat_password)
        else:
            mb.showerror("Ошибка", "Ваш пароль очень слабый, используйте символы латиницы, кириллицы и знаки препинания!")
            Registration()


        # data_clear = {'Login': ["admin"], 'Password': ["admin"], 'Block': []}
        with open('lab.pickle', 'wb') as filew:
            pickle.dump(data, filew)
    else:
        mb.showwarning("Внимание", "Пароли не совпадают, попробуйте еще раз!")
        Registration()

    child_window.destroy()


def win_auth():
    win.geometry("504x350+{0}+{1}".format(int(win.winfo_screenwidth() / 2) - 225, int(win.winfo_screenheight() / 2) - 225))
    win.resizable(False, False)

    label = Label(win, text="Авторизация", font=("Arial 32", 22), bg='#2d557d', fg="White", width=25, height=1)
    label.pack()

    msg_login = Label(win, text="Логин", font=("Arial 32", 12), height=2)
    msg_login.pack()
    entry_login = Entry(win, width=43,  textvariable=StringVar(), highlightthickness=1, relief=GROOVE, font=("Arial 32", 10))
    entry_login.pack()

    msg_pass = Label(win, text="Пароль", font=("Arial 32", 13), height=2)
    msg_pass.pack()
    entry_pass = Entry(win, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1, font=("Arial 32", 10))
    entry_pass.pack()

    button = Button(win, text="Вход", font=("Arial 32", 11), width=10, relief=FLAT, background="#34506b",
                    foreground="#ccc", height=1, command=lambda: cmd_entry(entry_login.get(), entry_pass.get(), objects))
    button.place(relx=0.15, rely=0.60)

    button1 = Button(win, text="Регистрация", font=("Arial 32", 11), width=18, relief=FLAT, background="#34506b",
                     foreground="#ccc", height=1, command=lambda: Registration())
    button1.place(relx=0.50, rely=0.60)
    objects = [label, msg_login, entry_login, msg_pass, entry_pass, button, button1]


def Registration():
    child_user = Toplevel()
    child_user.title("Регистрация")
    child_user.geometry("454x300+{0}+{1}".format(int(win.winfo_screenwidth() / 4), int(win.winfo_screenheight() / 4)))
    child_user.resizable(False, False)

    msg_login = Label(child_user, text="Введите логин:", font=("Arial 32", 12))
    msg_login.pack()
    entry_login = Entry(child_user, width=43, textvariable=StringVar(), highlightthickness=1, relief=GROOVE, font=("Arial 32", 10))
    entry_login.pack()

    msg_pass = Label(child_user, text="Введите пароль:", font=("Arial 32", 13))
    msg_pass.pack()
    entry_pass = Entry(child_user, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1, font=("Arial 32", 10))
    entry_pass.pack()

    repeat_password = Label(child_user, text="Повторите пароль:", font=("Arial 32", 13))
    repeat_password.pack()
    repeat_password = Entry(child_user, width=43, textvariable=StringVar(), show="●", relief=GROOVE, highlightthickness=1, font=("Arial 32", 10))
    repeat_password.pack()

    button = Button(child_user, text="Добавить", font=("Arial 32", 11), width=10, relief=GROOVE, background="#34506b", foreground="#ccc", command=lambda: check_pass(child_user, entry_login.get(), entry_pass.get(), repeat_password.get()))
    button.pack()


def information():
    mb.showinfo("О программе", "Автор: Курт Олег, Горобець Ангеліна\nГруппа: ФБ-72, ФБ-74\nВариант: 7\n\nНаявність латинських букв, символів кирилиці і розділових знаків")


def create():
    win.title("Лабораторная  №1")
    menubar = Menu(win)
    win.config(menu=menubar)
    info = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Справка", menu=info)
    info.add_command(label="О программе", command=information)
    win_auth()
    win.mainloop()


if __name__ == "__main__":
    try:
        signature = os.getlogin() + win32api.GetComputerName() + win32api.GetWindowsDirectory() + win32api.GetSystemDirectory()
        signature += "{}{}{}".format(win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(7), win32api.GlobalMemoryStatus()['TotalPhys'])
        sha = hashlib.sha256(signature.encode()).hexdigest()
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\KurtOlehHorobetsAngelina", 0, winreg.KEY_ALL_ACCESS)
        get = winreg.QueryValueEx(key, "Signature")
        if sha != get[0]:
            win.withdraw()
            mb.showerror("Ошибка лицензии!", "Переустановите программу!")
            win.destroy()
        else:
            create()
    except FileNotFoundError:
        win.withdraw()
        mb.showerror("Ошибка!", "Программа не установлена!")
        win.destroy()