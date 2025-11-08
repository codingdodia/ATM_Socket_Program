import socket
import sys
import json
HOST = "127.0.0.1"
PORT = 65432


packet = {
    "input" : False,
    "data" : ""
}


class ATM:
    def __init__(self, conn = None):
        self.balance = 100
        self.conn = conn
        pass

    def send_json(self, data : str = "", input : bool = False):

        packet = {
            "input" : input,
            "data" : data
        }
        json_packet = json.dumps(packet).encode('utf-8')

        self.conn.sendall(json_packet)
        return
    def deposit(self):

        self.send_json(data = "Enter the Deposit Amount or \"back\" to leave this function:", input = True)

        amount = self.conn.recv(1024).decode('utf-8')
        print(f"[LOG] Received Data: {amount}")
        if(amount == "back"):
            return
        while not is_float(amount) or float(amount) <= 0:
            if(amount == "back"):
                return
            self.send_json(data = "Please enter an a valid amount (Not negative and greater than 0) or \"back\" to leave this function:", input = True)
            amount = self.conn.recv(1024).decode('utf-8')
            print(f"[LOG] Received Data: {amount}")

        amount = float(amount)
        self.balance += amount
        self.send_json(data = f"Amount deposited!\nNew Balance: ${str(self.balance)}\n", input = False)
        return
        
    def withdraw(self):

        if(self.balance == 0):
            self.send_json(data = "Cannot process Withdrawal\nCurrent balance is $0\n", input = False)
            return

        self.send_json(data = f"Enter the Withdrawal Amount or \"all\" to Withdraw all \"back\" to leave this function\n Current Balance is ${str(self.balance)}\n", input = True)
        amount = self.conn.recv(1024).decode('utf-8')
        print(f"[LOG] Received Data: {amount}")
        if(amount == "back"):
            return

        if(amount == "all"):
            self.balance = 0
            self.send_json(data = f"Withdrawal Successful!\n New Balance: ${str(self.balance)}\n", input = False)
            return 

        while  not is_float(amount) or float(amount) <= 0 or  self.balance < float(amount):
            if(amount == "back"):
                return
            if(not is_float(amount) or float(amount) <= 0):
                self.send_json(data="Please enter an a valid amount (Not negative and greater than 0) or \"back\" to leave this function:", input = True)
            elif(self.balance < float(amount)):
                self.send_json(data= f"Not enough balance\n Current balance: ${str(self.balance)} \n Please enter a lower amount or \"back\" to leave this function:", input = True)
            amount = self.conn.recv(1024).decode('utf-8')
            print(f"[LOG] Received Data: {amount}")
        
        if(amount == "all"):
            self.balance = 0
            self.send_json(data= f"Withdrawal Successful!\n New Balance: ${str(self.balance)}\n", input= False)
            return 
        
            
        else:
            amount = float(amount)
            self.balance -= amount
            self.send_json(data= f"Withdrawal Successful!\n New Balance: ${str(self.balance)}\n", input= False)
            return


    def check_balance(self):
         self.send_json(data=f"Current Balance: ${str(self.balance)}\n", input= False)
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

        atm.send_json(data = options, input = True)
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
