import math
from datetime import datetime, date

transacoes = []
CATEGORIAS_DESPESA = ["Alimentação", "Transporte", "Moradia", "Saúde", "Educação", "Lazer", "Contas", "Vestuário", "Outros"]
CATEGORIAS_RECEITA = ["Salário", "Freelance", "Investimentos", "Presentes", "Outros"]

def cadastrar_transacao():
    print("\n=== Cadastro de Transação ===\n")

    tipo = ler_tipo("Insira o tipo da transação:")
    if tipo is None:
        return

    descricao = ler_descricao("Insira a descrição da transação: ")
    if descricao is None:
        return
    
    valor = ler_valor("Insira o valor da transação: ")
    if valor is None:
        return
    
    categoria = ler_categoria("Insira a categoria da transação: ", tipo)
    if categoria is None:
        return
    
    data = ler_data("Insira a data da transação: ")
    if data is None:
        return

    transacao = {"Tipo" : tipo, "Descrição" : descricao, "Valor" : valor, "Categoria" : categoria, "Data" : data}
    transacoes.append(transacao)

    print("\nTransação cadastrada!\n")

def obter_transacoes_ordenadas():
    return sorted(transacoes, key = lambda transacao: (transacao["Data"], transacao["Valor"]))

def imprimir_tabela(lista):
    print(f"{'Tipo':<9}{'Nº':<4}{'Descrição':<25}{'Valor (R$)':>12}  {'Categoria':<18}{'Data':<10}")
    print("-" * 80)
    
    for contagem, t in enumerate(lista, start = 1):
        print(f"{t['Tipo']:<9}{contagem:<4}{t['Descrição'][:24]:<25}{t['Valor']:>12.2f}  {t['Categoria'][:17]:<18}{t['Data'].strftime('%d/%m/%Y'):<10}")
    print()

def listar_transacoes():
    print("\n=== Lista de transações ===\n")

    if len(transacoes) == 0:
        print("Não há transações registradas.\n")
        return
    
    imprimir_tabela(obter_transacoes_ordenadas())

def mostrar_resumo():
    print("\n=== Resumo ===\n")

    if len(transacoes) == 0:
        print("Não há transações registradas.\n")
        return
    
    total_receitas = 0
    total_despesas = 0
    quantidade_despesas = 0

    for t in transacoes:
        if t["Tipo"] == "Receita":
            total_receitas += t["Valor"]
        else:
            total_despesas += t["Valor"]
            quantidade_despesas += 1

    saldo = total_receitas - total_despesas

    print(f"{'Informação':<28}{'Valor':>15}")
    print("-" * 43)
    print(f"{'Total de receitas (R$)':<28}{total_receitas:>15.2f}")
    print(f"{'Total de despesas (R$)':<28}{total_despesas:>15.2f}")
    print(f"{'Saldo (R$)':<28}{saldo:>15.2f}")

    if quantidade_despesas > 0:
        media = total_despesas / quantidade_despesas
        print(f"{'Média por despesa (R$)':<28}{media:>15.2f}\n")

    totais = {}
    for t in transacoes:
        if t["Tipo"] == "Despesa":
            categoria = t["Categoria"]
            totais[categoria] = totais.get(categoria, 0) + t["Valor"]

    if len(totais) > 0:
        print(f"{'Despesas por categoria':<28}{'Total (R$)':>15}")
        print("-" * 43)

        for categoria, valor in totais.items():
            print(f"{categoria:<28}{valor:>15.2f}")
    print()

def filtrar_por_mes():
    print("\n=== Transações por mês ===\n")

    if len(transacoes) == 0:
        print("Não há transações registradas.\n")
        return

    mes = ler_inteiro("Mês (1 a 12): ", 1, 12)
    if mes is None:
        return

    ano = ler_inteiro("Ano: ", 2000, date.today().year)
    if ano is None:
        return
    print()

    filtradas = []
    for d in obter_transacoes_ordenadas():
        if d["Data"].month == mes and d["Data"].year == ano:
            filtradas.append(d)

    if len(filtradas) == 0:
        print(f"Nenhuma transação em {mes:02d}/{ano}.\n")
        return

    imprimir_tabela(filtradas)

    receitas_mes = 0
    despesas_mes = 0

    for t in filtradas:
        if t["Tipo"] == "Receita":
            receitas_mes += t["Valor"]
        else:
            despesas_mes += t["Valor"]

    saldo_mes = receitas_mes - despesas_mes

    print(f"{'Resumo do mês':<28}{'Valor':>15}")
    print("-" * 43)
    print(f"{'Receitas (R$)':<28}{receitas_mes:>15.2f}")
    print(f"{'Despesas (R$)':<28}{despesas_mes:>15.2f}")
    print(f"{'Saldo (R$)':<28}{saldo_mes:>15.2f}")
    print()

def excluir_transacao():
    print("\n=== Excluir transação ===\n")

    if len(transacoes) == 0:
        print("Não há transações para excluir.\n")
    else:
        transacoes_ordenadas = obter_transacoes_ordenadas()
        imprimir_tabela(transacoes_ordenadas)

        numero = ler_inteiro("Número da transação a ser excluída: ", 1, len(transacoes_ordenadas))
        if numero is None:
            return
            
        confirmar = ler_confirmacao("\nTem certeza que deseja excluir? (s/n): ")
        if not confirmar:
            print("\nExclusão cancelada.\n")
            return
            
        transacao = transacoes_ordenadas[numero - 1]
        transacoes.remove(transacao)
        print("\nTransação excluída!\n")

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

def ler_categoria(mensagem, tipo):
    if tipo == "Receita":
        categorias = CATEGORIAS_RECEITA
    else:
        categorias = CATEGORIAS_DESPESA

    print(mensagem)
    print()
    for contagem, c in enumerate(categorias, start = 1):
        print(f"{contagem}) {c}")
    print()
    numero = ler_inteiro("Categoria: ", 1, len(categorias))
    if numero is None:
        return None

    return categorias[numero - 1]

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
            print("Valor Inválido. Digite só números inteiros.\n")
        except (EOFError, KeyboardInterrupt):
            print ("\nEntrada cancelada.\n")
            return None
    
        if numero is not None:
            if numero < minimo or numero > maximo:
                    print(f"O número precisa estar entre {minimo} e {maximo}.\n")
                    numero = None
    return numero

def ler_confirmacao(mensagem):
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

def ler_tipo(mensagem):
    print(mensagem)
    print("\n1) Receita")
    print("2) Despesa\n")

    opcao = ler_inteiro("Tipo: ", 1, 2)
    if opcao is None:
        return None

    if opcao == 1:
        return "Receita"
    else:
        return "Despesa"

#===============================================================================================================================================================================

opcao = 0

while opcao != 6:
    print("=== Controle Financeiro ===\n")
    print("1) Cadastrar transação")
    print("2) Listar transações")
    print("3) Resumo")
    print("4) Filtrar por mês")
    print("5) Excluir transação")
    print("6) Sair")

    opcao = ler_inteiro("\nEscolha: ", 1, 6)
    if opcao is None:
        opcao = 6

    if opcao == 1:
        cadastrar_transacao()
    elif opcao == 2:
        listar_transacoes()
    elif opcao == 3:
        mostrar_resumo()
    elif opcao == 4:
        filtrar_por_mes()
    elif opcao == 5:
        excluir_transacao()

print("\nSaindo...")