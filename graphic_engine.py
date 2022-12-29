from utils import rand, randSymbol, randCell, neighbour, riverNeighbour

class Map:
    #                0    1    2    3     4     5    6     7      8
    __CELLTYPES = ['🟩','🟫','🌲','🌳','🟦','⛰️ ', '🏥','🏭', '⬛️']
    __acsii = []
    def __init__(self, h, w):
        self.cells = [[0 for j in range(w)] for i in range(h)]
        self.h = h
        self.w = w

    def __getitem__(self, i):
        return self.cells[i]

    async def print(self, slash_inter, emb):
        for row in self.cells:
            for cell in row:
                self.__acsii.append(self.__CELLTYPES[cell])
            emb.add_field(name =''.join(self.__acsii), value =''.join(self.__acsii), inline=False)
            self.__acsii.clear()
        
        await slash_inter.send(embed = emb)
        emb.clear_fields()
            
    def checkBounds(self, x, y):
        return 0 <= x < self.h and 0 <= y < self.w


    def generateForest(self, prob):
        for row in range(self.h):
            for col in range(self.w):
                if (rand(prob)):
                    self[row][col] = randSymbol(2) + 2

    def generateLake(self, lenght = 1):
        rx, ry = randCell(self.h, self.w)
        self[rx][ry] = 4
        for i in range(lenght - 1):
            rx, ry = neighbour(rx, ry)
            if self.checkBounds(rx, ry):
                self[rx][ry] = 4
            else:
                break

    def generateMountains(self, lenght = 1):
        rx, ry = randCell(self.h, self.w)
        self[rx][ry] = 5
        for i in range(lenght - 1):
            rx, ry = neighbour(rx, ry)
            if self.checkBounds(rx, ry):
                self[rx][ry] = 5
            else:
                break       

    def generateRiver(self, lenght = 1):
        rx, ry = randCell(self.h, self.w)
        self[rx][ry] = 4
        for i in range(lenght - 1):
            rx, ry = riverNeighbour(rx, ry, 0)
            if self.checkBounds(rx, ry):
                self[rx][ry] = 4
            else:
                break
        rx, ry = randCell(self.h, self.w)
        self[rx][ry] = 4
        for i in range(lenght - 1):
            rx, ry = riverNeighbour(rx, ry, 0)
            if self.checkBounds(rx, ry):
                self[rx][ry] = 4
            else:
                break
