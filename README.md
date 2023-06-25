# Instant-Messaging-Application-centralized-and-p2p
A multi-functional instant messaging application developed using Python socket UDP. Centralized version is fully functional by incorporating Sqlite3 db and Tkinter UI design. P2P version is for proof-of-concept, a terminal-based application. 

# Centralized
A multi-functional instant messaging applicatio developed using Python socket UDP and Tkinter. The features include account registration and login. After successful login, users can view online users and engage in conversations with other online users in the chat room. It supports both private messaging and group messaging, allowing users to send text, emojis, and files, among other functionalities.

- Model structure:

  ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/41d482bc-e767-4756-ba5d-3c5d47ecb9ba)

- Advantages:
  - Simple structure and code implementation.
  - Client file can be lightweight.
  - No propagating delay issue.

- Disadvantages:
  - Single point failure of server can impact the entire network. 
  - The entire network performance is limited by the bandwidth of the server.
  - Data privacy concern as the server must have the client’s data to offer the service.  

- Feature list:
  - Account Registration and Login: Users can register an account and log in to the chat room.
  - Display of Online Users: The chat room interface displays a list of currently online users.
  - Group Chat and Private Messaging: Users can engage in group discussions within the chat room. Additionally, users have the option to initiate private conversations with specific individuals.
  - Sending Text Messages and Emojis: Users can send text messages to the chat room, contributing to ongoing conversations. The chat room also supports the transmission of emojis, adding visual elements to the messages.
  - File Sharing: Users can share files with other participants in the chat room. This feature allows for the exchange of various file types.

- Application Demo:
  - Login page:

    ![1687668888970](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/10151db7-9d68-47f7-8025-36b2ca8e92f4)
  
  - Registeration page:

    ![1687669645359](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/b01d0cc0-5a27-4874-a046-8cf66faa4b56)
  
  - Chatroom page:

    ![1687673734905](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/12d29725-b692-4089-9ebd-174cddb66794)

# Decentralized - p2p
A multi-functional instant messaging terminal application developed using Python multithreading socket programming. The chat system allows users to join an online community that is grouped by geographical proxmity or interest. When the users launch chat client, it obtains its geographical location, interest of the user, and the user id. Once the chat client connects to the "network", the user can join a group chat with users who are in geographical proximity or users with matching interest. It also supports both private messaging and group messaging.

- Model structure:
  
  - The simple ring type

  ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/b58ab3da-d731-4f7a-8c36-3e0730b8f7c6)

- Advantages:
  - Robust against single-point failure.
  - Client file can be lightweight.
  - No propagating delay issue.


- Disadvantages:
  - Message overhead.
  - Complicated coding structure. 
  - Propagation delay and data consistency issues.

- Feature list:
  - Display online users (command: /list-users)
  - Send group message
  - Send private message (command: /send-private-message [userID] [message])
  - Display current geo location (command: /list-geo)
  - Join geo based chat group within specified distance (command: /join-geo [radius])
  - Join interest based chat group (command: /join-interest)
  - Display whether a user has joined an interest based or geo based chat and a list of users in the current group (command: /status)

- Application Demo:
  - Connection stage (Demo based on 3-nodes ring structure)
    
    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/8d3ac0f6-a19c-4601-99aa-644b9590f7d1)

  - Lobby Chat (All)

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/987cec41-e0f5-4589-8d34-9601e1b44cc4)


  - Display online users

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/36d116a4-5e14-43f4-b4b8-6cd2e223ecdc)

  - Private messeging

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/a67f8a3d-0c98-466f-a8a6-74861247b2ee)

  - Display geo location

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/197c4545-286e-4f60-b69f-6d241c370801)

  - Join geo based chat group

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/5e3193ad-bf57-429a-9e30-e45cfc383cee)

  - Join interest based chat group

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/88fe148a-5463-4b3b-bae4-4d13815909f9)

  - Display whether a user has joined an interest based or geo based chat and a list of users in the current group

    ![image](https://github.com/yuantian94/Instant-Messaging-Application-centralized-and-p2p/assets/13746207/d85684c2-9bcc-4044-aff2-c4edd2060aaf)
