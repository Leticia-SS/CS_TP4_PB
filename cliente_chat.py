import socket
import threading 

class ChatClient:
    def __init__(self, host='192.168.0.174', port=12345):
        self.host = host
        self.port = port
        self.nickname = input("Escolha um nickname: ")
        self.client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Ero ao receber mensagens!")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            try:
                message = input()
                if message.lower() == '/sair':
                    self.client_socket.close()
                    break
                self.client_socket.send(f'{self.nickname}: {message}'.encode('utf-8'))          
            except:                         
                print("Ero ao enviar mensagem!")
                break
    def start_client(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f'COnectad ao servidor {self.host}:{self.port}')
            print(f'Digite "/sair" para desconectar')

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            self.send_messages()

        except Exception as ex:
            print(f"Erro ao conectar: {ex}")
        
        finally:
            self.client_socket.close()
            print("Desconectado do servidor")


if __name__ == "__main__":
    client = ChatClient()
    client.start_client()












