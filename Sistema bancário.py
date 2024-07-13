menu = """

Selecione uma das operações abaixo:
(1) - Depositar
(2) - Sacar
(3) - Extrato
(4) - Sair

->"""

saldo = 0
limite_saque = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3

while True:

    opcao = int(input(menu))

    if opcao == 1:
        deposito = float(input("Digite a quantia que deseja depositar: "))

        if deposito <= 0:
            print("Quantia inválida, por favor digite uma quantia válida.")

        else:
            saldo += deposito
            extrato += (f"Depósito realizado = R$ {deposito:.2f}\n")
        
    elif opcao == 2:
        if numero_saques >= LIMITE_SAQUES_DIARIOS:
            print("Já foi realizado a quantidade de saques diários permitidos.")

        else:
            saque = float(input("Digite a quantia que deseja sacar: "))

            if saque > limite_saque:
                print("Quantia maior que a permitida para sacar.")

            elif saque > saldo:
                print("Quantia maior que a disponível no saldo.")

            elif saque <= 0:
                print("Quantia inválida para sacar.")
                
            else:
                saldo -= saque
                numero_saques+=1
                extrato += (f'Saque realizado = R$ {saque:.2f}\n')

    elif opcao == 3:
        if not extrato:
            print(f"Extrato:\nNão foram realizadas movimentações.\nSaldo: R$ {saldo:.2f}")

        else:
            print(f'Extrato:\n{extrato}Saldo: R$ {saldo:.2f}')

    elif opcao == 4:
        break

    else:
        print("Opção inválida, por favor digite novamente.")
