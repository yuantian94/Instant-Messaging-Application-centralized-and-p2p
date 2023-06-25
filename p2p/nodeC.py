import queue
import socket
import threading
import time
import urllib.request
import json
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
with urllib.request.urlopen("https://geolocation-db.com/json") as url:
    data = json.loads(url.read().decode())

peer = []
message_Q = queue.Queue(maxsize=30)
srcID = '2'
nickname = input('Input your nickname: ')
interest = input('Input your interest: ').lower()
location = [data['latitude'],data['longitude']]
access = 0
geolist = []
topiclist = []
mode = 0
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return int(c * r)

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            print('Waiting for peer connection')
            s.connect(('localhost', 5004))
            print('Connected.')
            peer.append(['localhost',5004])
            break
        except:
            time.sleep(2)
    def write():
        while True:
            try:
                global mode
                global location
                global interest
                user_input = input('')
                check_input = user_input.split()

                if check_input[0] == '/list-users': #list-user
                    if len(check_input) != 1:
                        print("Invalid instruction format!")
                    else:
                        op = '1'
                        message = f"{op} {srcID} [name:{nickname}]-[userID:{srcID}]"
                        s.send(message.encode('ascii'))

                elif check_input[0] == '/send-private-message':
                    if len(check_input) < 2:
                        print("Invalid instruction format!")
                    else:
                        dstID = check_input[1]
                        if dstID != srcID:
                            op = '2'
                            message_data = check_input[2:]
                            message_data = ' '.join(message_data)
                            successbit = '0'
                            message = f"{op} {srcID} {dstID} {successbit} {nickname}: {message_data}"
                            s.send(message.encode('ascii'))
                        else:
                            print("Invalid ID!")

                elif check_input[0] == '/list-geo':
                    print(f"Latitude:{data['latitude']} Longitude:{data['longitude']} City:{data['city']}")

                elif check_input[0] == '/join-geo':
                    if len(check_input) == 1:
                        if len(geolist) == 0:
                            print("You have never joined a geo group so far!")
                        else:
                            mode = 1
                            print(f"You switched to geo group!")
                    elif len(check_input) == 2:
                        if len(geolist) != 0:
                            op = '5'
                            delete_list = geolist
                            delete_list = ' '.join(delete_list)
                            delete_message = f"{op} {srcID} {delete_list}"
                            s.send(delete_message.encode('ascii'))
                            geolist.clear()

                        time.sleep(2)
                        op = '3'
                        mode = 1
                        print(f"You switched to geo group!")
                        round = 1
                        new_list = []
                        new_list.append(srcID)
                        new_list = ' '.join(new_list)
                        lati = location[0]
                        long = location[1]
                        distance = check_input[1]
                        message = f"{op} {srcID} {round} {lati} {long} {distance} {new_list}"
                        s.send(message.encode('ascii'))
                    else:
                        print("Invalid instruction format!")

                elif check_input[0] == '/join-interest':
                    mode = 2
                    if len(check_input) == 1:
                        if len(topiclist) == 0:
                            op = '6'
                            interestlist = topiclist
                            interestlist.append(srcID)
                            interestlist = ' '.join(interestlist)
                            round = 1
                            message = f"{op} {srcID} {round} {interest} {interestlist}"
                            s.send(message.encode('ascii'))
                            print(f"You switched to interest group!")

                elif check_input[0] == '/status':
                    op = '8'
                    geo_info = 'place_holder'
                    topic = 'place_holder'
                    interest_info = 'place_holder'
                    if len(geolist) != 0:
                        geo_info = ','.join(geolist)
                    if len(topiclist) != 0:
                        topic = interest
                        interest_info = ','.join(topiclist)

                    message = f"{op} {srcID} {geo_info} {topic} {interest_info}|"
                    s.send(message.encode('ascii'))

                else:
                    if mode == 0:
                        op = '0'
                        message = f"{op} {srcID} {nickname} {srcID} {user_input}"
                        s.send(message.encode('ascii'))
                    elif mode == 1:
                        op = '4'
                        message = f"{op} {srcID} {nickname} {srcID} {user_input}"
                        s.send(message.encode('ascii'))

                    elif mode == 2:
                        op = '7'
                        message = f"{op} {srcID} {nickname} {srcID} {user_input}"
                        s.send(message.encode('ascii'))
            except:
                print("An send error occured!")
                s.close()
                break
    def propagate():
        while True:
            global topiclist
            if not message_Q.empty():
                message = message_Q.get()
                check_message = message.split()
                op = check_message[0]
                try:
                    if op == '0' or op == '2' or op =='3' or op == '4' or op == '5' or op == '6'or op == '7':
                        s.send(message.encode('ascii'))

                    elif op == '1': #list-user
                        data = check_message[2:]
                        data.append(f"[name:{nickname}]-[userID:{srcID}]")
                        data = ' '.join(data)
                        message = '{} {} {}'.format(check_message[0], check_message[1],data)
                        s.send(message.encode('ascii'))

                    elif op == '8': #message = f"{op} {srcID} {geo_info} {topic} {0,1}|"
                        geo_info = check_message[2].split(',')
                        if len(geo_info) == 1 and len(geolist) != 0 and geo_info[0] == 'place_holder':
                            check_message[2] = ','.join(geolist)
                        if len(topiclist) != 0:
                            topic = check_message[3].split(',')
                            if topic[0] == 'place_holder':
                                check_message[3] = interest
                                users = ','.join(topiclist)
                                users_info = f"{users}|"
                                check_message[4] = users_info
                            else:
                                if interest not in topic:
                                    topic.append(interest)
                                    users = ','.join(topiclist)
                                    check_message[4] = "{}{}".format(check_message[4],f"{users}|")
                                    check_message[3] = ','.join(topic)
                        message = f"{check_message[0]} {check_message[1]} {check_message[2]} {check_message[3]} {check_message[4]}"
                        s.send(message.encode('ascii'))

                except:
                    print("An propagate error occured!")
                    s.close()
                    break
    try:
        write_thread = threading.Thread(target=write)
        write_thread.start()
    except:
        print("An error on client")
    try:
        propagate_thread = threading.Thread(target=propagate)
        propagate_thread.start()
    except:
        print("An error on client")

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 5003))

    instructions = '\nInstructions:\n' \
                   + '[/list-users] to list all online users\n' \
                   + '[/send-private-message <userid>] to send private message\n' \
                   + '[/list-geo] displays the current geo location\n' \
                   + '[/join-geo <distance>] broadcasting geo based chatting within the specified distance\n' \
                   + '[/join-interest] joins interest based group\n' \
                   + '[/status] group status' \
                   + '\n'
    print(instructions)

    try:
        s.listen(1)
        c, a = s.accept()
        print(f'Connected: {a}')
        while True:
            try:

                global mode
                global location
                global interest
                message = c.recv(2048).decode('ascii')
                check_message = message.split()

                if check_message[0] == '1':
                    if check_message[1] == srcID:
                        print(f"Online users: {check_message[2:]}")

                elif check_message[0] == '8': #message = f"{op} {srcID} {geo_info} {topic} {0,1}|"
                    if check_message[1] == srcID:
                        if check_message[2].split(',')[0] != 'place_holder':
                            print(f"Geo group: {check_message[2]}")
                        else:
                            print(f"Geo group: None")
                        if check_message[3].split(',')[0] != 'place_holder':
                            topics = check_message[3].split(',')
                            users_info = check_message[4].split('|')
                            for index in range(len(topics)):
                                print(f"{topics[index]}: {users_info[index]}")

                elif check_message[0] == '2':
                    if check_message[2] == srcID:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        message_content = check_message[5:]
                        message_content = ' '.join(message_content)
                        print(f"[Private] [{current_time}] {check_message[4]}: {message_content}")
                        check_message[3] = '1'
                        message = ' '.join(check_message)
                    if check_message[1] == srcID:
                        if check_message[3] == '0':
                            print(f"The user is not online.")
                        else:
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            message_content = check_message[5:]
                            message_content = ' '.join(message_content)
                            print(f"[Private to userID:{check_message[2]}] [{current_time}] {check_message[4]}: {message_content}")
#message = f"{op} {srcID} {round} {lati} {long} {distance} {list}"

                elif check_message[0] == '3':               #geo request
                    if check_message[1] == srcID:               #Arrive the source
                        if int(check_message[2]) != 2:              #round 1 finished
                            round = int(check_message[2])+1
                            check_message[2] = str(round)
                            message = ' '.join(check_message)
                            list_to_add = check_message[6:]
                            geolist.clear()
                            for id in list_to_add:
                                geolist.append(id)
                            if not message_Q.full():
                                message_Q.put(message)

                    else:                                       #received as non-source
                        if int(check_message[2]) != 2:              #in round 1: handle the request
                            src_dist = float(check_message[5])
                            src_la = float(check_message[3])
                            src_lo = float(check_message[4])
                            comp_la = float(location[0])
                            comp_lo = float(location[1])
                            comp_dist = haversine(src_la,src_lo,comp_la,comp_lo)
                            if comp_dist <= src_dist:                   #within range
                                print(f"You were invited to a geo group created by user:{check_message[1]}")
                                append_list = check_message[6:]
                                append_list.append(srcID)
                                append_list = ' '.join(append_list)
                                message = f"{check_message[0]} {check_message[1]} {check_message[2]} {check_message[3]} {check_message[4]} {check_message[5]} {append_list}"
                                mode = 1

                        else:                                       #in round 2: get the full geo list
                            geo_append_list = check_message[6:]
                            for item in geo_append_list:
                                if item not in geolist:
                                    geolist.append(item)
                            if srcID not in geolist:
                                geolist.clear()


                elif check_message[0] == '4': #message = '{} {} {} {} {} {}'.format(op, srcID, nickname, uid, user_input)
                    if srcID in geolist:
                        if mode == 1:
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            message_content = check_message[4:]
                            message_content = ' '.join(message_content)
                            print(f"[Geo] [{current_time}] [userID:{check_message[3]}] {check_message[2]}: {message_content}")

                elif check_message[0] == '5': #message = f"{op} {srcID} {delete_list}"
                    if check_message[1] != srcID:
                        if srcID in check_message[2:]:
                            geolist.clear()
                            print("Someone in your current geo group created a new geo group. Current geo group is dismantled.")

                #message = f"{op} {srcID} {round} {interest} {interestlist}"
                elif check_message[0] == '6':               #interest request
                    if check_message[1] == srcID:               #Arrive the source
                        if int(check_message[2]) != 2:              #round 1 finished
                            round = int(check_message[2])+1
                            check_message[2] = str(round)
                            message = ' '.join(check_message)
                            list_to_add = check_message[4:]
                            topiclist.clear()
                            for id in list_to_add:
                                topiclist.append(id)
                            if not message_Q.full():
                                message_Q.put(message)

                    else:                                       #received as non-source
                        if int(check_message[2]) != 2:              #in round 1: handle the request
                            if check_message[3] == interest:                   #same interest
                                print(f"You were invited to a interest group created by user:{check_message[1]}")
                                append_list = check_message[4:]
                                append_list.append(srcID)
                                append_list = ' '.join(append_list)
                                message = f"{check_message[0]} {check_message[1]} {check_message[2]} {check_message[3]} {append_list}"
                                mode = 2
                        else:                                       #in round 2: get the full geo list
                            interest_append_list = check_message[4:]
                            for item in interest_append_list:
                                if item not in topiclist:
                                    topiclist.append(item)
                            if srcID not in topiclist:
                                topiclist.clear()

                elif check_message[0] == '7': #message = '{} {} {} {} {}'.format(op, srcID, nickname, user_input)

                    if srcID in topiclist:
                        if mode == 2:
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            message_content = check_message[4:]
                            message_content = ' '.join(message_content)
                            print(f"[{interest}] [{current_time}] [userID:{check_message[3]}] {check_message[2]}: {message_content}")


                elif check_message[0] == '0':
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    message_content = check_message[4:]
                    message_content = ' '.join(message_content)
                    print(f"[All] [{current_time}] [userID:{check_message[3]}] {check_message[2]}: {message_content}")


                if (not message_Q.full()) and (check_message[1] != srcID):
                    message_Q.put(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                c.close()
                break
    except ConnectionError:
        c.close()
        print(f'Disconnected: {a}')

client_thread = threading.Thread(target=client)
client_thread.start()

server_thread = threading.Thread(target=server)
server_thread.start()