from tkinter import *
from tkinter import filedialog, messagebox as mb
from git import Repo
import hashlib
import os
import win32api
import winreg

win = Tk()


def quit_app():
    win.destroy()
    exit()


def install(path, objects):
    if not path:
        mb.showwarning("Внимение", "Вы не выбрали путь!")
        return

    if os.path.exists(path):
        try:
            path += "/Lab2"
            if not os.path.exists(path):
                os.mkdir(path)

            if not os.path.isfile(path + "/main.py"):
                answer = mb.askyesno(title="Вопрос", message="Установка может занять некоторое время, продолжить?".format(path))

                if answer:
                    for item in objects:
                        item.destroy()

                    Repo.clone_from(url='http://user:password@github.com/KurtOleh/Lab.git', to_path=path)

                    signature = os.getlogin() + win32api.GetComputerName() + win32api.GetWindowsDirectory() + win32api.GetSystemDirectory()
                    signature += "{}{}{}".format(win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(7),
                                                 win32api.GlobalMemoryStatus()['TotalPhys'])
                    sha = hashlib.sha256(signature.encode()).hexdigest()

                    try:
                        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\KurtOlehHorobetsAngelina")
                    except OSError:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\KurtOlehHorobetsAngelina", 0, winreg.KEY_ALL_ACCESS)

                    winreg.SetValueEx(key, "Signature", 0, winreg.REG_SZ, sha)
                    key.Close()
                    win.title("Успешно")
                    Label(win, text="Программа успешно установлена!", font=("Arial 32", 12)).pack(pady=15)

                    button = Button(win, text="Завершить", font=("Arial 32", 11), width=10,  relief=FLAT,  background="#34506b", foreground="#ccc", command=quit_app())
                    button.place(x=318, y=130)
                else:
                    win.destroy()
            else:
                mb.showerror("Ошибка", "Программа уже установлена!")
                win.destroy()

        except (PermissionError, SystemExit):
            mb.showerror("Ошибка", "Отказано в доступе, выберете другой путь!")

    else:
        mb.showwarning("Внимание", "Некорректный путь. Выберете другой!")


def directory(entry):
    direction = filedialog.askdirectory()
    if direction:
        entry.delete(0, END)
        entry.insert(0, direction)


def create():
    win.title("Установщик")
    win.geometry("430x166+{0}+{1}".format(int(win.winfo_screenwidth() / 2) - 200, int(win.winfo_screenheight() / 2) - 200))
    win.resizable(False, False)

    label = Label(win, text="Установщик", font=("Arial 32", 22), bg='White', fg="Black", width=25, height=1)
    label.pack()

    msg_dir = Label(win, text="Выберите путь для установки:", font=("Arial 32", 10))
    msg_dir.place(x=10, y=50)
    entry_dir = Entry(win, width=48, textvariable=StringVar(), relief=GROOVE, font=("Arial 32", 10))
    entry_dir.insert(0, "C:/Program Files")
    entry_dir.place(x=14, y=76)

    button_dir = Button(win, text="Обзор...", font=("Arial 32", 8), width=9, relief=GROOVE, background="#fff", command=lambda: directory(entry_dir))
    button_dir.place(x=361, y=74)

    button = Button(win, text="Установить", font=("Arial 32", 11), width=10, relief=FLAT,  background="#34506b", foreground="#ccc", command=lambda: install(entry_dir.get(), objects))
    button.place(x=318, y=130)
    objects = [msg_dir, entry_dir, button_dir, button]

    win.mainloop()


if __name__ == "__main__":
    create()