# Matan Antebi
# 12.04.19
# ver 5.2

import socket, threading, sqlite3

"""
==============================
CONSTANTS
==============================
"""


all_connections = []
all_addresses = []


def add_user(username, password, pin):
    sqlconn = sqlite3.connect('accounts.db')
    cursor = sqlconn.cursor()
    check = "SELECT * FROM accounts WHERE username = " + '"' + username + '"'
    cursor.execute(check)
    selected_player = cursor.fetchone()
    if selected_player:
        return "user already exist"
    try:
        cursor.execute("INSERT INTO accounts VALUES (:username, :password, :balance, :pin_code, :in_use)",
                       {'username': username, 'password': password, 'balance': 0, 'pin_code': int(pin), 'in_use': 0})
        sqlconn.commit()
        sqlconn.close()
        print("Record created successfully")
        return "Record created successfully"
    except:
        return "Error"

def deposit(current_info, money, current_account):
    current_balance = current_info[2]
    current_balance += money
    current_account.update_balance(current_balance)
    answer = "Successfully deposited " + str(money) + "$."
    return str(answer)

def withdraw(current_info, money, current_account):
    current_balance = current_info[2]
    if current_balance >= money:
        current_balance -= money
        current_account.update_balance(current_balance)
        return "Successfully Withdrew " + str(money) + " From Your Bank Account."
    else:
        return "Oops, There is not balance in your account, Withdrawal failed."


# The function receives a connection, address and the index in all_connections,
# the function works in a thread for each client connected.
class accounts:

    def __init__(self, my_username, my_password):
        self.my_username = my_username
        self.my_password = my_password

    def login_user(self, username, password):
        if self.is_available() == 0:
            return "Error! " + username + " is unavailable right now, try again later"
        try:
            sqlconn = sqlite3.connect('accounts.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM accounts WHERE username = " + '"' + username + '"'
            cursor.execute(str1)

            selected_player = cursor.fetchone() #username, password, balance, pin
            if (password == selected_player[1]):
                cursor.execute("""UPDATE accounts SET in_use = :in_use
                                                     WHERE username = :username""",
                               {'in_use': 1, 'username': username})
                sqlconn.commit()
                sqlconn.close()
                return "Logged in successfully"
            else:
                return "Error! Incorrect username or password"
        except:
            self.my_username = ""
            self.my_password = ""
            return "Error! User not found"


    def get_balance(self):
        try:
            sqlconn = sqlite3.connect('accounts.db')
            print("connected")
            cursor = sqlconn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = :username", {'username': self.my_username})
            my_balance = cursor.fetchone()
            print("inside: ", my_balance)
            return my_balance
        except:
            return "error"

    def is_available(self):
        try:
            sqlconn = sqlite3.connect('accounts.db')
            print("connected")
            cursor = sqlconn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = :username", {'username': self.my_username})
            in_use = cursor.fetchone()[4]
            return in_use == 0
        except:
            return "error"

    def disconnect(self):
        try:
            sqlconn = sqlite3.connect('accounts.db')
            cursor = sqlconn.cursor()
            cursor.execute("""UPDATE accounts SET in_use = :in_use
                                                 WHERE username = :username""",
                           {'in_use': 0, 'username': self.my_username})
            sqlconn.commit()
            sqlconn.close()
            self.my_username = ""
            self.my_password = ""
            return self.my_username + " has disconnected"
        except:
            return "error"

    def getUsername(self):
        return self.my_username

    def check_pin(self, pin):
        try:
            sqlconn = sqlite3.connect('accounts.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM accounts WHERE username = " + '"' + self.my_username + '"'
            cursor.execute(str1)
            details = cursor.fetchone()
            if details[3] == pin:
                return True
            else:
                return False
        except:
            print("error")

    def update_balance(self, new_balance):
        try:
            sqlconn = sqlite3.connect('accounts.db')
            cursor = sqlconn.cursor()
            str1 = "SELECT * FROM accounts WHERE username = " + '"' + self.my_username + '"'
            cursor.execute(str1)

            cursor.execute("""UPDATE accounts SET balance = :new_balance
                                     WHERE username = :username""",
                           {'new_balance': new_balance, 'username': self.my_username})
            sqlconn.commit()
            sqlconn.close()
        except:
            print("Error!")


def Handle_Client(conn):
    current_account = accounts("", "")
    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if data.lower() == "login":
                if current_account.getUsername() != "":
                    conn.send(bytes("You can't do it right now", 'utf-8'))
                else:
                    conn.send(bytes("Enter username", 'utf-8'))
                    username = conn.recv(1024).decode('utf-8')
                    conn.send(bytes("Enter password", 'utf-8'))
                    password = conn.recv(1024).decode('utf-8')
                    current_account = accounts(username, password)
                    answer = current_account.login_user(username, password)
                    conn.send(bytes(answer, 'utf-8'))
            elif data.lower() == "register":
                if current_account.getUsername() != "":
                    conn.send(bytes("You can't do it right now", 'utf-8'))
                else:
                    conn.send(bytes("Enter username", 'utf-8'))
                    username = conn.recv(1024).decode('utf-8')
                    conn.send(bytes("Enter password", 'utf-8'))
                    password = conn.recv(1024).decode('utf-8')
                    conn.send(bytes("Enter pincode", 'utf-8'))
                    pincode = conn.recv(1024).decode('utf-8')
                    answer = add_user(username, password, pincode)
                    conn.send(bytes(answer, 'utf-8'))
            elif data == "deposit":
                if current_account.getUsername() == "":
                    conn.send(bytes("Error! Not connected to an account", 'utf-8'))
                else:
                    conn.send(bytes("Enter pin", 'utf-8'))
                    pin = conn.recv(1024).decode('utf-8')
                    if pin.isdigit() and current_account.check_pin(int(pin)):
                        conn.send(bytes("Enter amount to deposit", 'utf-8'))
                        to_deposit = conn.recv(1024).decode('utf-8')
                        if to_deposit.isdigit():
                            answer = deposit(current_account.get_balance(), float(to_deposit), current_account)
                        else:
                            answer = "Oops, Invalid input"
                        conn.send(bytes(answer, 'utf-8'))
                    else:
                        conn.send(bytes("Oops, Incorrect pin!", 'utf-8'))
            elif data.lower() == "withdraw":
                if current_account.getUsername() == "":
                    conn.send(bytes("Error! Not connected to an account", 'utf-8'))
                else:
                    conn.send(bytes("Enter pin", 'utf-8'))
                    pin = conn.recv(1024).decode('utf-8')
                    if pin.isdigit() and current_account.check_pin(int(pin)):
                        conn.send(bytes("Enter amount to withdraw", 'utf-8'))
                        to_withdraw = conn.recv(1024).decode('utf-8')
                        if to_withdraw.isdigit():
                            answer = withdraw(current_account.get_balance(), float(to_withdraw), current_account)
                        else:
                            answer = "Oops, Invalid input"
                        conn.send(bytes(answer, 'utf-8'))
                    else:
                        conn.send(bytes("Oops, Incorrect pin!", 'utf-8'))
            elif data.lower() == "balance":
                conn.send(bytes(str(current_account.get_balance()[2]), 'utf-8'))
            elif data.lower() == "disconnect":
                if current_account.getUsername() == "":
                    conn.send(bytes("Error! Not connected to an account", 'utf-8'))
                else:
                    print(current_account.disconnect())
                    conn.send(bytes("close", 'utf-8'))
            else:
                conn.send(bytes("Command not found", 'utf-8'))
    except ConnectionResetError:
        current_account.disconnect()






# The function receives a connection, address and the index in all_connections,
# the function open a thread for each client
def openThread(conn):
    t = threading.Thread(target=Handle_Client, args=(conn, ))
    t.start()

# The function receives server socket and accept clients, add each client's info to a list(all_connection,
# all_addresses) and call openThread function.
def accept_clients(server_socket):
    global all_connections
    while 1:
        conn, address = server_socket.accept()
        all_connections.append(conn)
        all_addresses.append(address)
        print(address[0], "Has connected")
        openThread(conn)


def Open_server():
    server_socket = socket.socket()
    port = 9999
    host = '0.0.0.0'
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Waiting For Connection...\n")
    accept_clients(server_socket)

def main():
    Open_server()

    # ===============================

if __name__ == '__main__':
    main()

