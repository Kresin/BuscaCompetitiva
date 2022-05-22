from math import inf as infinity
from random import choice
import platform
import time
from os import system

humano = -1
computador = +1
# Matriz do mapa do jogo da velha
mapa = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


# Função para calcular a heurística do estado
# estato: O estado atual do jogo
# retorna +1 caso o computador ganhe, -1 caso o humano ganhe ou 0 em caso de um empate
def calcula_heuristica(estado):
    if verifica_vitoria(estado, computador):
        valor = +1
    elif verifica_vitoria(estado, humano):
        valor = -1
    else:
        valor = 0

    return valor

# Verifica se algum dos jogadores(humano ou computador) ganhou a partida.
# Condições de vitória:
# Uma linha inteira com X ou O;
# Uma coluna inteira com X ou O;
# Uma diagonal inteira com X ou O;
def verifica_vitoria(estado, jogador):
    condicoes_vitoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador, jogador, jogador] in condicoes_vitoria:
        return True
    else:
        return False


# Verifica se o computador ou humano vencem o jogo em um determinado estado
def fim_de_jogo(estado):
    return verifica_vitoria(estado, humano) or verifica_vitoria(estado, computador)


# Obtém todos os espaços vazios do tabuleiro atual
def celulas_vazias(estado):
    celulas = []

    for x, linha in enumerate(estado):
        for y, celula in enumerate(linha):
            if celula == 0:
                celulas.append([x, y])

    return celulas


# Verifica se o movimento é válido. Um movimento só é valido caso a posição informada esteja vazia ou dentro dos
# alcances da matriz
def verifica_movimento_valido(x, y):
    if [x, y] in celulas_vazias(mapa):
        return True
    else:
        return False


# Adiciona o X ou O no mapa caso a jogada seja válida
def salvar_jogada(x, y, jogador):
    if verifica_movimento_valido(x, y):
        mapa[x][y] = jogador
        return True
    else:
        return False


# Algoritmo de mimimax para calcular a melhor jogado possível para o estado atual do jogo
# profundeza: índice do nó na árvore (0 <= índice <= 9) de jogadas
# Retorna uma lista contendo a linha e coluna da jogada junto do valor dessa jogada
def minimax(estado, profundeza, jogador):
    if jogador == computador:
        melhor_valor = [-1, -1, -infinity]
    else:
        melhor_valor = [-1, -1, +infinity]

    if profundeza == 0 or fim_de_jogo(estado):
        placar = calcula_heuristica(estado)
        return [-1, -1, placar]

    for celula in celulas_vazias(estado):
        x, y = celula[0], celula[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundeza - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == computador:
            if placar[2] > melhor_valor[2]:
                melhor_valor = placar  # max value
        else:
            if placar[2] < melhor_valor[2]:
                melhor_valor = placar  # min value

    return melhor_valor


# Limpa o console
def limpar_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


# Renderiza o tabuleiro do jogo no console
def printa_tabuleiro(estado, caracter_computador, caracter_humano):
    caracteres = {
        -1: caracter_humano,
        +1: caracter_computador,
        0: ' '
    }
    linha_pontilhada = '---------------'

    print('\n' + linha_pontilhada)
    for linha in estado:
        for celula in linha:
            caracter = caracteres[celula]
            print(f'| {caracter} |', end='')
        print('\n' + linha_pontilhada)


# Chama o algoritmo de minimax caso a profundeza da árvore seja inferior a 9, senão escolhe a coordenada faltante no
# mapa, pois será a última jogada
def turno_computador(caracter_computador, caracter_humano):
    profundeza = len(celulas_vazias(mapa))
    if profundeza == 0 or fim_de_jogo(mapa):
        return

    limpar_console()
    print(f'Turno do computador [{caracter_computador}]')
    printa_tabuleiro(mapa, caracter_computador, caracter_humano)

    if profundeza == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        jogada = minimax(mapa, profundeza, computador)
        x, y = jogada[0], jogada[1]

    salvar_jogada(x, y, computador)
    time.sleep(1)


# Pede para o jogador humano informar uma jogada válida
def turno_humano(caracter_computador, caracter_humano):
    profundeza = len(celulas_vazias(mapa))
    if profundeza == 0 or fim_de_jogo(mapa):
        return

    # Dicionário de jogadas válidas
    jogada = -1
    jogadas = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpar_console()
    print(f'Turno do humano [{caracter_humano}]')
    printa_tabuleiro(mapa, caracter_computador, caracter_humano)

    while jogada < 1 or jogada > 9:
        try:
            jogada = int(input('Informe um valor númerico entre 1 e 9: '))
            coordenada = jogadas[jogada]
            jogada_valida = salvar_jogada(coordenada[0], coordenada[1], humano)

            if not jogada_valida:
                print('Jogada inválida')
                jogada = -1
        except (EOFError, KeyboardInterrupt):
            print('Ocorreu um erro ao computar a sua jogada.')
            exit()
        except (KeyError, ValueError):
            print('Ocorreu um erro ao computar a sua jogada.')


# Método main responsável por chamar as funções do programa
def main():
    limpar_console()
    caracter_humano = ''  # X ou O
    caracter_computador = ''  # X ou O
    primeiro = ''  # Indica que joga por primeiro

    # O jogador humano escolhe qual caracter ele quer
    while caracter_humano != 'O' and caracter_humano != 'X':
        try:
            print('')
            caracter_humano = input('Escolha entre X ou O\nEscolhido: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Erro ao escolher o caracter')
            exit()
        except (KeyError, ValueError):
            print('Erro ao escolher o caracter')

    # Salva a escolha de caracter
    if caracter_humano == 'X':
        caracter_computador = 'O'
    else:
        caracter_computador = 'X'

    # Verifica se o jogador humano quer começar por primeiro
    limpar_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Quer começar jogando?[s/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Erro ao indicar se quer começar jogando')
            exit()
        except (KeyError, ValueError):
            print('Erro ao indicar se quer começar jogando')

    # Loop do jogo
    while len(celulas_vazias(mapa)) > 0 and not fim_de_jogo(mapa):
        if primeiro == 'N':
            turno_computador(caracter_computador, caracter_humano)
            primeiro = ''

        turno_humano(caracter_computador, caracter_humano)
        turno_computador(caracter_computador, caracter_humano)

    # Mensagem de fim de jogo
    if verifica_vitoria(mapa, humano):
        limpar_console()
        print(f'Turno do humano [{caracter_humano}]')
        printa_tabuleiro(mapa, caracter_computador, caracter_humano)
        print('Você venceu!')
    elif verifica_vitoria(mapa, computador):
        limpar_console()
        print(f'Turno do computador [{caracter_computador}]')
        printa_tabuleiro(mapa, caracter_computador, caracter_humano)
        print('Você perdeu!')
    else:
        limpar_console()
        printa_tabuleiro(mapa, caracter_computador, caracter_humano)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()
