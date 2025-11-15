import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def broadcast(self, message, sender_client=None):
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    # Remove cliente se não for possível enviar
                    self.remove_client(client)
    
    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            client.close()
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))
            print(f'{nickname} desconectou-se')
    
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break
    
    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print(f"Servidor de chat rodando em {self.host}:{self.port}")
            print("Aguardando conexões...")
            
            while True:
                client, address = self.server_socket.accept()
                print(f"Nova conexão de {address}")
                
                # Solicitar nickname
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                
                self.nicknames.append(nickname)
                self.clients.append(client)
                
                print(f"Nickname do cliente é {nickname}")
                self.broadcast(f"{nickname} entrou no chat!".encode('utf-8'))
                client.send('Conectado ao servidor!'.encode('utf-8'))
                
                # Iniciar thread para o cliente
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.daemon = True
                thread.start()
                
        except Exception as e:
            print(f"Erro no servidor: {e}")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
