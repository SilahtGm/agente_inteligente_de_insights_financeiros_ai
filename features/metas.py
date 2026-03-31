
import sqlite3

from db.connection import conectar_banco
from utils.helpers import pausar




def criar_metas(usuario):
   id_usuario = usuario[0]

   conexao = None

   try:
        conexao, cursor = conectar_banco()

        while True:
            objetivo = str(input("Descrição da meta: "))
            valor_objetivo = float(input("Digite o valor da meta: R$"))
            prazo = str(input("Digite o prazo (AAAA-MM-DD): "))

            query = ("INSERT INTO metas_economicas (id_usuario, valor_objetivo, objetivo, prazo) VALUES (?, ?, ?, ?)")
            cursor.execute(query,(id_usuario, valor_objetivo, objetivo, prazo))
            conexao.commit()

            # 3. Verifica se o ID foi gerado (confirmação de sucesso)
            if cursor.lastrowid:
                print("\n[+] Meta criada com sucesso!")
            else:
                print("\n[!] Ocorreu um erro na criação da sua meta.")


            # Pergunta se quer continuar
            continuar = input("\nDeseja registrar outra? (S/N): ").upper()
            if continuar != 'S':
                break

   except sqlite3.Error as e:
       print(f"\n[!] Erro no Banco de Dados: {e}")
   finally:
       if conexao:
           conexao.close()


def exibir_metas(usuario):
    id_usuario = usuario[0]

    conexao = None

    try:
        conexao, cursor = conectar_banco()
        query = "SELECT  objetivo, valor_objetivo, prazo FROM metas_economicas WHERE id_usuario = ?"
        cursor.execute(query,(id_usuario,))
        metas = cursor.fetchall()


        if not metas:
            print("\n[!] Você ainda não possui metas cadastradas.")
        else:
            contador = 0
            for m in metas:
                print("===================================================")
                print(f" Objetivo: {m[0]} | Valor: R${m[1]} | Prazo: {m[2]}")
                print("===================================================")

                contador += 1  # Aumenta 1 a cada volta
                if contador >= 10:  # Se já mostrou 10, para aqui
                    print("... (Existem mais metas, mas estas são as principais)")
                    break

            pausar()


    except sqlite3.Error as e:
        print(f"\n[!] Erro no Banco de Dados: {e}")
    finally:
        if conexao:
            conexao.close()