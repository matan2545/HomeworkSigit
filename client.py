# Matan Antebi
# 12.04.19
# ver 5.2

import socket


"""
==============================
Client
==============================
"""
my_socket = socket.socket()
port = 9999
host = '127.0.0.1'
my_socket.connect((host, port))
print("Connected !")

def welcome_message():
    print("=======================\n"
          "      Matan's ATM\n"
          "=======================\n"
          "Welcome to Matan's ATM!\nAvailable Commands: \n"
          "- Login\n- Register\n=======================")

def options_message():
    print("=======================\n"
          "      Matan's ATM\n"
          "=======================\n"
          "Available Commands: \n"
          "- Balance\n- Deposit\n- Withdraw\n- Disconnect\n=======================")

def atmSender():
    tosend = input("")
    my_socket.send(bytes(tosend, 'utf-8'))
    answer = my_socket.recv(1024).decode('utf-8')
    print(answer)
    if "Error" in answer or answer == "close" or answer == "Record created successfully":
        welcome_message()
    if answer == "Logged in successfully" or "Oops" in answer or "Successfully" in answer:
        options_message()



def main():
    welcome_message()
    while True:
        atmSender()


"""
Open rules page and wait for mouse input 
"""
if __name__ == '__main__':
    main()