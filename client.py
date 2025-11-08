import socket
import sys
import json

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
        try:
             data = json.loads(data)
        except json.JSONDecodeError:
             print("Error")
             data = data
        

        
        if('input' in data and data.get('input') == True):
             print(data.get('data'))
             response = input(">>> ")

             if(response == "exit"):
                  return False
             
             s.sendall(response.encode('utf-8'))
            
             if(response == "quit"):
                  return False


        else:
             print(data.get('data') if 'data' in data else data)
             


if __name__ == "__main__":
     connect()
