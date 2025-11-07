import socket
import sys
HOST = "127.0.0.1"
PORT = 65432


class ATM:
    def __init__(self, conn = None):
        self.balance = 100
        self.conn = conn
        pass

    def deposit(self):

        self.conn.sendall(b"Enter the Deposit Amount or \"back\" to leave this function:")
        amount = self.conn.recv(1024).decode('utf-8')
        print(f"[LOG] Received Data: {amount}")
        if(amount == "back"):
            return
        while not is_float(amount) or float(amount) <= 0:
            if(amount == "back"):
                return
            self.conn.sendall(b"Please enter an a valid amount (Not negative and greater than 0) or \"back\" to leave this function:")
            amount = self.conn.recv(1024).decode('utf-8')
            print(f"[LOG] Received Data: {amount}")

        amount = float(amount)
        self.balance += amount
        self.conn.sendall(b"Amount deposited!\nNew Balance: $" + str(self.balance).encode('utf-8') + b"\n")
        return
        
    def withdraw(self):

        if(self.balance == 0):
            self.conn.sendall(b"Cannot process Withdrawal\nCurrent balance is 0\n")
            return

        self.conn.sendall(b"Enter the Withdrawal Amount or \"all\" to Withdraw all \"back\" to leave this function\n Current Balance is $" + str(self.balance).encode('utf-8') + b"\n")
        amount = self.conn.recv(1024).decode('utf-8')
        print(f"[LOG] Received Data: {amount}")
        if(amount == "back"):
            return

        if(amount == "all"):
            self.balance = 0
            self.conn.sendall(b"Withdrawal Successful!\n New Balance: $" + str(self.balance).encode('utf-8') + b"\n")
            return 

        while  not is_float(amount) or float(amount) <= 0 or  self.balance < float(amount):
            if(amount == "back"):
                return
            if(not is_float(amount) or float(amount) <= 0):
                self.conn.sendall(b"Please enter an a valid amount (Not negative and greater than 0) or \"back\" to leave this function:")
            elif(self.balance < float(amount)):
                self.conn.sendall(b"Not enough balance\n Current balance: $" + str(self.balance).encode('utf-8') + b"\n Please enter a lower amount or \"back\" to leave this function:")
            amount = self.conn.recv(1024).decode('utf-8')
            print(f"[LOG] Received Data: {amount}")
        
        if(amount == "all"):
            self.balance = 0
            self.conn.sendall(b"Withdrawal Successful!\n New Balance: $" + str(self.balance).encode('utf-8') + b"\n")
            return 
        
            
        else:
            amount = float(amount)
            self.balance -= amount
            self.conn.sendall(b"Withdrawal Successful!\n New Balance: $" + str(self.balance).encode('utf-8') + b"\n")
            return


    def check_balance(self):
         self.conn.sendall(b"Current Balance: $" + str(self.balance).encode('utf-8') + b"\n")
         return

atm = ATM()

def is_float(s: str):
    try:
        float(s)
    except:
        return False
    return True

def connect():
    # Create the listening socket and keep it open until a client sends 'quit'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Allow quick reuse of the address/port after restarting server
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print(f"Server listening on {HOST}:{PORT}")

        # Accept clients in a loop. If ATM_process returns False, stop the server.
        while True:
            try:
                conn, addr = s.accept()
            except KeyboardInterrupt:
                print("Server shutting down (KeyboardInterrupt)")
                break

            with conn:
                print(f"Connected by {addr}")
                # ATM_process returns False when the client requests server reset/quit
                keep_running = ATM_process(conn)
                if not keep_running:
                    print("Received quit signal from client — shutting down server.")
                    # exit the program gracefully
                    sys.exit()

def ATM_process(conn) -> bool:

    options = '''Welcome to the ATM!
Please enter the numbers associate with the task or enter \"exit\" to exit the program or \"quit\" to reset the server and the client:
1 Deposit
2 Withdraw
3 Check Balance '''

    atm.conn = conn # Set the current connection to the ATM's connection


    while True:
        conn.sendall(options.encode('utf-8'))
        data = conn.recv(1024)
        if not data:
            return True
        data = data.decode('utf-8').strip()
        print(f"[LOG] Received data: {data}")


        match data:
            case '1':
                atm.deposit()
            case '2':
                atm.withdraw()
            case '3':
                atm.check_balance()
            case 'quit':
                return False
            case _:  # This is the default case
                conn.sendall(b"\n!!! PLEASE ENTER A VALID INPUT !!! \n")

    

if __name__ == "__main__":
    connect()
