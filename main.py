import math
from datetime import datetime, date

despesas = []

def cadastrar_despesa():
    print("\n=== Cadastro de Despesa ===\n")

    descricao = ler_descricao("Insira a descrição da despesa: ")
    if descricao is None:
        return
    valor = ler_valor("Insira o valor da despesa: ")
    if valor is None:
        return
    categoria = ler_categoria("Insira a categoria da despesa: ")
    if categoria is None:
        return
    data = ler_data("Insira a data da despesa: ")
    if data is None:
        return

    despesa = {"Descrição" : descricao, "Valor" : valor, "Categoria" : categoria, "Data" : data}
    despesas.append(despesa)

    print("\nDespesa cadastrada!\n")

def obter_despesas_ordenadas():
    return sorted(despesas, key = lambda despesa: (despesa["Data"], despesa["Valor"]))

def imprimir_tabela(lista):
    print(f"{'Nº':<4}{'Descrição':<25}{'Valor (R$)':>12}  {'Categoria':<18}{'Data':<10}")
    print("-" * 71)
    
    for contagem, d in enumerate(lista, start = 1):
        print(f"{contagem:<4}{d['Descrição'][:24]:<25}{d['Valor']:>12.2f}  {d['Categoria'][:17]:<18}{d['Data'].strftime('%d/%m/%Y'):<10}")
    print()

def listar_despesas():
    print("\n=== Lista de despesas ===\n")

    if len(despesas) == 0:
        print("Nenhuma despesa foi cadastrada ainda.\n")
    else:
        imprimir_tabela(obter_despesas_ordenadas())

def mostrar_resumo():
    print("\n=== Resumo ===\n")

    if len(despesas) == 0:
        print("Não há despesas registradas.\n")
    else:
        total = 0
        for d in despesas:
            total += d["Valor"]

        quantidade = len(despesas)
        media = total / quantidade

        print(f"{'Informação':<28}{'Valor':>15}")
        print("-" * 43)
        print(f"{'Quantidade de despesas':<28}{quantidade:>15}")
        print(f"{'Valor total (R$)':<28}{total:>15.2f}")
        print(f"{'Média por despesa (R$)':<28}{media:>15.2f}\n")

        totais = {}
        for d in despesas:
            categoria = d["Categoria"]
            totais[categoria] = totais.get(categoria, 0) + d["Valor"]

        print(f"{'Categoria':<28}{'Total (R$)':>15}")
        print("-" * 43)
        for categoria, valor in totais.items():
            print(f"{categoria:<28}{valor:>15.2f}")
        print()

def excluir_despesa():
        print("\n=== Excluir despesa ===\n")
        if len(despesas) == 0:
            print("Não há despesas para excluir.\n")
        else:
            despesas_ordenadas = obter_despesas_ordenadas()
            imprimir_tabela(despesas_ordenadas)
            numero = ler_inteiro("Número da despesa a ser excluída: ", 1, len(despesas_ordenadas))
            if numero is None:
                return
                
            confirmar = ler_confirmação("\nTem certeza que deseja excluir? (s/n): ")
            if not confirmar:
                print("\nExclusão cancelada.\n")
                return
            
            despesa = despesas_ordenadas[numero - 1]
            despesas.remove(despesa)
            print("\nDespesa excluída!\n")

def ler_descricao(mensagem):
    texto = ""
    while texto == "":
        try:
            texto = input(mensagem).strip().capitalize()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada Cancelada.\n")
            return None
        if texto == "":
            print("O campo não pode ficar vazio.\n")
        elif not any(letra.isalpha() for letra in texto):
            print("O texto precisa ter pelo menos uma letra.\n")
            texto = ""
    return texto

def ler_categoria(mensagem):
    texto = ""
    while texto == "":
        try:
            texto = input(mensagem).strip().capitalize()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada Cancelada.\n")
            return None
        if texto == "":
            print("O campo não pode ficar vazio.\n")
        elif any(letra.isdigit() for letra in texto):
            print("A categoria não pode ter números.\n")
            texto = ""
    return texto

def ler_valor(mensagem):
    numero = None
    while numero is None:
        try:
            texto = input(mensagem).strip().replace(",",".")
            numero = float(texto)
        except ValueError:
            print("Valor Inválido. Digite só números, ex: 120,50\n")
        except (EOFError, KeyboardInterrupt):
            print ("\nEntrada cancelada.\n")
            return None

        if numero is not None:
            if not math.isfinite(numero):
                print("Valor inválido. Digite um número normal, ex: 120,50\n")
                numero = None
            elif numero <= 0:
                    print("O valor precisa ser maior que zero.\n")
                    numero = None
            elif numero > 99999999.99:
                    print("Valor alto demais.\n")
                    numero = None
    return round(numero, 2)

def ler_data(mensagem):
    data = None
    while data is None:
        try:
            texto = input(mensagem).strip()
            data = datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use dd/mm/aaaa, ex: 01/01/2000\n")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada Cancelada.\n")
            return None

        if data is not None and data > date.today():
            print("A data não pode ser futura.\n")
            data = None
    return data

def ler_inteiro(mensagem, minimo, maximo):
    numero = None
    while numero is None:
        try:
            texto = input(mensagem).strip()
            numero = int(texto)
        except ValueError:
            print("Valor Inválido. Digite só números inteiros\n")
        except (EOFError, KeyboardInterrupt):
            print ("\nEntrada cancelada.\n")
            return None
    
        if numero is not None:
            if numero <= 0:
                    print("O valor precisa ser maior que zero.\n")
                    numero = None
            elif numero < minimo or numero > maximo:
                    print(f"O número precisa estar entre {minimo} e {maximo}.\n")
                    numero = None
    return numero

def ler_confirmação(mensagem):
    resposta = ""
    while resposta not in ("s", "n"):
        try:
            resposta = input(mensagem).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada cancelada.")
            return None
        if resposta not in ("s", "n"):
            print("Responda com 's' para sim ou 'n' para não.")
    return resposta == "s"

opcao = ""

while opcao != "5":
    print("=== Controle Financeiro ===\n")
    print("1) Cadastrar despesa")
    print("2) Listar despesas")
    print("3) Resumo")
    print("4) Excluir despesa")
    print("5) Sair")

    try:
        opcao = input("\nEscolha: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada Cancelada.\n")
        opcao = "5"

    if opcao == "1":
        cadastrar_despesa()
    elif opcao == "2":
        listar_despesas()
    elif opcao == "3":
        mostrar_resumo()
    elif opcao == "4":
        excluir_despesa()
    elif opcao != "5":
        print("Opção inválida.\n")

print("\nSaindo...")