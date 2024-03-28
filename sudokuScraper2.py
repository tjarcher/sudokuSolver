import requests
from bs4 import BeautifulSoup
import math
import copy

print("Choose a difficulty")
print("1 is Easy, 2 is Medium, 3 is Hard, 4 is Extreme")
difficulty = input("Difficulty: ")
while difficulty not in ["1","2","3","4"]:
    print("Sorry, please enter a valid difficulty")
    print("1 is Easy, 2 is Medium, 3 is Hard, 4 is Extreme")
    difficulty = input("Difficulty: ")
url = 'https://west.websudoku.com/?level=' + str(difficulty)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


table = soup.find("table", class_ = "t")
squares = table.find_all("input")

# create blank board
board1 = [0,0,0,0,0,0,0,0,0]
board2 = [0,0,0,0,0,0,0,0,0]
board3 = [0,0,0,0,0,0,0,0,0]
board4 = [0,0,0,0,0,0,0,0,0]
board5 = [0,0,0,0,0,0,0,0,0]
board6 = [0,0,0,0,0,0,0,0,0]
board7 = [0,0,0,0,0,0,0,0,0]
board8 = [0,0,0,0,0,0,0,0,0]
board9 = [0,0,0,0,0,0,0,0,0]
board = [board1, board2, board3, board4, board5, board6, board7, board8, board9]

# read in values from websudoku.com
index = 0
for i in range(9):
    for j in range(9):
        try:
            val = squares[index]["value"]
        except:
            val = 0
        board[i][j] = int(val)
        index += 1

print("Initial Board:")
for k in range(9):
    print(board[k])
print("")

solvedSquares = 0
nines = [[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]],[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]],[[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]],[[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]],[[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]],[[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]],[[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]],[[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]],[[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]]
# create board with all possible values
possibles = []
for i in range(9):
    possibles.append([])
    for j in range(9):
        possibles[i].append([1,2,3,4,5,6,7,8,9])

def solveSquare(board, possibles, solvedSquares, row, column, value):
    status = True
    # status will go false if an error is found (no possibles and no value for a square)
    board[row][column] = value
    printPossibles(possibles)
    for w in range (9):
        print(board[w])
    print("Inserting " + str(value) + " at (" + str(row) + "," + str(column) + ")")
    print("")
    possibles[row][column] = []
    solvedSquares += 1
    for g in range(9):
        if value in possibles[g][column]:
            possibles[g][column].remove(value)
            if len(possibles[g][column]) == 0 and board[g][column] == 0:
                return False, board, possibles, solvedSquares
            if len(possibles[g][column]) == 1:
                status, board, possibles, solvedSquares = solveSquare(board, possibles, solvedSquares, g, column, possibles[g][column][0])
        if value in possibles[row][g]:
            possibles[row][g].remove(value)
            if len(possibles[row][g]) == 0 and board[row][g] == 0:
                return False, board, possibles, solvedSquares
            if len(possibles[row][g]) == 1:
                status, board, possibles, solvedSquares = solveSquare(board, possibles, solvedSquares, row, g, possibles[row][g][0])
    firstRow = (math.floor(row/3))*3
    firstColumn = (math.floor(column/3))*3
    boxRows = [firstRow, firstRow+1, firstRow+2]
    boxColumns = [firstColumn, firstColumn + 1, firstColumn + 2]
    for x in boxRows:
        for y in boxColumns:
            if value in possibles[x][y]:
                possibles[x][y].remove(value)
                if len(possibles[x][y]) == 0 and board[x][y] == 0:
                    return False, board, possibles, solvedSquares
                if len(possibles[x][y]) == 1:
                    status, board, possibles, solvedSquares = solveSquare(board, possibles, solvedSquares, x, y, possibles[x][y][0])
    
    return status, board, possibles, solvedSquares

def guessSolveSquare(board, possibles, solvedSquares, row, column, value):
    status = True
    # status will go false if an error is found (no possibles and no value for a square)
    board[row][column] = value
    printPossibles(possibles)
    for w in range (9):
        print(board[w])
    print("Inserting " + str(value) + " at (" + str(row) + "," + str(column) + ")")
    print("")
    possibles[row][column] = []
    solvedSquares += 1
    for g in range(9):
        if value in possibles[g][column]:
            possibles[g][column].remove(value)
            if len(possibles[g][column]) == 0 and board[g][column] == 0:
                return False, board, possibles, solvedSquares
        if value in possibles[row][g]:
            possibles[row][g].remove(value)
            if len(possibles[row][g]) == 0 and board[row][g] == 0:
                return False, board, possibles, solvedSquares
    firstRow = (math.floor(row/3))*3
    firstColumn = (math.floor(column/3))*3
    boxRows = [firstRow, firstRow+1, firstRow+2]
    boxColumns = [firstColumn, firstColumn + 1, firstColumn + 2]
    for x in boxRows:
        for y in boxColumns:
            if value in possibles[x][y]:
                possibles[x][y].remove(value)
                if len(possibles[x][y]) == 0 and board[x][y] == 0:
                    return False, board, possibles, solvedSquares
    
    return status, board, possibles, solvedSquares

def solveBoard(board, possibles, solvedSquares):
    improve = True
    status = True
    # improve will go false if no further moves can be made without guessing
    # status will go to false if an error is encountered (no value and no possibles for a square)
    while solvedSquares < 81 and improve == True:
        inSolve = solvedSquares
        for m in range(9):
            for n in range(9):
                if len(possibles[m][n]) == 1:
                    status, board, possibles, solvedSquares = solveSquare(board, possibles, solvedSquares, m, n, possibles[m][n][0])
                    break
                if len(possibles[m][n]) == 0 and board[m][n] == 0:
                    print("No possible values at square (" + str(m) + ", " + str(n) + ")")
                    status = False
                    return status, improve, board, possibles, solvedSquares
        if inSolve == solvedSquares:
            improve = False
            print("Cannot solve board any further")
            printPossibles(possibles)
    return status, improve, board, possibles, solvedSquares

def guessSolveBoard(board, possibles, solvedSquares):
    improve = True
    status = True
    # improve will go false if no further moves can be made without guessing
    # status will go to false if an error is encountered (no value and no possibles for a square)
    while solvedSquares < 81 and improve == True:
        inSolve = solvedSquares
        for m in range(9):
            for n in range(9):
                if len(possibles[m][n]) == 1:
                    status, board, possibles, solvedSquares = guessSolveSquare(board, possibles, solvedSquares, m, n, possibles[m][n][0])
                    break
                if len(possibles[m][n]) == 0 and board[m][n] == 0:
                    print("No possible values at square (" + str(m) + ", " + str(n) + ")")
                    status = False
                    return status, improve, board, possibles, solvedSquares
        if inSolve == solvedSquares:
            improve = False
            print("Cannot solve board any further")
            printPossibles(possibles)
    return status, improve, board, possibles, solvedSquares

def checkBoard(board):
    correct = True
    for q in range(9):
        rowCheck = []
        columnCheck = []
        for r in range(9):
            if board[q][r] in rowCheck:
                correct = False
                break
            else:
                rowCheck.append(board[q][r])
            if board[r][q] in columnCheck:
                correct = False
                break
            else:
                columnCheck.append(board[r][q])
    for s in range(9):
        squareCheck = []
        for t in range(9):
            if board[nines[s][t][0]][nines[s][t][1]] in squareCheck:
                correct = False
                break
            else:
                squareCheck.append(board[nines[s][t][0]][nines[s][t][1]])
    return correct

def printPossibles(possibles):
    print("Possibles Matrix:")
    for i in range(9):
        for j in range(9):
            print(f"({i},{j}): {possibles[i][j]}")

def guess(board, possibles, solvedSquares, saveBoard, savePossibles, saveSolvedSquares):
    saveBoard = copy.deepcopy(saveBoard)
    savePossibles = [[[value for value in row] for row in matrix] for matrix in savePossibles]
    saveSolvedSquares = saveSolvedSquares[:]
    solved = False
    checked = False
    options = 2
    while options in range(2,9) and (solved != True or checked != True):
        b = 0
        while b in range(9) and (solved != True or checked != True):
            c = 0
            while c in range(9) and (solved != True or checked != True):
                if len(possibles[b][c]) == options:
                    tempChoices = possibles[b][c]
                    for tempValue in tempChoices:
                        saveBoard.append(board)
                        savePossibles.append(possibles)
                        saveSolvedSquares.append(solvedSquares)
                        print("Solved Squares: " + str(saveSolvedSquares))
                        print("Guessing " + str(tempValue) + " at (" + str(b) + "," + str(c) + ")")
                        status, board, possibles, solvedSquares = guessSolveSquare(board, possibles, solvedSquares, b,c,tempValue)
                        status, solved, board, possibles, solvedSquares = guessSolveBoard(board, possibles, solvedSquares)
                        checked = checkBoard(board)
                        if solved == True and checked == True:
                            return board
                        else:
                            if solvedSquares == 81 or status == False:
                                board = saveBoard.pop()
                                possibles = savePossibles.pop()
                                solvedSquares = saveSolvedSquares.pop()
                                print("Solved Squares: " + str(saveSolvedSquares))
                                for w in range (9):
                                    print(board[w])
                                print("Resetting to " + str(len(saveSolvedSquares)) + " level")
                                print("")         
                            else:
                                board = guess(board, possibles, solvedSquares, saveBoard, savePossibles, saveSolvedSquares)
                c += 1
            b += 1
        options += 1
    return board


    

for j in range(9):
    for k in range(9):
        if board[j][k] != 0:
            status, board, possibles, solvedSquares = solveSquare(board, possibles, solvedSquares, j,k,board[j][k])

status, solved, board, possibles, solvedSquares = solveBoard(board, possibles, solvedSquares)

#print("Midpoint:")
#for w in range (9):
    #print(board[w])

saveBoard = []
savePossibles = []
saveSolvedSquares = []
if solved != True:
    print("\n\n\n")
    board = guess(board, possibles, solvedSquares, saveBoard, savePossibles, saveSolvedSquares)


checked = checkBoard(board)

if checked != True:
    print("Can not solve")
    for w in range (9):
        print(board[w])
else:
    print("Final Board:")
    for w in range (9):
        print(board[w])


