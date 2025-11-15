import socket
import time

class GmailSender:
    def __init__(self):
        self.smtp_server = "localhost"
        self.port = 1025

    def get_email_info(self):
        print("===== ENVIO DE EMAIL VIA GMAIL =====")
        self.to_email = input("Digite o email do destinatario: ").strip()
        self.subject = input("Digite o titulo do email: ").strip()

        print("Digite o conteudo do email (digite 'FIM' para finalizar):")  
       
        lines = []
        while True:
            line = input()
            if line.upper() == 'FIM':
                break

            lines.append(line)

        self.body = '\n'.join(lines)


    def read_response(self, sock, timeout=5):
        try:
            sock.settimeout(timeout)
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            print(f'Servidor: {response.strip()}')
            return response
        except Exception as ex:
            print(f"Erro ao ler resposta: {ex}")
            return '' 


    def send_email_anonymous(self):
        try:
            print(f"\nConectando ao {self.smtp_server} na porta {self.port}...")
            
        
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.smtp_server, self.port))
            
            response = self.read_response(sock) 
            if not response.startswith('220'):
                print("Erro de conexao inicial")
                return False


            commands = [
                f"EHLO localhost\r\n",
                f"MAIL FROM: <teste@ethereal.email>\r\n",
                f"RCPT TO: <{self.to_email}>\r\n", 
                "DATA\r\n",
                f"Subject: {self.subject}\r\n",
                f"\r\n{self.body}\r\n",
                ".\r\n",
                "QUIT\r\n"
            ]



            for cmd in commands:
                print(f'Enviando: {cmd.strip()}')
                sock.send(cmd.encode('utf-8'))  # CORRIGIDO: usando sock.send
                time.sleep(1)


                response = self.read_response(sock)  

                if response and response[0] in '45':  
                    print(f"Erro no servidor: {response}")
                    return False


            sock.close()  
            return True


        except Exception as ex:
            print(f"Erro durante envio: {ex}")
            return False


    def test_connection(self):
        try:
            print(f"Testando conexao com {self.smtp_server}:{self.port}...")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.smtp_server, self.port))
            
            response = self.read_response(sock)  
            if response.startswith('220'):
                print("Conexao estabelecida")
                sock.send(b"QUIT\r\n")  
                sock.close()  
                return True

            else:
                print("Falha na conexao")
                return False

            

        except Exception as ex:
            print(f"Erro na conexao: {ex}")
            return False


    def start(self):
        self.get_email_info()
        
        print(f"\nResumo do email:")
        print(f"Para: {self.to_email}")
        print(f"Assunto: {self.subject}")
        print(f"Mensagem: {self.body}")
        
        confirmar = input("\nDeseja enviar o email? (s/n): ").strip().lower()
        
        if confirmar == 's':
            print("\nEnviando email...")
            if self.send_email_anonymous():
                print("Email enviado com sucesso")
            else:
                print("Falha no envio do email")
        else:
            print("Envio cancelado.")



if __name__ == "__main__":
    sender = GmailSender()
    sender.start()




