#DEPENDENCIAS E SUGESTÕES:
    # 1 - BAIXE E INSTALE O SQLITE
    # 2 - RECOMENDADO USAR SQLITESTUDIO PARA VER E MANIPULAR BD
    # 3 - BAIXAR EXTENSÕES DO VSCODE: SQLITE e SQLITE Viewer
    # 4 - TALVEZ PRECISE MUDAR O DIRETORIO DA VARIAVEL 'caminho'

import sqlite3

# Dicionário de Cores:
cores = {
    'default': '\033[m',
    'vermelho-sub': '\033[4;31m',
    'azul':'\033[34m',
    'brazil':'\033[42;33m'
}
 
### Conexão
caminho = ".\\db_Filmes.db"

def conectar(caminho):
    conexao = None
    try:
        conexao = sqlite3.connect(caminho)
        print('Conectado com sucesso!')
    except sqlite3.Error as er:
        print(er)
    return conexao


### FUNÇÕES DE PROCEDIMENTOS DO BANCO
# Criando tabela
def criarTabela(conexao, comando):
    try:
        cursor = conexao.cursor()
        cursor.execute(comando)
        
        print('{}Tabela criada com sucesso{}'.format(cores['azul'], cores['default']))
    except sqlite3.Error as er:
        print(er)

#funcao mostrar tabela
def MostrarTabela(conexao):
    try:
        cursor = conexao.cursor()
        comandoMostrarTabela = """
        SELECT *
        FROM TB_FILMES;
        """
        cursor.execute(comandoMostrarTabela)
        
        #imprimindo linhas
        for linha in cursor.fetchall():
            print(linha)
    except sqlite3.Error as er:
        print(er)


# INSERÇÃO DE DADOS

def preencher():
    print(f'\n{"PREENCHENDO":=^20}')
    campo = [
        str(input('TÍTULO DO FILME -> ')).upper(),
        str(input('GÊNERO -> ')).capitalize(),
        int(input('ANO DE LANÇAMENTO -> ')),
        int(input('BILHETERIA -> '))
    ]
    return campo

def inserirDados(conexao):
    campos = preencher()

    comando = f"""
    INSERT INTO tb_Filmes
    (TITULO, GENERO, ANO, BILHETERIA) VALUES
    ('{campos[0]}', '{campos[1]}', '{campos[2]}', {campos[3]});
    """
    
    try:
        cursor = conexao.cursor()
        cursor.execute(comando)
        conexao.commit()

        print("{}Dados inseridos com sucesso!{}".format(cores['azul'], cores['default']))

    except sqlite3.Error as er:
        print(er)

# "TRUNCATE"
comandoTruncar = """
DELETE FROM tb_Filmes;
"""
def truncar(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute(comandoTruncar)
        conexao.commit()
        print('Tabela zerada com sucesso')
    except sqlite3.Error as er:
        print(er)

# DELETAR LINHA ESPECIFICA
def deletarlinha(conexao):
    linha = int(input('Qual o {}ID{} do produto deseja excluir? '.format(cores['vermelho-sub'], cores['default'])))
    cursor = conexao.cursor()
    comando = f"""
DELETE FROM tb_Filmes
WHERE CODIGO = {linha};"""
    
    try:
        cursor.execute(comando)
        conexao.commit()
        print(f'Peça de ID #{linha} deletado com sucesso!')
    except sqlite3.Error as er:
        print(er)

# Apagar tabela
def dropTable(conexao):
    comando = "DROP TABLE tb_Filmes"
    try:
        cursor = conexao.cursor()
        cursor.execute(comando)
        print('Tabela apagada com sucesso!')
    except sqlite3.Error as er:
        print(er)

# Atualizar uma célula
def update(conexao, qnt):
    print("\n{}{:=^25}{}".format(cores['brazil'], 'UPDATE', cores['default']))
    
    ordem = 1

    while ordem <= qnt:
        if qnt > 1:
            print(f'==={ordem}º Update===')
        
        ordem += 1

        id = int(input('Qual o {}ID{} da linha que deseja alterar o valor -> '.format(cores['vermelho-sub'], cores['default'])))

        while True:
            print(f'{"Qual a coluna":=^25}')
            print("""
            [1] TITULO
            [2] GENERO
            [3] ANO
            [4] BILHETERIA""")

            numColuna = int(input('\nSUA RESPOSTA -> '))

            if numColuna == 1:
                nomeColuna = 'TITULO'
                break
            elif numColuna == 2:
                nomeColuna = 'GENERO'
                break
            elif numColuna == 3:
                nomeColuna = 'ANO'
                break
            elif numColuna == 4:
                nomeColuna = 'BILHETERIA'
                break
            else:
                print(f'{"Resposta Inválida":=^25}')
        
        if nomeColuna != 'valor':
            dado = str(input('VALOR NOVO -> '))
        else:
            while True:
                try:
                    dado = float(input('VALOR NOVO -> '))
                    break

                except ValueError:
                    print('Digite apenas valores numéricos!')
                    print(f'{"TENTE NOVAMENTE":-^25}') 

        comandoUpdate = f"""
        UPDATE tb_Filmes
        SET {nomeColuna} = '{dado}'
        WHERE rowid = {id};"""

        try:
            cursor = conexao.cursor()
            cursor.execute(comandoUpdate)
            conexao.commit()
        except sqlite3.Error as er:
            print(er)

### Menu
def menu(conexao):
    print(f"""
    {'MENU':=^20}
    [1] INSERIR DADOS
    [2] ATUALIZAR DADO
    [3] DELETAR LINHA
    
    [0] Sair""")
    
    try:
        resp = int(input('SUA RESPOSTA -> '))
        if resp == 1:
            inserirDados(conexao)
        elif resp == 2:
            print('\nESCOLHA UMA OPÇÃO:')
            print('[1] Atualizar apenas um dado')
            print('[2] Atualizar vários dados')
            opcao = int(input('\nResposta -> '))

            if opcao == 1:
                update(conexao, 1)
            else:
                qnt = int(input('Quantos dados deseja atualizar? '))
                update(conexao, qnt)

        elif resp == 3:
            deletarlinha(conexao)
        elif resp == 0:
            exit()
        elif resp == 16082003:
            truncar(conexao)           #Comando oculto
        else:
            print('\n=== Valor inválido. Tente novamente!===\n')
            menu(conexao)

    except ValueError as ve:
        print('\n=== Valor inválido. Tente novamente!===\n')
        menu(conexao)

def resetTable(conexao):
    dropTable(conexao)
    
    comandoCriarTabela = """
    CREATE TABLE tb_Filmes (
    CODIGO INTEGER PRIMARY KEY,
    TITULO VARCHAR (50),
    GENERO VARCHAR (30),
    ANO INTEGER,
    BILHETERIA INTEGER
        )"""

    criarTabela(vcon, comandoCriarTabela)
    # Se já existe será printado "Already Exists"


### Iniciando procedimentos

# Estabelecer conexão
vcon = conectar(caminho) 
# resetTable(vcon)

menu(vcon)

# Chamando a função MostrarTabela
MostrarTabela(vcon)

vcon.close()
