from random import random, randint

def rand(prob): ## generate true if prob > random or false 
    return random() < prob/100

def randSymbol(n):
    return randint(0, n-1)

def randCell(w, h):
    return randint(0, w-1), randint(0, h-1)

def neighbour(x, y):
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    move = moves[randint(0, 3)]
    return x+move[0], y+move[1]

def riverNeighbour(x, y, ban):
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    moves.pop(ban)
    move = moves[randint(0, 2)]
    return x+move[0], y+move[1]

def randToCard():
    int = randint(0, 12)
    cards = ['двойка', 'тройка', 'четверка', 'пятерка', 'шестёрка', 'семёрка', 'восьмёрка', 'девятка', 'десятка', 'валет', 'дама', 'король', 'туз']
    return cards[int]

def cardValue(cards):
    value = {'двойка': 2, 'тройка': 3, 'четверка': 4, 'пятерка': 5, 'шестёрка': 6, 'семёрка': 7, 'восьмёрка': 8, 'девятка': 9, 'десятка': 10, 'валет': 10, 'дама': 10, 'король': 10, 'туз': 11}
    ans = []
    for i in range(len(cards)):
        card = cards[i]
        if card in value:
            ans.append(value[f'{card}'])
        else:
            return 'Something went wrong while check cardvalue'
    return sum(ans)
