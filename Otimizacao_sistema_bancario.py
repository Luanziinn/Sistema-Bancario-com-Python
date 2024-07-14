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

saldo = 0
limite_saque = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3
AGENCIA = "0001"
usuarios = []
contas = []
cont_contas = 1 

def depositar(saldo, deposito, extrato, /):
    if deposito <= 0:
            print("Quantia inválida, por favor digite uma quantia válida.")

    else:
        saldo += deposito
        extrato += (f"Depósito realizado = R$ {deposito:.2f}\n")

    return saldo, extrato

def sacar(*, saldo, saque, extrato, limite_saque, numero_saques, limite_saques_diarios):
    if numero_saques >= LIMITE_SAQUES_DIARIOS:
        print("Já foi realizado a quantidade de saques diários permitidos.")

    elif saque > limite_saque:
        print("Quantia maior que a permitida para sacar.")

    elif saque > saldo:
        print("Quantia maior que a disponível no saldo.")

    elif saque <= 0:
        print("Quantia inválida para sacar.")
                
    else:
        saldo -= saque
        numero_saques+=1
        extrato += (f'Saque realizado = R$ {saque:.2f}\n') 

    return saldo, extrato    

def mostrar_extrato(saldo, /, *, extrato):
    if not extrato:
            print(f"Extrato:\nNão foram realizadas movimentações.\nSaldo: R$ {saldo:.2f}")
            
    else:
        print(f'Extrato:\n{extrato}Saldo: R$ {saldo:.2f}')

def cadastrar_conta(agencia, cont_contas, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario_encontrado = buscar_usuario(cpf, usuarios)

    if usuario_encontrado:
        print("Conta cadastrada com sucesso.")
        return {"agencia": agencia, "numero_conta": cont_contas, "usuario": usuario_encontrado}
    
    else:
        print("Usuário não foi encontrado.")

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta['agencia']}\nC/C: {conta['numero_conta']}\nTitular: {conta['usuario']['nome']}\n")
    
def cadastrar_usuario(usuario):
    cpf = input("Digite somente os número do CPF: ")
    usuario = buscar_usuario(cpf, usuarios)

    if usuario:
        print("Um usuário com o CPF informado já está cadastrado.")
        return
    
    nome = input("Digite o nome completo: ")
    data_nas = input("Digite a data de nascimento: ")
    endereco = input("Digite o endereço com o seguinte formato: (logradouro, nº - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nas": data_nas, "cpf": cpf, "endereco":endereco})
    print("Usuário cadastrado.")

def buscar_usuario(cpf, usuarios):
    usuarios_buscados = []
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuarios_buscados.append(usuario)
    if usuarios_buscados:
        return usuarios_buscados[0]
    else:
        return None

while True:

    opcao = int(input(menu))

    if opcao == 1:
        deposito = float(input("Digite a quantia que deseja depositar: "))

        saldo, extrato = depositar(saldo, deposito, extrato)
    
        
    elif opcao == 2:
        saque = float(input("Digite a quantia que deseja sacar: "))
            
        saldo, extrato = sacar(saldo=saldo, saque=saque, extrato=extrato, 
                               limite_saque=limite_saque, numero_saques=numero_saques, 
                               limite_saques_diarios=LIMITE_SAQUES_DIARIOS)


    elif opcao == 3:
        mostrar_extrato(saldo, extrato=extrato)

    elif opcao == 4:
        conta = cadastrar_conta(AGENCIA, cont_contas, usuarios)

        if conta:
            contas.append(conta)
            cont_contas +=1

    elif opcao == 5:
        listar_contas(contas)

    elif opcao == 6:
        cadastrar_usuario(usuarios)

    elif opcao == 0:
        break

    else:
        print("Opção inválida, por favor digite novamente.")