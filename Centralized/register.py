import random
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from need_module import sys

class Register(object):
    def __init__(self, Login,Chat,master=None):
        self.root = master  # define internal variable root
        self.root.title('Register')
        self.Login=Login
        self.Chat=Chat

        # 设置窗口居中
        sw = self.root.winfo_screenwidth()  # Horizontal
        sh = self.root.winfo_screenheight()  # Vertical
        w = 690  # 宽
        h = 520  # 高
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry("%dx%d+%d+%d" % (w, h, (x + 160), y))
        self.root.iconbitmap(r'images/icon/register.ico')  # top left icon
        self.root.resizable(0, 0)  # fixed window size
        # ctypes.windll.shcore.SetProcessDpiAwareness(1)
        # ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        # self.root.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.creatregister()

    def creatregister(self):
        self.fr2 = Frame(self.root)
        self.fr2.pack()
        self.fr1 = Frame(self.root)
        self.fr1.pack(pady=10)

        self.benner_list = ['images/benner/banner-1.jpg', 'images/benner/banner-2.jpg', 'images/benner/banner-3.jpg',
                            'images/benner/banner-4.jpg', 'images/benner/banner-5.jpg', 'images/benner/banner-6.jpg', ]
        self.benner_img = random.choice(self.benner_list)  # random picture

        # pic size：690x300
        self.pic = Image.open(self.benner_img)
        self.register_benner = ImageTk.PhotoImage(self.pic)

        # tag benner pic
        self.imgLabel = Label(self.fr2, image=self.register_benner)
        self.imgLabel.pack()

        # tag user and password
        self.label_usr = Label(self.fr1, text="Username: ")
        self.label_usr.grid(row=0, column=0)
        self.label_pwd = Label(self.fr1, text="Password: ")
        self.label_pwd.grid(row=1, column=0, pady=5)
        self.label_repwd = Label(self.fr1, text="Confirm Password：")
        self.label_repwd.grid(row=2, column=0)

        # textbox username
        self.var_usr_name = StringVar()
        self.entry_name = Entry(self.fr1, textvariable=self.var_usr_name)
        self.entry_name.grid(row=0, column=1)
        self.entry_name.focus_set()  # obtain focus
        self.docheck1 = self.entry_name.register(self.usercheck)
        self.entry_name.config(validate='all', validatecommand=(self.docheck1, '%P'))

        # textbox pass
        self.var_usr_pwd = StringVar()
        self.entry_pwd = Entry(self.fr1, textvariable=self.var_usr_pwd, show="*")
        self.entry_pwd.grid(row=1, column=1)
        self.docheck2 = self.entry_pwd.register(self.passwordcheck)
        self.entry_pwd.config(validate='all', validatecommand=(self.docheck2, '%d', '%S'))
        # textbox confirm
        self.var_usr_repwd = StringVar()
        self.entry_repwd = Entry(self.fr1, textvariable=self.var_usr_repwd, show="*")
        self.entry_repwd.grid(row=2, column=1)

        self.fr3 = Frame(self.root)
        self.fr3.pack()
        # login
        self.root.bind('<Return>', self.reg)  # set return
        self.bt_register = Button(self.fr3, text="Register", command=lambda: self.reg())
        self.bt_register.grid(row=1, column=1, pady=5, padx=35)
        # self.la = Label(self.fr3, width=5)
        # self.la.grid(row=0, column=0)
        self.bt_quit = Button(self.fr3, text="Exit", command=sys.exit)
        self.bt_quit.grid(row=1, column=2)

        # # bottom banner
        self.fr4 = Frame(self.root)
        self.fr4.pack(side='bottom')

        self.bt_register = Button(self.fr4, text=" Go Back", relief=FLAT, bg='#f0f0f0', command=self.register_win_close)
        self.bt_register.pack(side='left', anchor='s')
        self.la2 = Label(self.fr4, width=150)
        self.la2.pack()
        self.tsLabel2 = Label(self.fr4, text="Register Page", fg="red")
        self.tsLabel2.pack(side='right', anchor='s', pady=5)

    def register_win_close(self):
        self.fr1.destroy()
        self.fr2.destroy()
        self.fr3.destroy()
        self.fr4.destroy()  # destory login page
        self.Login(Register,self.Chat,self.root)

    def usercheck(self, what):
        if len(what) > 8:
            self.la2.config(text='Username length not exceeding 16 characters', fg='red')
            return False
        return True

    def passwordcheck(self, why, what):
        if why == '1':
            if what not in '0123456789':
                self.la2.config(text='Numbers only for Password ', fg='red')
                return False
        return True

    def reg(self, *args):

        usr_name = self.var_usr_name.get()
        usr_pwd = self.var_usr_pwd.get()
        usr_repwd = self.var_usr_repwd.get()

        if usr_name == '' or usr_pwd == '' or usr_repwd == '':
            messagebox.showwarning(title='Error', message="Empty Input")

        else:
            # db
            conn = sqlite3.connect('yonghu.db')
            # Cursor：
            cursor = conn.cursor()
            # userlist：
            cursor.execute('create table if not exists user(username varchar(20),password varchar(20))')

            # check username
            cursor.execute('select username from user')
            values = cursor.fetchall()
            userList = []
            for i in values:
                # print(i[0])
                userList.append(i[0])

            if usr_name in userList:
                messagebox.showwarning('Error', 'Username Taken！')
            else:
                if usr_pwd == usr_repwd:
                    # insert data
                    cursor.execute("insert into user (username,password) values (?,?)", (usr_name, usr_repwd))
                    if (messagebox.showinfo('Register', 'Successful')):
                        self.root.unbind('<Return>')
                        self.register_win_close()
                else:
                    messagebox.showerror('Error', 'Invalid password')

            # close Cursor:
            cursor.close()
            # commit：
            conn.commit()
            # close Connection：
            conn.close()
        return 'break'
