"""
Author: Yuan Tian
Copyright (c) 2022 by Yuan Tian, All Rights Reserved.
Function: chat room application
"""


import socket
import threading
import time
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Treeview
from stickers import *
from login import *
from register import *

'''
    sock
    server
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
server = ('127.0.0.1', 9999)


class ChatClient():
    def __init__(self, name, scr1, scr2, fri_list, obj_emoji):
        self.name = name
        self.scr1 = scr1
        self.scr2 = scr2
        self.fri_list = fri_list
        self.obj_emoji = obj_emoji

    def toSend(self, *args):
        self.msg = self.scr2.get(1.0, 'end').strip()
        self.send(self.msg)
        if self.msg != '':
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.scr1.configure(state=NORMAL)
            self.scr1.insert("end", "{} {}:\n".format(self.name, now_time), 'green')
            self.scr1.insert("end", self.msg + '' + '\n')
            self.scr1.see(END)
            self.scr2.delete('1.0', 'end')
            self.scr1.config(state=DISABLED)
            print(f'{self.name}: message sent', self.msg.strip())
            return "break"

    def toPrivateSend(self, *args):
        self.msg = self.scr2.get(1.0, 'end').strip()
        self.scr2.delete('1.0', 'end')
        send_type, send_file = self.private_send(self.msg)
        if self.msg != '' and self.fri_list.selection() != ():
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.scr1.configure(state=NORMAL)
            tar_name = self.fri_list.selection()[0]
            print('Private Chat Username:', tar_name)
            self.scr1.insert("end", "{} {}:\n".format(self.name, now_time), 'green')
            if send_type == 'text':
                self.scr1.insert("end", f'{self.msg}')
                self.scr1.insert("end", f'  |private {tar_name}\n', 'zise')
                self.scr1.see(END)
                self.scr2.delete('1.0', 'end')
                self.scr1.config(state=DISABLED)
                print(f'{self.name}：message sent', self.msg, '[private]')
            else:
                self.scr1.insert("end", f'{send_file} file sent, waiting for receiving', 'shengzise')
                self.scr1.insert("end", f' |host:{tar_name}\n', 'zise')
                self.scr1.see(END)
                print(f'{self.name}：file sent', send_file, '[private]')

    def Get_File(self, filename):
        fpath, tempfilename = os.path.split(filename)
        fname, extension = os.path.splitext(tempfilename)
        return fpath, fname, extension, tempfilename

    def send_file(self, fileType, fileName, filePath):
        message = {}
        message["chat_type"] = "private"
        message["message_type"] = "ask-file"
        message["file_type"] = fileType
        message["file_name"] = fileName
        message["send_user"] = self.name
        message["recv_user"] = self.fri_list.selection()[0]
        message["content"] = filePath
        jsondata = json.dumps(message, ensure_ascii=False)
        sock.sendto(jsondata.encode('utf-8'), server)

    def cut_data(self, fhead, data):
        for i in range(fhead // 1024 + 1):
            time.sleep(0.0000000001)  
            if 1024 * (i + 1) > fhead: 
                sock.sendto(data[1024 * i:], server)  
                print('No.' + str(i + 1) + ' file send')
            else:
                sock.sendto(data[1024 * i:1024 * (i + 1)], server)
                print('No.' + str(i + 1) + ' file send')

    def succ_recv(self, filename, sourcename):
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.scr1.configure(state=NORMAL)
        self.scr1.insert("end", "{} {}:\n".format(self.name, now_time), 'green')
        self.scr1.insert("end", f'Received {filename} file', 'shengzise')
        self.scr1.insert("end", f' |from:{sourcename}\n', 'zise')
        self.scr1.see(END)
        self.scr1.config(state=DISABLED)

    def succ_send(self, recv_user, filename):

        self.scr1.configure(state=NORMAL)
        self.scr1.insert("end", f'{filename}', 'shengzise')
        self.scr1.insert("end", f' |sent to {recv_user}\n', 'zise')
        self.scr1.see(END)
        self.scr1.config(state=DISABLED)
        print(f'{self.name}：{filename}--file sent to', recv_user)

    def send(self, msg):

        if msg != '':
            message = {}
            message["chat_type"] = "normal"
            message["message_type"] = "text"
            message["send_user"] = self.name
            message["content"] = msg.strip()
            jsondata = json.dumps(message, ensure_ascii=False)
            sock.sendto(jsondata.encode('utf-8'), server)

    def private_send(self, msg):
        fpath, fname, extension, tempfilename = self.Get_File(msg) 
        # print(extension)
        if self.fri_list.selection() == ():
            messagebox.showwarning(title='Error', message='Invalid receiver')

        elif str(extension) in ('.py', '.doc', '.txt', '.docx'):  
            self.send_file('normal-file', tempfilename, msg)
            return 'normal-file', tempfilename

        elif str(extension) in ('.jpg', '.png'):
            self.send_file('image', tempfilename, msg)
            return 'image', tempfilename

        elif str(extension) in ('.avi', '.mp4'):
            self.send_file('video', tempfilename, msg)
            return 'video', tempfilename

        else:
            message = {}
            message["chat_type"] = "private"
            message["message_type"] = "text"
            message["send_user"] = self.name
            message["recv_user"] = self.fri_list.selection()[0]
            message["content"] = msg.strip()
            jsondata = json.dumps(message, ensure_ascii=False)
            sock.sendto(jsondata.encode('utf-8'), server)
            return 'text', ''

    def recv(self):
        message = {}
        message["message_type"] = "init_message"
        message["content"] = self.name
        json_str = json.dumps(message, ensure_ascii=False)
        sock.sendto(json_str.encode('utf-8'), server)
        while True:
            data = sock.recv(1024)
            source = data.decode('utf-8')
            json_data = json.loads(data.decode('utf-8'))
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.scr1.configure(state=NORMAL)
            if json_data['message_type'] == "init_message":
                self.scr1.insert("end", f'Welcome {json_data["content"]} enters chatroom' + '\n', 'red')
                print(json_data["online_user"])
                user_list = eval(json_data["online_user"])
                for user in user_list:
                    if str(user) not in self.fri_list.get_children() and str(user) != self.name: 
                        self.fri_list.insert('', 2, str(user), text=str(user).center(24), values=("1"), tags='Other users')
                print(json_data["content"] + 'Enter chatroom...')

            elif json_data['message_type'] == "leave_message":
                self.scr1.insert("end", f'{json_data["content"]} left chatroom...' + '\n', 'red')
                if json_data["content"] in self.fri_list.get_children():
                    self.fri_list.delete(json_data["content"])
                print(json_data["content"] + 'left chatroom...')

            elif json_data['chat_type'] == "normal":
                if json_data['message_type'] == "text":
                    self.scr1.insert("end", "{} {}:\n".format(json_data['send_user'], now_time), 'green')
                    self.scr1.insert("end", json_data['content'] + '\n')

                elif json_data['message_type'] == "stickers":
                    self.scr1.configure(state=NORMAL)
                    self.scr1.insert("end", "{} {}:\n".format(json_data['send_user'], now_time), 'green')
                    dics = self.obj_emoji.dics
                    if json_data['content'] in dics:
                        mes = json_data['content']
                        self.scr1.image_create(END, image=dics[mes])
                        self.scr1.insert("end", '\n', 'zise')
                        self.scr1.see(END)
                    self.scr1.config(state=DISABLED)
                    print(f'Received {json_data["send_user"]} emoji', json_data['content'])

            elif json_data['chat_type'] == "private":
                if json_data['message_type'] == "text":
                    self.scr1.insert("end", "{} {}:\n".format(json_data['send_user'], now_time), 'green')
                    self.scr1.insert("end", json_data['content'])
                    self.scr1.insert("end", f'  |private\n', 'zise')
                    print(f'[private]receive {json_data["send_user"]} message：', json_data['content'])

                elif json_data['message_type'] == "stickers":

                    self.scr1.configure(state=NORMAL)
                    self.scr1.insert("end", "{} {}:\n".format(json_data['send_user'], now_time), 'green')
                    dics = self.obj_emoji.dics
                    if json_data['content'] in dics:
                        mes = json_data['content']
                        self.scr1.image_create(END, image=dics[mes])
                        self.scr1.insert("end", f'  |private\n', 'zise')
                        self.scr1.see(END)
                    self.scr1.config(state=DISABLED)
                    print(f'[private]receive {json_data["send_user"]} emoji：', json_data['content'])

                elif json_data['message_type'] == "ask-file":
                    fileType = json_data["file_type"]
                    self.scr1.configure(state=NORMAL)
                    self.scr1.insert("end", "{} {}:\n".format(json_data["send_user"], now_time), 'green')
                    self.scr1.insert("end", f'sending {fileType} to you...\n', 'shengzise')
                    self.scr1.see(END)
                    self.scr1.config(state=DISABLED)

                    flag = messagebox.askyesno(title='Error',
                                               message=f'{json_data["send_user"]} sent {fileType} to you\nConfirm?')
                    if flag:
                        json_data['message_type'] = "isRecv"
                        json_data['isRecv'] = "true"
                        jsondata = json.dumps(json_data, ensure_ascii=False)
                        sock.sendto(jsondata.encode('utf-8'), server)

                    else:
                        json_data['message_type'] = "isRecv"
                        json_data['isRecv'] = "false"
                        jsondata = json.dumps(json_data, ensure_ascii=False)
                        sock.sendto(jsondata.encode('utf-8'), server)
                        self.scr1.configure(state=NORMAL)
                        self.scr1.insert("end", "{} {}:\n".format(self.name, now_time), 'green')
                        self.scr1.insert("end", f'you rejected {fileType}', 'shengzise')
                        self.scr1.insert("end", f' |from:{json_data["send_user"]}\n', 'zise')
                        self.scr1.see(END)
                        self.scr1.config(state=DISABLED)

                elif json_data['message_type'] == "isRecv":
                    if json_data['isRecv'] == "true":
                        if json_data["file_type"] == 'normal-file':
                            f = open(json_data["content"], 'rb')  
                            data = f.read()
                            fhead = len(data)
                            print('File size:', fhead)

                            message = {}
                            message["chat_type"] = "private"
                            message["message_type"] = "file-data"
                            message["file_length"] = str(fhead)
                            message["file_name"] = json_data["file_name"]
                            message["send_user"] = json_data["send_user"]
                            message["recv_user"] = json_data["recv_user"]
                            message["content"] = ''
                            jsondata = json.dumps(message, ensure_ascii=False)
                            sock.sendto(jsondata.encode('utf-8'), server)

                            print('Sending...')
                            self.cut_data(fhead, data)
                            print('Send complete!')
                            f.close()
                    else:
                        self.scr1.insert("end", "{} {}:\n".format(json_data["send_user"], now_time), 'green')
                        self.scr1.insert("end", f"{json_data['file_name']} rejected by the other side \n", 'chengse')
                        self.scr1.see(END)

                elif json_data['message_type'] == "file-data":
                    print('Receiving')
                    filename = json_data['file_name']
                    data_size = int(json_data['file_length'])
                    print('File size:' + str(data_size))
                    recvd_size = 0
                    data_total = b''
                    j = 0
                    while not recvd_size == data_size:
                        j = j + 1
                        if data_size - recvd_size > 1024:
                            data, addr = sock.recvfrom(1024)
                            recvd_size += len(data)
                            print('No.' + str(j) + ' data Received')
                        else:  # 最后一片
                            data, addr = sock.recvfrom(1024)
                            recvd_size = data_size
                            print('No.' + str(j) + ' data Received')
                        data_total += data

                    f = open(filename, 'wb')
                    f.write(data_total)
                    f.close()
                    print(filename, 'Received!')
                    self.succ_recv(filename, json_data["send_user"])
                    message = {}
                    message["chat_type"] = "private"
                    message["message_type"] = "Recv_msg"
                    message["Recv_msg"] = "true"
                    message["file_length"] = json_data['file_length']
                    message["file_name"] = json_data["file_name"]
                    message["send_user"] = json_data["recv_user"]
                    message["recv_user"] = json_data["send_user"]
                    jsondata = json.dumps(message, ensure_ascii=False)
                    sock.sendto(jsondata.encode('utf-8'), server)

                elif json_data['message_type'] == "Recv_msg":
                    if json_data['Recv_msg'] == "true":
                        recv_user = json_data['recv_user']
                        filename = json_data['file_name']
                        self.succ_send(recv_user, filename)


class ChatUI():
    def __init__(self, root):
        self.root = root

    def JieShu(self):
        flag = messagebox.askokcancel(title='Notification', message='Exit Chatroom?')
        if flag:
            message = {}
            message["message_type"] = "leave_message"
            message["content"] = self.name
            jsondata = json.dumps(message, ensure_ascii=False)
            sock.sendto(jsondata.encode('utf-8'), server)
            sys.exit(0)

    def openfile(self):
        r = askopenfilename(title='FileOpen', filetypes=[('All File', '*.*'), ('text file', '.txt'), ('python', '*.py *.pyw')])
        self.scr2.insert(INSERT, r)

    def chat(self, usename):
        self.name = usename
        self.root.title('chatroom--username:' + self.name)
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = 1120
        h = 720
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry("%dx%d+%d+%d" % (w, h, (x + 160), y))
        self.root.iconbitmap(r'images/icon/chat.ico')

        self.root.resizable(0, 0)

        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

        self.root.tk.call('tk', 'scaling', ScaleFactor / 75)

        self.root.resizable(1, 1)
        self.scr1 = scrolledtext.ScrolledText(self.root, height=18, font=('times', 13))
        self.scr1.tag_config('green', foreground='#008C00', font=('times', 10))
        self.scr1.tag_config('red', foreground='red')
        self.scr1.tag_config('zise', foreground='#aaaaff')
        self.scr1.tag_config('shengzise', foreground='#9d4cff')
        self.scr1.tag_config('chengse', foreground='#ff7f27')

        # 创建树形列表
        self.fri_list = Treeview(self.root, height=30, show="tree")
        self.fri_list.insert('', 0, 'online_user', text='Online users'.center(10, '-'), values=("1"), tags='Online users')
        if self.name not in self.fri_list.get_children():
            self.fri_list.insert('', 1, 'me', text=self.name.center(24), values=("1"), tags='self')
        self.fri_list.grid(row=1, column=2, rowspan=7, sticky=N)
        self.fri_list.tag_configure('Online users', foreground='#aa5500', font=('times', 13))
        self.fri_list.tag_configure('self', foreground='red', font=('times', 10))
        self.fri_list.tag_configure('Other users', font=('times', 10))

        self.scr1.grid(row=1, column=1)
        l0 = Label(self.root, text='')
        l0.grid(row=2)
        l1 = Label(self.root, text='Type in message content：')
        l1.grid(row=3, column=1)
        self.scr2 = scrolledtext.ScrolledText(self.root, height=6, font=('times', 13))
        self.scr2.grid(row=4, column=1)
        l2 = Label(self.root, text='')
        l2.grid(row=5)
        tf = Frame(self.root)
        tf.grid(row=6, column=1)

        obj_emoji = Emoji(self.root, self.send_mark)
        chat = ChatClient(self.name, self.scr1, self.scr2, self.fri_list, obj_emoji)

        b0 = Button(tf, text=' Emoji ', command=obj_emoji.express)
        b0.grid(row=1, column=0, padx=20)
        b1 = Button(tf, text=' All ', command=chat.toSend)
        b1.grid(row=1, column=1, padx=20)
        b4 = Button(tf, text=' Private ', command=chat.toPrivateSend)
        b4.grid(row=1, column=2, padx=20)
        b2 = Button(tf, text=' SendFile ', command=self.openfile)
        b2.grid(row=1, column=3, padx=20, pady=20)
        b3 = Button(tf, text=' Email ', command='')
        b3.grid(row=1, column=4, padx=20)
        b4 = Button(tf, text=' FTP ', command='')
        b4.grid(row=1, column=5, padx=20)
        b5 = Button(tf, text=' LoginFTP ', command='')
        b5.grid(row=1, column=6, padx=20)
        b6 = Button(tf, text=' Exit ', command=self.JieShu)
        b6.grid(row=1, column=7, padx=20)

        tr = threading.Thread(target=chat.recv, args=(),
                              daemon=True)

        tr.start()
        self.root.protocol("WM_DELETE_WINDOW", self.JieShu)

    def send_mark(self, exp, dics):
        stick_code = exp
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.scr1.configure(state=NORMAL)
        self.scr1.insert("end", "{} {}:\n".format(self.name, now_time), 'green')
        message = {}
        message["message_type"] = "stickers"
        message["send_user"] = self.name
        message["content"] = stick_code

        if self.fri_list.selection() != () and self.fri_list.selection()[0] != 'me':
            message["chat_type"] = "private"
            message["recv_user"] = self.fri_list.selection()[0]
            jsondata = json.dumps(message, ensure_ascii=False)
            sock.sendto(jsondata.encode('utf-8'), server)
            self.scr1.image_create(END, image=dics[stick_code])
            self.scr1.insert("end", f'  |private{self.fri_list.selection()[0]}\n', 'zise')
            print(f'message:{stick_code} sent![private {self.fri_list.selection()[0]}]')
        else:
            message["chat_type"] = "normal"
            jsondata = json.dumps(message, ensure_ascii=False)
            sock.sendto(jsondata.encode('utf-8'), server)
            self.scr1.image_create(END, image=dics[stick_code])
            print(f'message:{stick_code} sent！')
            self.scr1.insert(END, '\n')
        self.scr1.see(END)
        self.scr1.config(state=DISABLED)


if __name__ == '__main__':
    root = Tk()
    Main = ChatUI(root)
    Login(Register, Main.chat, root)
    root.mainloop()
