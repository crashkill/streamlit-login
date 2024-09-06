from pyrfc import Connection

class SAPConnection:
    def __init__(self, server, username, password, client='800', sysnr='00'):
        self.server = server
        self.username = username
        self.password = password
        self.client = client
        self.sysnr = sysnr
        self.conn = None

    def connect(self):
        """Estabelece a conexão com o servidor SAP."""
        try:
            self.conn = Connection(
                user=self.username,
                passwd=self.password,
                ashost=self.server,
                client=self.client,
                sysnr=self.sysnr
            )
            print("Conexão com o SAP estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar ao SAP: {e}")

    def execute(self, function_name, parameters):
        """Executa uma função RFC no servidor SAP e retorna o resultado."""
        if self.conn:
            try:
                result = self.conn.call(function_name, **parameters)
                return result
            except Exception as e:
                print(f"Erro ao executar a função {function_name}: {e}")
        else:
            print("Conexão não estabelecida. Não é possível executar a função.")

    def disconnect(self):
        """Desconecta do servidor SAP."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Conexão com o SAP desconectada.")
        else:
            print("Conexão não estabelecida. Não é necessário desconectar.")
