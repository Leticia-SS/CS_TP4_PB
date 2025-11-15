import socketserver
import threading

class SMTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"Conexão recebida de {self.client_address[0]}")
        self.request.send(b"220 localhost ESMTP Fake Server\r\n")
        
        while True:
            try:
                data = self.request.recv(1024).decode().strip()
                if not data:
                    break
                    
                print(f"CLIENTE: {data}")
                
                if data.upper().startswith("EHLO"):
                    self.request.send(b"250-localhost\r\n250 OK\r\n")
                elif data.upper().startswith("MAIL FROM"):
                    self.request.send(b"250 OK\r\n")
                elif data.upper().startswith("RCPT TO"):
                    self.request.send(b"250 OK\r\n")
                elif data.upper().startswith("DATA"):
                    self.request.send(b"354 Enter message, end with .\r\n")
                elif data == ".":
                    self.request.send(b"250 Message accepted for delivery\r\n")
                    print("EMAIL ACEITO PELO SERVIDOR LOCAL!")
                elif data.upper().startswith("QUIT"):
                    self.request.send(b"221 Bye\r\n")
                    break
                else:
                    self.request.send(b"250 OK\r\n")
                    
            except Exception as e:
                print(f"Erro: {e}")
                break

def start_smtp_server():
    server = socketserver.TCPServer(('localhost', 1025), SMTPHandler)
    print("Servidor SMTP Fake rodando na porta 25...")
    print("Aguardando conexões...")
    server.serve_forever()

if __name__ == "__main__":
    start_smtp_server()



