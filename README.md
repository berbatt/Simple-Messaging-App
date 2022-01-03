# Simple-Messaging-App

This is a messaging app over TCP/IP where clients connect to the server by their nicknames <br />
and send messages to each other.

The messages send by clients are stored in a local SQL Lite Database, with the help of it <br />
clients can make some query operations such as 'get last 5 from-me' which means that get the last five messages <br />
send by me or 'get contains hello to-me' that means that get the messages send to me which also contains the text 'hello'

# Installation

With the command below you can install the required packages to run this project

pip3 install -r requirements.txt

# Execution

You can run the server by giving the port number as an argument: <br />
python3 mainServer 1050 <br /> <br />

You can run the client by giving the **nickname**, **server's IP address** and **port number** to connect to: <br />
python3 mainClient berkay 127.0.0.1 1050 <br />

<br /> 

After running the client program, here are the queries that a client can request from server: <br />
**list** -> shows currently connected users  <br />
**furkan message_text** -> sends message to the client specified by the nickname (furkan)  <br />
**get last X** -> shows the last X messages either send to or received by them <br />
**get contains hello** -> shows the messages containing 'hello' text related to them   <br />
**get from-me** -> shows the messages which are sent by the connected client