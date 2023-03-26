import pygame

from collections import deque

pygame.init()

screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()

pygame.display.set_caption("Chain Game")
icon = pygame.image.load('ChainGame.jpg')
pygame.display.set_icon(icon)

gridImg = pygame.image.load('grid.png')
redImg = pygame.image.load('redsquare.png')
yellowImg = pygame.image.load('yellowsquare.png')
darkRedImg = pygame.image.load('darkredsquare.png')
darkYellowImg = pygame.image.load('darkyellowsquare.png')

firstTurn = True
redTurn = True
prevTurn = (-1, -1)
redTileCount = 0
yellowTileCount = 0

# status stores the colour of each tile: either white, red or yellow
status = [[0] * 8 for i in range(8)]
for x in range(8):
    for y in range(8):
        status[x][y] = "white"
adjMatrix = [['w'] * 64 for i in range(64)]
xcoords = [216, 298, 380, 462, 544, 626, 708, 790]
ycoords = [46, 128, 210, 292, 374, 456, 538, 620]


def gamebutton(x, y, gridX, gridY, clickevent=None):
    global redTurn
    global firstTurn
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + 73 > mouse[0] > x and y + 73 > mouse[1] > y:
        if redTurn:
            screen.blit(darkRedImg, (x, y))
        else:
            screen.blit(darkYellowImg, (x, y))
        if click[0] == 1 and clickevent != None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    clickevent(gridX, gridY)


def gameclickevent(gridX, gridY):
    global redTurn
    global firstTurn
    global prevTurn
    global adjMatrix
    global redTileCount
    global yellowTileCount
    if prevTurn != (gridX, gridY):
        if redTurn and not firstTurn and status[gridX][gridY] != "red" and (
                (gridY != 0 and status[gridX][gridY - 1] == "red") or (gridX != 7 and status[gridX + 1][gridY] == "red") or (gridY != 7 and status[gridX][
                gridY + 1] == "red") or (gridX != 0 and status[gridX - 1][gridY] == "red")):
            

            redTileCount += 1
            if status[gridX][gridY] == "yellow":
                
                status[gridX][gridY] = "red"
                yellowTileCount -= 1
                #print(bfs_v3([prevTurn],[prevTurn], redTurn, redTileCount, yellowTileCount, 1, 1, status))
                print(bfs_v4(status, prevTurn, [], redTurn, 1, 1, redTileCount, yellowTileCount))
            prevTurn = (gridX, gridY)
            status[gridX][gridY] = "red"
            redTurn = False
            #bfs([(gridX, gridY)])


        elif not redTurn and not firstTurn and status[gridX][gridY] != "yellow" and (
                (gridY != 0 and status[gridX][gridY - 1] == "yellow") or (gridX != 7 and status[gridX + 1][gridY] == "yellow") or (gridY != 7 and status[gridX][
            gridY + 1] == "yellow") or (gridX != 0 and status[gridX - 1][gridY] == "yellow")):


            yellowTileCount += 1
            if status[gridX][gridY] == "red":
                status[gridX][gridY] = "yellow"
                redTileCount -= 1
                #print(bfs_v3([prevTurn],[prevTurn], redTurn, redTileCount, yellowTileCount, 1, 1, status))
                print(bfs_v4(status, prevTurn, [], redTurn, 1, 1, redTileCount, yellowTileCount))

            prevTurn = (gridX, gridY)
            status[gridX][gridY] = "yellow"
            redTurn = True
            #bfs([(gridX, gridY)])


        elif redTurn and firstTurn:
            if status[gridX][gridY] == "yellow":
                yellowTileCount -= 1
            status[gridX][gridY] = "red"
            redTurn = False
            redTileCount += 1
            prevTurn = (gridX, gridY)
            #bfs([(gridX, gridY)])
            #print(bfs_v3([prevTurn],[prevTurn], redTurn, redTileCount, yellowTileCount, 1, 1, status))
        elif not redTurn and firstTurn:
            if status[gridX][gridY] == "red":
                redTileCount -= 1
            status[gridX][gridY] = "yellow"
            # change it to red turn after bfs is completed
            # does bfs only need to run if e.g. red cell has been taken over by yellow? Surely yes?
            # bfs not needed on first turn
            yellowTileCount += 1
            firstTurn = False
            prevTurn = (gridX, gridY)
            #bfs([(gridX, gridY)])
            #print(bfs_v3([prevTurn],[prevTurn], redTurn, redTileCount, yellowTileCount, 1, 1, status))
            redTurn = True

# determines if win condition is met
def bfs(tileList):
    # tileList starts containing only the cell that the player has just clicked on
    global adjMatrix
    global redTurn
    global redTileCount
    global yellowTileCount
    global status

    # adjCount is the number of adjacencies. i.e. if 2 cells border each other, that would be 1 adjacency. 3 adjacent cells = 2 adjacencies
    adjCount = 1
    visitedList = []
    print("NEW TILE")

    # if it is yellow's turn:
    if not redTurn:

        # while tileList is not empty and adjacency count is less than or equal to yellow tile count:
        while tileList and adjCount <= yellowTileCount:
            x = tileList[0][0]
            y = tileList[0][1]

            # if tile has not yet been visited:
            if (x, y) not in visitedList:

                # if there exists a tile to the north and it has not been visited, is not in the waiting list and is also yellow:
                if y != 0 and (x, y-1) not in visitedList and (x, y-1) not in tileList and status[x][y-1] == "yellow":

                    # adjCount must always be less than or equal to the tile count, so we make sure it is less than before incrementing it.
                    # INCORRECT: in a 3x3 square grid where all tiles are filled in, there are 12 adjacencies
                    # instead: run a bfs from the clicked tile. 
                    #  If number of found tiles < redTileCount, yellow wins.
                    if adjCount < yellowTileCount:
                        adjCount += 1
                    print("(" + str(x) + ", " + str(y-1) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")

                    # add the north tile to the waiting list
                    tileList.append((x, y-1))

                if x != 7 and (x+1, y) not in visitedList and (x+1, y) not in tileList and status[x+1][y] == "yellow":
                    if adjCount < yellowTileCount:
                        adjCount += 1
                    print("(" + str(x+1) + ", " + str(y) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x+1, y))
                if y != 7 and (x, y+1) not in visitedList and (x, y+1) not in tileList and status[x][y+1] == "yellow":
                    if adjCount < yellowTileCount:
                        adjCount += 1
                    print("(" + str(x) + ", " + str(y+1) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x, y+1))
                if x != 0 and (x-1, y) not in visitedList and (x-1, y) not in tileList and status[x-1][y] == "yellow":
                    if adjCount < yellowTileCount:
                        adjCount += 1
                    print("(" + str(x-1) + ", " + str(y) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x-1, y))
                visitedList.append((x, y))
            tileList.pop(0)
            print("adjCount is " + str(adjCount))
            print("yellowTileCount is " + str(yellowTileCount))
            print('Visited list is {0}'.format(visitedList))
        if adjCount < yellowTileCount:
            print("Red wins!")
    else:
        while tileList and adjCount <= redTileCount:
            x = tileList[0][0]
            y = tileList[0][1]
            if (x, y) not in visitedList:
                if y != 0 and (x, y-1) not in visitedList and (x, y-1) not in tileList and status[x][y - 1] == "red":
                    if adjCount < redTileCount:
                        adjCount += 1
                    print("(" + str(x) + ", " + str(y-1) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x, y - 1))
                if x != 7 and (x+1, y) not in visitedList and (x+1, y) not in tileList and status[x + 1][y] == "red":
                    if adjCount < redTileCount:
                        adjCount += 1
                    print("(" + str(x+1) + ", " + str(y) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x + 1, y))
                if y != 7 and (x, y+1) not in visitedList and (x, y+1) not in tileList and status[x][y + 1] == "red":
                    if adjCount < redTileCount:
                        adjCount += 1
                    print("(" + str(x) + ", " + str(y+1) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x, y + 1))
                if x != 0 and (x-1, y) not in visitedList and (x-1, y) not in tileList and status[x - 1][y] == "red":
                    if adjCount < redTileCount:
                        adjCount += 1
                    print("(" + str(x-1) + ", " + str(y) + ") is adjacent to (" + str(x) + ", " + str(y) + ")")
                    tileList.append((x - 1, y))
                visitedList.append((x, y))
            tileList.pop(0)
            print("adjCount is " + str(adjCount))
            print("redTileCount is " + str(redTileCount))
            print('Visited list is {0}'.format(visitedList))
        if adjCount < redTileCount:
            print("Yellow wins!")

def bfs_v2(visitedList, tileList, redTurn, actualRedCount, actualYellowCount, knownRedCount, knownYellowCount, status):
    # tileList starts containing only the tile that the player has just clicked on.
    # tileList is a 'waiting list' or queue of tiles that are known to exist and have yet to be visited.

    x = tileList[0][0]
    y = tileList[0][1]

    # pop (x, y) from tileList
    tileList.pop(0)

    # add the current tile (x, y) to the visited list    
    visitedList.append((x, y))

    # if the RED player has just placed a tile:
    if redTurn:

        # we now check if RED has won the game, by seeing if YELLOW's tiles have been broken up.
        while tileList:


            # if there exists a tile to the north and it has not been visited, is not in the waiting list and is also yellow:
            if y != 0 and (x, y-1) not in visitedList and (x, y-1) not in tileList and status[x][y-1] == "yellow":

                # add the north tile to the waiting list
                tileList.append((x, y-1))

                # increment the known yellow count as we have found a new yellow tile
                knownYellowCount += 1

            # if there exists a tile to the east and it has not been visited, is not in the waiting list and is also yellow:
            if x != 7 and (x+1, y) not in visitedList and (x+1, y) not in tileList and status[x+1][y] == "yellow":

                # add the east tile to the waiting list
                tileList.append((x+1, y))

                # increment the known yellow count as we have found a new yellow tile
                knownYellowCount += 1

            # if there exists a tile to the south and it has not been visited, is not in the waiting list and is also yellow:
            if y != 7 and (x, y+1) not in visitedList and (x, y+1) not in tileList and status[x][y+1] == "yellow":

                # add the south tile to the waiting list
                tileList.append((x, y+1))

                # increment the known yellow count as we have found a new yellow tile
                knownYellowCount += 1

            # if there exists a tile to the west and it has not been visited, is not in the waiting list and is also yellow:
            if x != 0 and (x-1, y) not in visitedList and (x-1, y) not in tileList and status[x-1][y] == "yellow":

                # add the west tile to the waiting list
                tileList.append((x-1, y))

                # increment the known yellow count as we have found a new yellow tile
                knownYellowCount += 1    
                

# recursive bfs to count the number of adjacent tiles of the same colour
# knownRedCount and knownYellowCount should be initialised as 1
def bfs_v3(visitedList, tileList, redTurn, actualRedCount, actualYellowCount, knownRedCount, knownYellowCount, status):

    # change this to start from an adjacent tile to the one that was clicked on

    if not tileList:
        return "sodium"
        if not redTurn and actualRedCount > knownRedCount:
            return "YELLOW wins!"
        elif redTurn and actualYellowCount > knownYellowCount:
            return "RED wins!"
        else:
            return "Keep playing!"

    # pop tile from tileList
    currentTile = tileList.pop(0)
    x = currentTile[0]
    y = currentTile[1]
    print("x = " + str(x))
    print("y = " + str(y))

    if redTurn:

        # if there exists a tile to the north and it has not been visited, is not in the waiting list and is also yellow:
        if y != 0 and (x, y-1) not in visitedList and status[x][y-1] == "yellow":

            # add the north tile to the visited list
            visitedList.append((x, y-1))

            # add the north tile to the waiting list
            tileList.append((x, y-1))

            # increment the known yellow count as we have found a new yellow tile
            knownYellowCount += 1

        # if there exists a tile to the east and it has not been visited, is not in the waiting list and is also yellow:
        if x != 7 and (x+1, y) not in visitedList and status[x+1][y] == "yellow":

            # add the east tile to the waiting list
            tileList.append((x+1, y))

            # increment the known yellow count as we have found a new yellow tile
            knownYellowCount += 1

        # if there exists a tile to the south and it has not been visited, is not in the waiting list and is also yellow:
        if y != 7 and (x, y+1) not in visitedList and status[x][y+1] == "yellow":

            # add the south tile to the waiting list
            tileList.append((x, y+1))

            # increment the known yellow count as we have found a new yellow tile
            knownYellowCount += 1

        # if there exists a tile to the west and it has not been visited, is not in the waiting list and is also yellow:
        if x != 0 and (x-1, y) not in visitedList and status[x-1][y] == "yellow":

            # add the west tile to the waiting list
            tileList.append((x-1, y))

            # increment the known yellow count as we have found a new yellow tile
            knownYellowCount += 1

    else:

        # if there exists a tile to the north and it has not been visited, is not in the waiting list and is also red:
        if y != 0 and (x, y-1) not in visitedList and status[x][y-1] == "red":

            # add the north tile to the visited list
            visitedList.append((x, y-1))

            # add the north tile to the waiting list
            tileList.append((x, y-1))

            # increment the known red count as we have found a new red tile
            knownRedCount += 1

        # if there exists a tile to the east and it has not been visited, is not in the waiting list and is also red:
        if x != 7 and (x+1, y) not in visitedList and status[x+1][y] == "red":

            # add the east tile to the waiting list
            tileList.append((x+1, y))

            # increment the known red count as we have found a new red tile
            knownRedCount += 1

        # if there exists a tile to the south and it has not been visited, is not in the waiting list and is also red:
        if y != 7 and (x, y+1) not in visitedList and status[x][y+1] == "red":

            # add the south tile to the waiting list
            tileList.append((x, y+1))

            # increment the known red count as we have found a new red tile
            knownRedCount += 1

        # if there exists a tile to the west and it has not been visited, is not in the waiting list and is also red:
        if x != 0 and (x-1, y) not in visitedList and status[x-1][y] == "red":

            # add the west tile to the waiting list
            tileList.append((x-1, y))

            # increment the known red count as we have found a new red tile
            knownRedCount += 1

    bfs_v3(visitedList, tileList, redTurn, actualRedCount, actualRedCount, knownRedCount, knownYellowCount, status)

def bfs_v4(status, tile, visitedList, redTurn, knownRedCount, knownYellowCount, actualRedCount, actualYellowCount):
    
    x = tile[0]
    y = tile[1]

    print("Starting from " + str(x), ", " + str(y))

    q = deque()

    visitedList.append(tile)

    q.append(tile)

    while q:
    
        tile = q.popleft()

        x = tile[0]
        y = tile[1]

        adjTiles = [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]

        for i in range(4):
            x = adjTiles[i][0]
            y = adjTiles[i][1]
            print("Checking " + str(x), ", " + str(y))
            if x == -1 or y == -1 or x == 8 or y == 8:
                break
            if redTurn and (x,y) not in visitedList and status[x][y] == "yellow":
                visitedList.append((x, y))
                q.append((x, y))
                print("Counting " + str(x) + ", " + str(y))
                knownYellowCount += 1
                print(str(knownYellowCount))
            if not redTurn and (x,y) not in visitedList and status[x][y] == "red":
                visitedList.append((x, y))
                q.append((x, y))
                print("Counting " + str(x) + ", " + str(y))
                knownRedCount += 1
                print(str(knownRedCount))

    if redTurn and knownYellowCount < actualYellowCount:
        return "Red wins!"
    elif not redTurn and knownRedCount < actualRedCount:
        return "Yellow wins!"
    else:
        return "Keep playing!"


        

        

    





running = True
while running:
    pygame.display.update()
    screen.fill((0, 0, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(gridImg, (210, 40))

    # for x in xcoords:
    # for y in ycoords:
    # for a in range(8):
    # for b in range(8):
    # gamebutton(x, y, a, b, gameclickevent)

    gamebutton(216, 46, 0, 0, gameclickevent)
    gamebutton(298, 46, 1, 0, gameclickevent)
    gamebutton(380, 46, 2, 0, gameclickevent)
    gamebutton(462, 46, 3, 0, gameclickevent)
    gamebutton(544, 46, 4, 0, gameclickevent)
    gamebutton(626, 46, 5, 0, gameclickevent)
    gamebutton(708, 46, 6, 0, gameclickevent)
    gamebutton(790, 46, 7, 0, gameclickevent)

    gamebutton(216, 128, 0, 1, gameclickevent)
    gamebutton(298, 128, 1, 1, gameclickevent)
    gamebutton(380, 128, 2, 1, gameclickevent)
    gamebutton(462, 128, 3, 1, gameclickevent)
    gamebutton(544, 128, 4, 1, gameclickevent)
    gamebutton(626, 128, 5, 1, gameclickevent)
    gamebutton(708, 128, 6, 1, gameclickevent)
    gamebutton(790, 128, 7, 1, gameclickevent)

    gamebutton(216, 210, 0, 2, gameclickevent)
    gamebutton(298, 210, 1, 2, gameclickevent)
    gamebutton(380, 210, 2, 2, gameclickevent)
    gamebutton(462, 210, 3, 2, gameclickevent)
    gamebutton(544, 210, 4, 2, gameclickevent)
    gamebutton(626, 210, 5, 2, gameclickevent)
    gamebutton(708, 210, 6, 2, gameclickevent)
    gamebutton(790, 210, 7, 2, gameclickevent)

    gamebutton(216, 292, 0, 3, gameclickevent)
    gamebutton(298, 292, 1, 3, gameclickevent)
    gamebutton(380, 292, 2, 3, gameclickevent)
    gamebutton(462, 292, 3, 3, gameclickevent)
    gamebutton(544, 292, 4, 3, gameclickevent)
    gamebutton(626, 292, 5, 3, gameclickevent)
    gamebutton(708, 292, 6, 3, gameclickevent)
    gamebutton(790, 292, 7, 3, gameclickevent)

    gamebutton(216, 374, 0, 4, gameclickevent)
    gamebutton(298, 374, 1, 4, gameclickevent)
    gamebutton(380, 374, 2, 4, gameclickevent)
    gamebutton(462, 374, 3, 4, gameclickevent)
    gamebutton(544, 374, 4, 4, gameclickevent)
    gamebutton(626, 374, 5, 4, gameclickevent)
    gamebutton(708, 374, 6, 4, gameclickevent)
    gamebutton(790, 374, 7, 4, gameclickevent)

    gamebutton(216, 456, 0, 5, gameclickevent)
    gamebutton(298, 456, 1, 5, gameclickevent)
    gamebutton(380, 456, 2, 5, gameclickevent)
    gamebutton(462, 456, 3, 5, gameclickevent)
    gamebutton(544, 456, 4, 5, gameclickevent)
    gamebutton(626, 456, 5, 5, gameclickevent)
    gamebutton(708, 456, 6, 5, gameclickevent)
    gamebutton(790, 456, 7, 5, gameclickevent)

    gamebutton(216, 538, 0, 6, gameclickevent)
    gamebutton(298, 538, 1, 6, gameclickevent)
    gamebutton(380, 538, 2, 6, gameclickevent)
    gamebutton(462, 538, 3, 6, gameclickevent)
    gamebutton(544, 538, 4, 6, gameclickevent)
    gamebutton(626, 538, 5, 6, gameclickevent)
    gamebutton(708, 538, 6, 6, gameclickevent)
    gamebutton(790, 538, 7, 6, gameclickevent)

    gamebutton(216, 620, 0, 7, gameclickevent)
    gamebutton(298, 620, 1, 7, gameclickevent)
    gamebutton(380, 620, 2, 7, gameclickevent)
    gamebutton(462, 620, 3, 7, gameclickevent)
    gamebutton(544, 620, 4, 7, gameclickevent)
    gamebutton(626, 620, 5, 7, gameclickevent)
    gamebutton(708, 620, 6, 7, gameclickevent)
    gamebutton(790, 620, 7, 7, gameclickevent)

    for a in range(8):
        for b in range(8):
            if status[a][b] == "red":
                screen.blit(redImg, (xcoords[a], ycoords[b]))
            elif status[a][b] == "yellow":
                screen.blit(yellowImg, (xcoords[a], ycoords[b]))

    pygame.display.update()
