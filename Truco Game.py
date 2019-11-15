from random import shuffle
import sys
import time

naipes = ['Espadas', 'Copas', 'Paus', 'Ouros']
numbers = [4, 5, 6, 7, 'Q', 'J', 'K', 'A', 2, 3]
name = ['Primeiro Jogador', 'Segundo Jogador', 'Terceiro Jogador', 'Quarto Jogador']
regras = open('regras.txt')

cont1, cont2, match1, match2, matchpoint = 0, 0, 0, 0, 1

def welcomeTruco():
    print('''Bem-vindo ao Truco em Python!        
created by: Gustavo Lira and Fábio Tepedino''')
    menu = 0
    while menu != 4:
        jumpLine()
        print('''[1] Jogar
[2] Alterar o Nome dos Jogadores
[3] Como Jogar
[4] Sair do Programa''')
        try: menu = int(input('>>>> '))
        except: print('Tá errado')
        if menu == 1: break
        if menu == 2: nameDefinition(), time.sleep(2)
        if menu == 3: print(regras.read()), time.sleep(5), regras.close()
        if menu == 4: sys.exit('Fim do Programa. Volte Sempre!')

def generateCardDeck():
    cards = []
    for naipe in naipes:
        for number in numbers:
            card = (f'{number} de {naipe}')
            cards.append(card)
    return cards

def nameDefinition():
    for n in range(0,4):
        name[n] = input(f'Digite o nome do jogador {n + 1}: ').title()
    jumpLine()
    print(f'{name[0]} e {name[2]} são do Time 1')
    print(f'{name[1]} e {name[3]} são do Time 2')

def shuffleEffect():
    jumpLine(), print('EMBARALHANDO CARTAS...'), time.sleep(1)

def generateShuffleDeck():
    deck = generateCardDeck()
    shuffle(deck)
    return deck

def players(hand):
    playerone = hand[0:3]
    playertwo = hand[3:6]
    playerthree = hand[6:9]
    playerfour = hand[9:12]
    return playerone, playertwo, playerthree, playerfour

def choiceCard(hand, deck):
    global matchpoint
    while cont1 or cont2 <= 2:
        try: pos = int(input(f'Escolha uma carta [1-{len(hand)}] [4 para trucar]: ')) - 1
        except: continue
        if pos == 3: trucoChallenge('TRUCO! A rodada está valendo 3 pontos. [5 para double truco]', 3)
        if pos == 4: trucoChallenge('DOUBLE TRUCO! A rodada está valendo 6 pontos. [6 para ultimate truco]', 6)
        if pos == 5: trucoChallenge('ULTIMATE TRUCO! A rodada vale a partida.', 12)
        try: deck.append(hand[pos])
        except: continue
        del hand[pos]
        jumpLine()
        print('Cartas na mesa:', deck)
        if pos in range (0,3): break

def biggerCard(a, b):

    numbers = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    manilhas = ['7', 'A', '7', '4']
    naipes = ['Ouros', 'Espadas', 'Copas', 'Paus']
    aManilha, bManilha = False, False

    for i in range(0, 4):
        if a[0] == manilhas[i] and a[1] == naipes[i]:
            aManilha = True
            p1 = 10 + i

        if b[0] == manilhas[i] and b[1] == naipes[i]:
            bManilha = True
            p2 = 10 + i

    if not aManilha:
        for i in range(0, 10):
            if a[0] == numbers[i]:
                p1 = i

    if not bManilha:
        for i in range(0, 10):
            if b[0] == numbers[i]:
                p2 = i

    if p1 > p2:
        return a
    elif p1 < p2:
        return b
    elif p1 == p2:
        return 0

def compareCards(deck):
    global cont1, cont2
    p1 = [deck[0][0], deck[0][5:]]
    p2 = [deck[1][0], deck[1][5:]]
    p3 = [deck[2][0], deck[2][5:]]
    p4 = [deck[3][0], deck[3][5:]]

    team1 = biggerCard(p1, p3)
    if team1 == 0: team1 = p1

    team2 = biggerCard(p2, p4)
    if team2 == 0: team2 = p2

    winner = biggerCard(team1, team2)
    if winner == 0: print('Empate!')
    if winner == team1:
        cont1 += 1
        print('Time 1 venceu a rodada')
    if winner == team2:
        cont2 += 1
        print('Time 2 venceu a rodada')
    print(f'Pontuação Time 1: {cont1}')
    print(f'Pontuação Time 2: {cont2}')
    jumpLine()

def trucoChallenge(msg, t):
    global matchpoint
    print(msg)
    matchpoint = (matchpoint * 0) + t
    jumpLine()

def playerTurn(msg, nome, p):
    print(msg, nome)
    print(p)
    choiceCard(p, list)
    jumpLine()

def roundVictory(msg):
    global matchpoint, cont1, cont2
    print(msg)
    print('PONTUAÇÃO TOTAL')
    print('Time 1 x Time 2')
    print(f'   {match1}   x    {match2}  ')
    time.sleep(1), shuffleEffect()
    matchpoint, cont1, cont2 = 1, 0, 0

def matchVictoryConditions(mat, msg):
    if mat >= 12:
        jumpLine()
        print(msg)
        sys.exit()

def gameMatch():
    global cont1, cont2, match1, match2, matchpoint
    playerone, playertwo, playerthree, playerfour = players(generateShuffleDeck())
    jumpLine()

    while True:
        for r in range(0,3):
            playerTurn('Time 1 -', name[0], playerone)
            playerTurn('Time 2 -', name[1], playertwo)
            playerTurn('Time 1 -', name[2], playerthree)
            playerTurn('Time 2 -', name[3], playerfour)

            compareCards(list)
            for p in range(0,4):
                list.pop()

        if cont1 > cont2 or cont1 == cont2:
            match1 += matchpoint
            roundVictory('Time 1 venceu')
            break

        if cont2 > cont1:
            match2 += matchpoint
            roundVictory('Time 2 venceu')
            break

def jumpLine():
    print('')

list = []

welcomeTruco()
while True:
    gameMatch()
    matchVictoryConditions(match1, 'Fim do Jogo! Vitória do time 1')
    matchVictoryConditions(match2, 'Fim do Jogo! Vitória do time 2')
    continue






