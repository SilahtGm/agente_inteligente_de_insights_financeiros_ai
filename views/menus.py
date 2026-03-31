# main.py
import sys
from db.connection import inicializar_banco, conectar_banco
from auth.auth import login, criar_conta
from features.transacoes import registrar_transacao, exibir_transacoes
from features.metas import criar_metas, exibir_metas
from features.relatorios import checar_saldo, exibir_saude_financeira, exibir_ranking_gastos
from ia.fingpt import (
    sugerir_economia,
    resumo_financeiro_ia,
    prever_proximos_meses,
    fazer_pergunta
)

# Funções Menu



def menu():
    inicializar_banco()
    while True:
        print("\n=============================")
        print(" Sistema de Gestão Financeira ")
        print("=============================")
        print(" 1 - Fazer Login")
        print(" 2 - Criar Nova Conta")
        print(" 0 - Sair do Sistema")
        print("=============================")
        op = input("Escolha uma opção: ")

        match op:

            case "1":
                login()
            case "2":
                criar_conta()
            case "0":
                print("\nEncerrando o sistema. Até mais!")
                sys.exit()
            case _:
                print("\n[!] Opção inválida. Tente novamente.")



def menu_pos_login(usuario):
    nm_usuario = usuario[1]

    while True:
        print(f"\n==========================================")
        print(f"       SGF - PAINEL DE CONTROLE           ")
        print(f"       Usuário: {nm_usuario.upper()}")
        print(f"==========================================")
        print(" [1] VISÃO GERAL (Saldo)")
        print(" [2] TRANSAÇÕES (ENTRADA/SAÍDA)")
        print(" [3] RELATÓRIOS E GRÁFICOS")
        print(" [4] PLANEJAMENTO (Metas Econômicas)")
        print(" [5] INSIGHTS I.A (FinGPT)")
        print(" [0] LOGOUT")
        print("==========================================")

        opcao = input("Escolha uma operação: ")

        match opcao:
            case "1":
                checar_saldo(usuario)


            case "2":
               menu_transacoes(usuario)


            case "3":
                menu_relatorios(usuario)
            case "4":
               menu_metas_economicas(usuario)

            case "5":
                menu_ia(usuario)


            case "0":
                print(f"\nEncerrando sessão de {nm_usuario}...")
                break

            case _:
                print("\n[!] Opção incorreta. Tente novamente.")

def menu_transacoes(usuario):

        nm_usuario = usuario[1]
        while True:
            print("============================")
            print(" SGF - MOVIMENTAÇÕES FINANCEIRAS")
            print(f" Usuário: {nm_usuario.upper()}")
            print("============================")
            print(" [1] EFETUAR ENTRADA/SAÍDA")
            print(" [2] EXIBIR MOVIMENTAÇÕES EXISTENTES")
            print(" [0] VOLTAR")
            print("==========================================")
            opcao = input("Escolha uma operação: ")

            match opcao:
                case "1":
                    registrar_transacao(usuario)
                case "2":
                    exibir_transacoes(usuario)
                case "0":
                    print("Voltando...")
                    break
                case _:
                    print("\n[!] Opção incorreta. Tente novamente.")



def menu_metas_economicas(usuario):

    nm_usuario = usuario[1]
    while True:
        print("============================")
        print(" SGF - METAS ECONÔMICAS")
        print(f" Usuário: {nm_usuario.upper()}")
        print("============================")
        print(" [1] LANÇAR NOVA META")
        print(" [2] EXIBIR METAS EXISTENTES")
        print(" [0] VOLTAR")
        print("==========================================")
        opcao = input("Escolha uma operação: ")

        match opcao:
            case "1": criar_metas(usuario)
            case "2": exibir_metas(usuario)
            case "0":
                print("Voltando...")
                break
            case _:
                print("\n[!] Opção incorreta. Tente novamente.")


def menu_relatorios(usuario):
    while True:
        print("=================================")
        print("    SGF - INSIGHTS FINANCEIROS")
        print(f"    Analista: {usuario[1].upper()}")
        print("=================================")
        print(" [1] DIAGNÓSTICO DE SAÚDE (KPIs)")
        print(" [2] MAIORES GASTOS (Ranking)")
        print(" [0] VOLTAR")
        print("=================================")
        opcao = input("Escolha o insight desejado: ")

        if opcao == "1":
            exibir_saude_financeira(usuario)
        elif opcao == "2":
            exibir_ranking_gastos(usuario)
        elif opcao == "0":
            break
        else:
            print("[!] Opção inválida.")


def menu_ia(usuario):
    nm_usuario = usuario[1]
    while True:
        print("===================================================")
        print("          🤖 ASSISTENTE IA - FinGPT")
        print(f"          👤 Usuário: {nm_usuario}")
        print("===================================================")
        print("[1] 📊 Analisar meus dados")
        print("    -> Ver resumo financeiro")
        print("[2] 💰 Sugerir economia")
        print("    -> Dicas para gastar menos")
        print("[3] 🔮 Prever próximos meses")
        print("    -> Como estarei financeiramente")
        print("[4] ❓ Fazer pergunta")
        print("    -> Qualquer dúvida sobre finanças")
        print("[0] ↩️  Voltar ao menu principal")
        print("===================================================")
        opcao = input("\nEscolha uma opção: ")
        match opcao:
            case "1":
                resumo_financeiro_ia(usuario)
            case "2":
                sugerir_economia(usuario)
            case "3":
                prever_proximos_meses(usuario)
            case "4":
                fazer_pergunta(usuario)
            case "0":
                print("Voltando...")
                break
            case _:
                print("\n[!] Opção incorreta. Tente novamente.")



# Start do sistema
menu()


# APOIO DE ESTUDOS
# ==============================================================================
# GUIA DE MÉTODOS DO CURSOR (SQLITE3)
# ==============================================================================

# cursor.execute(query, params)
# -> O MAIS USADO: Envia um comando SQL para o banco de dados.
# -> Use '?' como placeholder para passar variáveis com segurança.
# Ex: cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_user,))

# cursor.fetchone()
# -> BUSCA UMA LINHA: Retorna a primeira linha do resultado da consulta.
# -> Útil para: Logins, somas de saldo (SUM) ou buscar um item específico.
# -> Retorna: Uma TUPLA se achar algo, ou NONE se não achar nada.

# cursor.fetchall()
# -> BUSCA TUDO: Retorna uma LISTA contendo todas as linhas da consulta.
# -> Útil para: Listar extratos, mostrar todas as categorias ou metas.
# -> Retorna: Uma lista de tuplas [ (id1, nome1), (id2, nome2) ].

# cursor.lastrowid
# -> O "RG" DO NOVO REGISTRO: Retorna o ID (PK) da última linha que você inseriu.
# -> Útil para: Confirmar se o INSERT funcionou ou vincular dados na hora.
# -> Só funciona após comandos INSERT.

# cursor.executescript(string_sql)
# -> MÚLTIPLOS COMANDOS: Executa vários comandos SQL de uma vez (separados por ;).
# -> Útil para: Rodar o arquivo 'schema.sql' ou 'inserts.sql' na inicialização.

# cursor.rowcount
# -> LINHAS AFETADAS: Diz quantas linhas foram alteradas pelo último comando.
# -> Útil para: Saber se um UPDATE ou DELETE realmente alterou algo no banco.
# ==============================================================================



