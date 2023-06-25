import random
import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from need_module import json,ctypes,sys,os



class Login(object):
    def __init__(self, Register,Chat,master=None):
        self.root = master  # define internal variable root
        self.root.title('Login Page')
        self.Register=Register
        self.Chat=Chat
        self.root.iconbitmap(r'images/icon/login.ico')  # top left icon


        # set window: middle
        sw = self.root.winfo_screenwidth()  # Horizontal
        sh = self.root.winfo_screenheight()  # Vertical
        w = 690
        h = 535
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry("%dx%d+%d+%d" % (w, h, (x + 160), y))
        self.root.resizable(0, 0)  # fixed window size
        
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        
        self.root.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.creatlogin()

    def creatlogin(self):
        self.fr2 = Frame(self.root)
        self.fr2.pack()
        self.fr1 = Frame(self.root)
        self.fr1.pack(pady=10)

        self.benner_list = ['images/benner/banner-1.jpg', 'images/benner/banner-2.jpg', 'images/benner/banner-3.jpg',
                            'images/benner/banner-4.jpg', 'images/benner/banner-5.jpg', 'images/benner/banner-6.jpg', ]
        self.benner_img = random.choice(self.benner_list) 

        # pic size：690x300
        self.pic = Image.open(self.benner_img)
        self.login_benner = ImageTk.PhotoImage(self.pic)

        # tag benner pic
        self.imgLabel = Label(self.fr2, image=self.login_benner)
        self.imgLabel.pack()

        # tag user and password
        self.label_usr = Label(self.fr1, text="Username: ")
        self.label_usr.grid(row=0, column=0, pady=10)
        self.label_pwd = Label(self.fr1, text="Password: ")
        self.label_pwd.grid(row=1, column=0)

        # textbox username
        self.var_usr_name = StringVar()
        self.entry_name = Entry(self.fr1, textvariable=self.var_usr_name)
        self.entry_name.grid(row=0, column=1)
        self.entry_name.focus_set()  # obtain focus
        # textbox pass
        self.var_usr_pwd = StringVar()
        self.entry_pwd = Entry(self.fr1, textvariable=self.var_usr_pwd, show="*")
        self.entry_pwd.grid(row=1, column=1)

        self.saved_msg()

        self.fr3 = Frame(self.root)
        self.fr3.pack()
        self.rd_login = IntVar()
        self.rd_Passwd = IntVar()
        self.checkboxLogin = Checkbutton(self.fr3, text="Auto-login", variable=self.rd_login)
        self.checkboxPasswd = Checkbutton(self.fr3, text="Remember password", variable=self.rd_Passwd)

        self.la = Label(self.fr3, width=5)
        self.la.grid(row=0, column=0)
        self.checkboxLogin.grid(row=0, column=1)
        self.checkboxPasswd.grid(row=0, column=2)
        # login
        self.root.bind('<Return>', self.check_login)  

        self.bt_login = Button(self.fr3, text="Login", command=lambda: self.check_login())
        self.bt_login.grid(row=1, column=1, pady=5)
        self.bt_quit = Button(self.fr3, text="Exit", command=sys.exit)
        self.bt_quit.grid(row=1, column=2)

        # # bottom
        self.fr4 = Frame(self.root)
        self.fr4.pack(side='bottom')

        self.bt_register = Button(self.fr4, text="Register", relief=FLAT, bg='#f0f0f0', command=self.login_win_close)
        self.bt_register.pack(side='left', anchor='s')
        self.la2 = Label(self.fr4, width=150)
        self.la2.pack()
        self.tsLabel2 = Label(self.fr4, text="Chatroom page", fg="red")
        self.tsLabel2.pack(side='right', anchor='s', pady=5)

    def red_msg(self):
        if self.rd_Passwd.get() == 1:
            # JSON
            new_usr = {
                'username': self.var_usr_name.get(),
                'password': self.var_usr_pwd.get()
            }
            with open('usr.json', 'w') as wp:
                json.dump(new_usr, wp)

    def saved_msg(self):
        self.saved_name = ''
        self.saved_pwd = ''
        if os.path.exists('usr.json'):
            with open('usr.json', 'r') as fp:
                json_file = json.load(fp)
                json_str = json.dumps(json_file)

                json_date = json.loads(json_str)
                print(json_date)
                self.saved_name = json_date['username']
                self.saved_pwd = json_date['password']
                # print(self.saved_name,self.saved_pwd)
        if self.saved_name != '':
            self.entry_name.insert(END, self.saved_name)
            self.entry_pwd.insert(END, self.saved_pwd)

    def login_win_close(self):

        self.fr1.destroy()
        self.fr2.destroy()
        self.fr3.destroy()
        self.fr4.destroy()
        self.Register(Login,self.Chat,self.root)

    def check_login(self, *args):
        global usr_name
        self.usr_name = self.var_usr_name.get()
        self.usr_pwd = self.var_usr_pwd.get()
        conn = sqlite3.connect('yonghu.db')
        cursor = conn.cursor()

        if self.usr_name == '' or self.usr_pwd == '':
            messagebox.showwarning(title='Error', message="Empty input")

        else:
            # Query：
            cursor.execute('select username from user')
            values = cursor.fetchall()
            cursor.execute('select password from user where username="%s"' % self.usr_name)
            # querylist：
            values2 = cursor.fetchall()
            userList = []
            for i in values:
                # print(i[0])
                userList.append(i[0])

            if self.usr_name in userList:
                if self.usr_pwd == values2[0][0]:
                    messagebox.showinfo(title='Notification', message='Welcome Back!')
                    self.root.unbind('<Return>')
                    self.red_msg()
                    print('Remember Password?:',self.rd_Passwd.get())
                    self.fr1.destroy()
                    self.fr2.destroy()
                    self.fr3.destroy()
                    self.fr4.destroy()
                    self.Chat(self.usr_name)

                else:
                    messagebox.showerror(title='Error', message="Invalid username or password")
            else:
                messagebox.showerror(title='Error', message="No such username")
            cursor.close()
            conn.close()

            return 'break'