import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def transacoes(self, conta, transacao):
        transacao.registrar(conta)

    def incorporar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nas, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nas = data_nas
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def cadastrar_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, saque):
        saldo = self.saldo
        
        if saque > saldo:
            print("Quantia maior que a disponível no saldo.")
            return False

        elif saque <= 0:
            print("Quantia inválida para sacar.")
            return False
                
        else:
            self._saldo -= saque
            return True

    def depositar(self, deposito):
        if deposito <= 0:
            print("Quantia inválida, por favor digite uma quantia válida.")
            return False

        else:
            self._saldo += deposito
            return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saque = 500, limite_saques_diarios = 3):
        super().__init__(numero, cliente)
        self.limite_saque = limite_saque
        self.limite_saques_diarios = limite_saques_diarios

    def sacar(self, valor):
        numero_saques = 0
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == "Saque":
                numero_saques+=1
            
        if numero_saques >= self.limite_saques_diarios:
            print("Já foi realizado a quantidade de saques diários permitidos.")
            return False

        elif valor > self.limite_saque:
            print("Quantia maior que a permitida para sacar.")
            return False

        else:
            return super().sacar(valor)

    def __str__(self):
        return (f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}\n")

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def incorporar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        resultado_transacao = conta.sacar(self.valor)

        if resultado_transacao:
            conta.historico.incorporar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        resultado_transacao = conta.depositar(self.valor)

        if resultado_transacao:
            conta.historico.incorporar_transacao(self)

menu = """
Selecione uma das operações abaixo:
(1) - Depositar
(2) - Sacar
(3) - Extrato
(4) - Nova Conta
(5) - Listar Contas
(6) - Novo Usuário
(0) - Sair
->"""

usuarios = []
contas = []
cont_contas = 1 

def depositar(usuarios):
    cpf = input("Digite o número do CPF: ")
    usuario_encontrado = buscar_usuario(cpf, usuarios)    

    if usuario_encontrado:   
        deposito = float(input("Digite a quantia que deseja depositar: "))
        transacao = Deposito(deposito)
    
    else:
        print("O usuário não foi encontrado.")
        return

    resultado_conta = buscar_conta(usuario_encontrado)
    if not resultado_conta:
        return
    
    usuario_encontrado.transacoes(resultado_conta, transacao)

def sacar(usuarios):
    cpf = input("Digite o número do CPF: ")
    usuario_encontrado = buscar_usuario(cpf, usuarios)    

    if usuario_encontrado:
        saque = float(input("Digite a quantia que deseja sacar: "))
        transacao = Saque(saque)

    else:
        print("Usuário não foi encontrado.")
        return

    resultado_conta = buscar_conta(usuario_encontrado)
    if not resultado_conta:
        return
    
    usuario_encontrado.transacoes(resultado_conta, transacao)

def mostrar_extrato(usuarios):
    cpf = input("Digite o número do CPF: ")
    usuario_encontrado = buscar_usuario(cpf, usuarios)    

    if usuario_encontrado:
        resultado_conta = buscar_conta(usuario_encontrado)
        if not resultado_conta:
            return
        
        transacoes = resultado_conta.historico.transacoes
        extrato = ''
        if transacoes:
            for transacao in transacoes:
                extrato += f"{transacao['tipo']}: R$ {transacao['valor']:.2f}\n"
        else: 
            extrato = 'Não foi feita nenhuma movimentação.'       
            
        print(f"Extrato:\n{extrato}\nSaldo: R$ {resultado_conta.saldo:.2f}")
    else:
        print("Usuário não foi encontrado.")

def cadastrar_conta(cont_contas, usuarios, contas):
    cpf = input("Digite o CPF do usuário: ")
    usuario_encontrado = buscar_usuario(cpf, usuarios)

    if usuario_encontrado:
        conta = ContaCorrente.cadastrar_conta(cliente=usuario_encontrado, numero=cont_contas)
        contas.append(conta)
        usuario_encontrado.incorporar_conta(conta)
        print("Conta cadastrada com sucesso.")
        return conta
        

    else:
        print("Usuário não foi encontrado.")
        return

def listar_contas(contas):
    for conta in contas:
        print(str(conta))
    
def cadastrar_usuario(usuarios):
    cpf = input("Digite somente os número do CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("Um usuário com o CPF informado já está cadastrado.")
        return
    
    nome = input("Digite o nome completo: ")
    data_nas = input("Digite a data de nascimento: ")
    endereco = input("Digite o endereço com o seguinte formato: (logradouro, nº - bairro - cidade/sigla estado): ")
    usuario = PessoaFisica(nome=nome, data_nas=data_nas, cpf=cpf, endereco=endereco)
    usuarios.append(usuario)
    print("Usuário cadastrado.")

def buscar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
 
    return None

def buscar_conta(usuario):
    if not usuario.contas:
        print("Usuário não possui contas.")
        return None
    
    return usuario.contas[0]

while True:
    opcao = int(input(menu))

    if opcao == 1:
        depositar(usuarios)
        
    elif opcao == 2:
        sacar(usuarios)

    elif opcao == 3:
        mostrar_extrato(usuarios)

    elif opcao == 4:
        conta = cadastrar_conta(cont_contas, usuarios, contas)
        if conta:
            cont_contas += 1

    elif opcao == 5:
        listar_contas(contas)

    elif opcao == 6:
        cadastrar_usuario(usuarios)

    elif opcao == 0:
        break

    else:
        print("Opção inválida, por favor digite novamente.")