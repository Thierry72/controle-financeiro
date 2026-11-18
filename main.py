print("=== Controle Financeiro ===")

opcao = ""

while opcao != "3":
    print("\n1) Cadastrar despesa")
    print("2) Listar despesas")
    print("3) Sair")

    try:
        opcao = input("\nEscolha: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada Cancelada")
        opcao = "3"

    if opcao == "1":
        print("Cadastrar...")
    elif opcao == "2":
        print("Listar...")
    elif opcao != "3":
        print("Opção inválida")

print("Saindo...")