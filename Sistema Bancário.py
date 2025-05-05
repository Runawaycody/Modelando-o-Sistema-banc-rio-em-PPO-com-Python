from datetime import datetime, date

class Cliente:
    def __init__(self, nome: str, data_nascimento, cpf: str, endereco: str):
        self.nome = nome
        self.data_nascimento = data_nascimento  # pode ser string ou date
        self.cpf = ''.join(filter(str.isdigit, cpf))
        self.endereco = endereco
        self.contas = []  # lista de contas associadas

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"

    def adicionar_conta(self, conta):
        if conta not in self.contas:
            self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: date, cpf: str, endereco: str):
        super().__init__(nome, data_nascimento, cpf, endereco)

class Transacao:
    def __init__(self, valor: float, descricao: str = ""):
        self.valor = valor
        self.descricao = descricao

    def __str__(self):
        return self.descricao

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor: float, sucesso: bool = True):
        if sucesso:
            descricao = f"Depósito: R$ {valor:.2f}"
        else:
            descricao = f"Depósito falhado: valor inválido R$ {valor:.2f}"
        super().__init__(valor, descricao)

class Saque(Transacao):
    def __init__(self, valor: float, sucesso: bool, motivo: str = ""):
        if sucesso:
            descricao = f"Saque: R$ {valor:.2f}"
        else:
            descricao = f"Saque falhado: {motivo} para R$ {valor:.2f}"
        super().__init__(valor, descricao)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def imprimir_extrato(self):
        print("================================ Extrato ================================")
        if self.transacoes:
            for transacao in self.transacoes:
                print(transacao)
        else:
            print("Nenhuma transação realizada.")
        print("=======================================================================")

class Conta:
    def __init__(self, cliente: Cliente, numero: int, agencia: str = "0001"):
        self.cliente = cliente
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0.0
        self.historico = Historico()

    def get_saldo(self) -> float:
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(cliente, numero)

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            transacao = Deposito(valor)
            transacao.registrar(self)
            return True
        else:
            transacao = Deposito(valor, sucesso=False)
            transacao.registrar(self)
            return False

    def sacar(self, valor: float) -> bool:
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            transacao = Saque(valor, True)
            transacao.registrar(self)
            return True
        else:
            motivo = "valor inválido" if valor <= 0 else "saldo insuficiente"
            transacao = Saque(valor, False, motivo)
            transacao.registrar(self)
            return False

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, agencia: str = "0001", limite: float = 500.0, limite_saques: int = 3):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor: float) -> bool:
        if self.saques_realizados >= self.limite_saques:
            transacao = Saque(valor, False, "limite diário atingido")
            transacao.registrar(self)
            return False
        if valor > self.limite:
            transacao = Saque(valor, False, f"valor acima do limite de R$ {self.limite:.2f}")
            transacao.registrar(self)
            return False
        if valor > self.saldo:
            transacao = Saque(valor, False, "saldo insuficiente")
            transacao.registrar(self)
            return False
        if valor > 0:
            self.saldo -= valor
            self.saques_realizados += 1
            transacao = Saque(valor, True)
            transacao.registrar(self)
            return True
        else:
            transacao = Saque(valor, False, "valor inválido")
            transacao.registrar(self)
            return False

class SistemaBancario:
    def __init__(self):
        self.usuarios = []  # Lista de clientes (PessoaFisica, etc.)
        self.contas = []    # Lista de contas (Conta, ContaCorrente, etc.)
        self.numero_conta = 1

    def cadastrar_usuario(self):
        print("\n" + "=" * 16 + " Cadastro de Usuário (Cliente/Pessoa Física) " + "=" * 16)
        cpf_input = input("CPF (apenas números serão armazenados): ")
        cpf_numeros = ''.join(filter(str.isdigit, cpf_input))
        usuario_encontrado = next((usuario for usuario in self.usuarios if usuario.cpf == cpf_numeros), None)
        if usuario_encontrado:
            print("Aviso: CPF encontrado. Usuário vinculado à conta existente.")
            return usuario_encontrado

        nome = input("Nome: ")
        data_nascimento_str = input("Data de Nascimento (DD/MM/AAAA): ")
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
        except ValueError:
            print("Data de nascimento inválida. Usando string original.")
            data_nascimento = data_nascimento_str
        endereco = input("Endereço (formato: logradouro, nro, bairro, cidade/sigla estado): ")
        cliente = PessoaFisica(nome, data_nascimento, cpf_numeros, endereco)
        self.usuarios.append(cliente)
        print("Usuário cadastrado com sucesso!")
        return cliente

    def criar_conta_corrente(self):
        if not self.usuarios:
            print("Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
            return
        cpf_buscar = input("Informe o CPF para selecionar o usuário: ")
        cpf_buscar = ''.join(filter(str.isdigit, cpf_buscar))
        usuario = next((u for u in self.usuarios if u.cpf == cpf_buscar), None)
        if usuario is None:
            print("Usuário não encontrado. Cadastre um usuário primeiro.")
            return
        conta = ContaCorrente(usuario, self.numero_conta)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        self.numero_conta += 1
        print("Conta corrente criada com sucesso!")
        return conta

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for conta in self.contas:
            print(f"Agência: {conta.agencia}")
            print(f"Conta: {conta.numero}")
            print(f"Titular: {conta.cliente.nome}")
            print("========================================================================")

    def selecionar_conta(self):
        cpf = input("Informe o CPF: ")
        cpf = ''.join(filter(str.isdigit, cpf))
        contas_usuario = [conta for conta in self.contas if conta.cliente.cpf == cpf]
        if not contas_usuario:
            print("Nenhuma conta encontrada para o CPF informado.")
            return None
        if len(contas_usuario) == 1:
            return contas_usuario[0]
        else:
            print("Mais de uma conta encontrada para o CPF informado:")
            for conta in contas_usuario:
                print(f"Conta: {conta.numero}, Agência: {conta.agencia}")
            numero = input("Informe o número da conta desejada: ")
            conta_selecionada = next((conta for conta in contas_usuario if str(conta.numero) == numero), None)
            if not conta_selecionada:
                print("Conta não encontrada.")
            return conta_selecionada

    def depositar(self):
        if not self.contas:
            print("Nenhuma conta criada. Crie uma conta primeiro.")
            return
        conta = self.selecionar_conta()
        if conta:
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                if conta.depositar(valor):
                    print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("Operação falhou! Valor inválido.")
            except ValueError:
                print("Valor inválido.")

    def sacar(self):
        if not self.contas:
            print("Nenhuma conta criada. Crie uma conta primeiro.")
            return
        conta = self.selecionar_conta()
        if conta:
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                if conta.sacar(valor):
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                else:
                    print("Operação de saque falhou.")
            except ValueError:
                print("Valor inválido.")

    def extrato(self):
        if not self.contas:
            print("Nenhuma conta criada. Crie uma conta primeiro.")
            return
        conta = self.selecionar_conta()
        if conta:
            conta.historico.imprimir_extrato()
            print(f"Saldo: R$ {conta.get_saldo():.2f}")

    def menu(self):
        while True:
            print("\n" + "=" * 16 + " MENU " + "=" * 16)
            print("1. Depositar")
            print("2. Sacar")
            print("3. Extrato")
            print("4. Cadastrar Usuário")
            print("5. Criar Conta Corrente")
            print("6. Listar Contas")
            print("7. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.depositar()
            elif opcao == "2":
                self.sacar()
            elif opcao == "3":
                self.extrato()
            elif opcao == "4":
                usuario = self.cadastrar_usuario()
                if usuario:
                    print(f"Usuário {usuario.nome} cadastrado/selecionado.")
            elif opcao == "5":
                self.criar_conta_corrente()
            elif opcao == "6":
                self.listar_contas()
            elif opcao == "7":
                print("Obrigado por utilizar o sistema. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")

def main():
    sistema = SistemaBancario()
    sistema.menu()

if __name__ == "__main__":
    main()