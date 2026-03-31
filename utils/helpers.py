import os

# --- FUNÇÕES UTILITÁRIAS ---
def pausar():
    # ESSA FUNÇÃO SEGURA A TELA PARA VOCÊ LER A MENSAGEM ANTES DE LIMPAR
    input("\nPRESSIONE [ENTER] PARA CONTINUAR...")
    print("\n\n\n\n")
    # Limpa a tela
    os.system('cls' if os.name == 'nt' else 'clear')