import socket
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def connect():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except ConnectionRefusedError:
                    print("Connection to the server was refused. Make sure the server is running.")
                    exit()

            if(not ATM_process(s)): # If either "exit" or "quit" is entered by the user
                 print("Closing connection and gracefully exiting") 
                 s.close()
                 sys.exit()


def ATM_process(s: socket.socket) -> bool:
    while(True):
        
        data = s.recv(1024).decode('utf-8')
        print(data)
        
        if("Balance:" not in data and "!!!" not in data):
            response = input(">>> ")

            if(response == "exit"): # Only exits the client
                return False 
            s.sendall(response.encode('utf-8'))

            if(response == "quit"): # Quits both the server and the client, acting as a reset
             return False


        
        
        
        



            
        
if __name__ == "__main__":
     connect()
