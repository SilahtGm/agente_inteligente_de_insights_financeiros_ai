# Importações necessarias
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from db.connection import conectar_banco
from utils.helpers import pausar


def checar_saldo(usuario):
    id_usuario = usuario[0]
    try:
        conexao, cursor = conectar_banco()

        tipo = "Entrada"
        query1 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query1, (id_usuario, tipo))
        entrada = cursor.fetchone()

        if entrada[0] is None:
            print("Você não possui transações de entrada")
            return

        tipo2 = "Saída"
        query2 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query2,(id_usuario, tipo2))
        saida = cursor.fetchone()

        if saida[0] is None:
            print("Você não possui transações de saída")
            return

        entrada_valor = entrada[0] or 0
        saida_valor = saida[0] or 0
        saldo = entrada_valor - saida_valor

        print(f"\n=============================")
        print(f"   SALDO ATUAL: R$ {saldo}")
        print(f"Entradas: R$ {entrada_valor} | Saídas: R$ {saida_valor}")
        print(f"=============================")

        pausar()

        conexao.commit()
        conexao.close()




    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")


def exibir_saude_financeira(usuario):
    id_usuario = usuario[0]

    try:
        conexao, cursor = conectar_banco()

        tipo = "Entrada"
        query1 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query1, (id_usuario, tipo))
        entrada = cursor.fetchone()

        if entrada[0] is None:
            print("Você não possui transações de entrada")
            return

        tipo2 = "Saída"
        query2 = "SELECT SUM(valor) FROM transacoes WHERE id_usuario = ? AND tipo = ?"
        cursor.execute(query2, (id_usuario, tipo2))
        saida = cursor.fetchone()

        if saida[0] is None:
            print("Você não possui transações de saída")
            return

        saldo = entrada[0] - saida[0]

        # Cálculo de Eficiência Financeira (Quanto % do que ganho eu guardo?)
        if entrada[0] > 0:
            eficiencia = (saldo / entrada[0]) * 100
        else:
            eficiencia = 0

        print(f"\n=============================")
        print(f"   DIAGNÓSTICO DE SAÚDE")
        print(f"=============================")
        print(f" Total Entradas: R$ {entrada[0]}")
        print(f" Total Saídas:   R$ {saida[0]}")
        print(f" ---------------------------")
        print(f" SALDO ATUAL:    R$ {saldo}")
        print(f" TAXA DE SOBRA:  {eficiencia}")
        print(f"=============================")

        if eficiencia > 20:
            print("SITUAÇÃO: [ÓTIMA] - Você está poupando como um profissional!")
        elif eficiencia > 0:
            print("SITUAÇÃO: [ALERTA] - Sua margem de segurança é pequena.")
        else:
            print("SITUAÇÃO: [CRÍTICA] - Você está gastando mais do que recebe.")


        pausar()
        # Pergunta se quer ver o gráfico
        op = input("\nDeseja visualizar o comparativo em gráfico? (S/N): ").upper()
        if op == 'S':


            # Usando Pandas para preparar os dados de forma simples
            df = pd.DataFrame({
                'Categoria': ['Entradas', 'Saídas'],
                'Valores': [entrada[0], saida[0]]
            })

            # Gerando um gráfico de barras simples
            df.plot(kind='bar', x='Categoria', y='Valores', color=['green', 'red'], legend=False)
            plt.title("Comparativo: Entradas vs Saídas")
            plt.ylabel("Valor em R$")
            plt.xticks(rotation=0)
            plt.show()

        elif op == 'N':
            print("Vizualização encerrada.")


        conexao.close()
    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")


def exibir_ranking_gastos(usuario):
    id_usuario = usuario[0]

    try:
        conexao, cursor = conectar_banco()

        # Usamos o Pandas para ler a query direto do banco
        query = """
            SELECT t.valor, c.nm_categoria, t.descricao
            FROM transacoes t
            JOIN categorias c ON t.id_categoria = c.id_categoria
            WHERE t.id_usuario = ? AND t.tipo = 'Saída'
            ORDER BY t.valor DESC
        """
        cursor.execute(query, (id_usuario,))
        ranking = cursor.fetchall()
        conexao.close()

        # Verifica se a lista está vazia
        if not ranking:
            print("\n[!] Você ainda não possui transações de saída para gerar um ranking.")
            return

        print("\n==============================================")
        print("      TOP 10 MAIORES GASTOS (RANKING)")


        if not ranking:
            print("\n[!] Você ainda não possui transações cadastradas.")
        else:
            contador = 0
            for m in ranking:
                print("==============================================")
                print(f" {contador + 1}º - MAIOR GASTO: R${m[0]}")
                print(f" CATEGORIA: {m[1]}")
                print(f" MOTIVO/DESC: {m[2]}")
                print("===================================================")


                contador += 1  # Aumenta 1 a cada volta
                if contador >= 10:  # Se já mostrou 10, para aqui
                    print("... (Existem mais transações, mas estas são as principais)")
                    break

            pausar()



    except Exception as e:
        print(f"\n[!] Ocorreu um erro: {e}")


