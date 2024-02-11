import math
# initialize board
board1 = [1,2,3,4,5,6,7,8,9]
board2 = [7,8,9,1,2,3,4,5,6]
board3 = [4,5,6,7,8,9,1,2,3]
board4 = [2,3,4,5,6,7,8,9,1]
board5 = [5,6,7,8,9,1,2,3,4]
board6 = [8,9,1,2,3,4,5,6,7]
board7 = [3,4,5,6,7,8,9,1,2]
board8 = [6,7,8,9,1,2,3,4,5]
board9 = [0,0,0,0,0,0,0,0,0]
board = [board1, board2, board3, board4, board5, board6, board7, board8, board9]
solvedSquares = 0
nines = [[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]],[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]],[[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]],[[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]],[[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]],[[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]],[[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]],[[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]],[[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]]]
# create board with all possible values
possibles = []
for i in range(9):
    possibles.append([])
    for j in range(9):
        possibles[i].append([1,2,3,4,5,6,7,8,9])

def solveSquare(row, column, value):
    board[row][column] = value
    possibles[row][column] = []
    global solvedSquares
    solvedSquares += 1
    for g in range(9):
        if value in possibles[g][column]:
            possibles[g][column].remove(value)
            if len(possibles[g][column]) == 1:
                solveSquare(g, column, possibles[g][column][0])
        if value in possibles[row][g]:
            possibles[row][g].remove(value)
            if len(possibles[row][g]) == 1:
                solveSquare(row, g, possibles[row][g][0])
    firstRow = (math.floor(row/3))*3
    firstColumn = (math.floor(column/3))*3
    boxRows = [firstRow, firstRow+1, firstRow+2]
    boxColumns = [firstColumn, firstColumn + 1, firstColumn + 2]
    for x in boxRows:
        for y in boxColumns:
            if value in possibles[x][y]:
                possibles[x][y].remove(value)
                if len(possibles[x][y]) == 1:
                    solveSquare(x, y, possibles[x][y][0])

def solveBoard():
    improve = True
    while solvedSquares < 81 and improve == True:
        inSolve = solvedSquares
        for m in range(9):
            for n in range(9):
                if len(possibles[m][n]) == 1:
                    solveSquare(m, n, possibles[m][n][0])
                    break
        if inSolve == solvedSquares:
            improve = False
    return improve

def checkBoard():
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

    

for j in range(9):
    for k in range(9):
        if board[j][k] != 0:
            solveSquare(j,k,board[j][k])

solved = solveBoard()

if solved != True:
    for options in range(2,9):
        for b in range(9):
            for c in range(9):
                if len(possibles[b][c]) == options:
                    tempChoices = possibles[b][c]
                    for tempValue in tempChoices:
                        saveBoard = board
                        savePossibles = possibles
                        saveSolvedSquares = solvedSquares
                        solveSquare(b,c,tempValue)
                        solved = solveBoard()
                        checked = checkBoard()
                        if solved == True and checked == True:
                            break
                        else:
                            board = saveBoard
                            possibles = savePossibles
                            solvedSquares = saveSolvedSquares
                if solved == True and checked == True:
                    break
                else:
                    board = saveBoard
                    possibles = savePossibles
                    solvedSquares = saveSolvedSquares


checked = checkBoard()

if solved != True or checked != True:
    print("Can not solve")
else:
    for w in range (9):
        print(board[w])
    


    