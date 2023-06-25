import socket
from need_module import json,logging,time


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket definition
    s_addr = ('127.0.0.1', 9999)
    s.bind(s_addr)  # IP address and port

    logging.info('UDP Server on %s:%s...', s_addr[0], s_addr[1])

    user = {}  # dict{name:addr}

    print('----------Server Initializing-----------')
    print('Bind UDP on ' + str(s_addr))
    print('Waiting on data...')
    while True:

        try:

            data, addr = s.recvfrom(1024)
            # print(data)
            json_data=json.loads(data.decode('utf-8'))
            print(json_data)

            if json_data['message_type']=="init_message":
                if json_data['content'] not in user:
                    user[json_data['content']]=addr
                    user_list=[i for i in user.keys()]
                    json_data['online_user'] = f'{user_list}'
                    json_str = json.dumps(json_data, ensure_ascii=False)
                    for address in user.values():
                        s.sendto(json_str.encode('utf-8'), address)  # send data and address to client
                    print(json_data['content'] + 'enter Chatroom')
                    print(f'OnlineUsers{user_list}')

            elif json_data['message_type']=="leave_message":
                if json_data['content'] in user:
                    user.pop(json_data['content'])
                    user_list = [i for i in user.keys()]
                    for address in user.values():
                        s.sendto(data, address) # send data and address to client
                    print(json_data['content']+'left Chatroom')
                    print(f'OnlineUsers{user_list}')
                    continue

            elif json_data['chat_type'] == "normal":
                if json_data['message_type'] != "file":
                    for address in user.values():
                        if address != addr:
                            s.sendto(data, address)  # send data and address to client

            elif json_data['chat_type'] == "private":
                recv_user = json_data['recv_user']
                send_user = json_data['send_user']
                if json_data['message_type'] != "file-data":
                    s.sendto(data, user[recv_user])  # send data and address to client

                else:
                    filename = json_data['file_name']
                    data_size = int(json_data['file_length'])
                    print('File Size:' + str(data_size))
                    recvd_size = 0
                    data_total = b''
                    j = 0
                    while not recvd_size == data_size:
                        j = j + 1
                        if data_size - recvd_size > 1024:
                            data, addr = s.recvfrom(1024)
                            recvd_size += len(data)
                            print('No.' + str(j) + ' data Received')
                        else:  # last one
                            data, addr = s.recvfrom(1024)
                            recvd_size = data_size
                            print('No.' + str(j) + ' data Received')
                        data_total += data


                    fhead = len(data_total)
                    message = {}
                    message["chat_type"] = "private"
                    message["message_type"] = "file-data"
                    message["file_length"] = str(fhead)
                    message["file_name"] = json_data["file_name"]
                    message["send_user"] = json_data['send_user']
                    message["recv_user"] = json_data['recv_user']
                    message["content"] = ''
                    jsondata = json.dumps(message, ensure_ascii=False)
                    s.sendto(jsondata.encode('utf-8'), user[recv_user])

                    print('Sending...')
                    for i in range(len(data_total) // 1024 + 1):
                        time.sleep(0.0000000001)  # in case too fast
                        if 1024 * (i + 1) > len(data_total):
                            s.sendto(data_total[1024 * i:], user[recv_user])  # send last piece of data
                            print('No.' + str(i+1) + ' data send')
                        else:
                            s.sendto(data_total[1024 * i:1024 * (i + 1)], user[recv_user])
                            print('No.' + str(i+1) + ' data send')

                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print('%s: "%s" Send Complete! from %s:%s [host:%s] at %s' % (send_user, filename, addr[0], addr[1], user[recv_user], now_time))

        except ConnectionResetError:
            logging.warning('Someone left unexpectedly.')


if __name__ == '__main__':
    main()
