import random
 
class Matrix:
    def __init__(self):
        self.matrix = [[0 for i in range(4)] for j in range(4)]
        self.score = 0
        self.addNewNum()
        self.addNewNum()

    def addNewNum(self):
        while True:
            a = random.randint(0, len(self.matrix)-1)
            b = random.randint(0, len(self.matrix)-1)
            if self.matrix[a][b] == 0:
                self.matrix[a][b] = 2
                return True
    
    def getScore(self):
        return self.score

    def addPoints(self, points):
        self.score += points

    def getData(self):
        return self.matrix
    
    def setData(self, mat):
        self.matrix = mat

    def printMatrix(self):
        print(f'matrix score = {self.score}')
        for i in range(4):
            print(self.matrix[i])

    def getState(self):
        # check for win cell
        stat = 'lose'
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] >= 2048:
                    stat = 'win'

        # check for any zero entries
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    return 'not over'
        # check for same cells that touch each other
        for i in range(4):
            # intentionally reduced to check the row on the right and below
            for j in range(3):
                if self.matrix[i][j+1] == self.matrix[i][j]:
                    return 'not over'
        for j in range(4):
            for i in range(3):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return 'not over'

        return stat



def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


def cover_up(mat):
    new = []
    for j in range(4):
        partial_new = []
        for i in range(4):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat, done):
    points = 0
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                points += mat[i][j]
                mat[i][j+1] = 0
                done = True
    return mat, points, done


def up(mat):
    # return matrix after shifting up
    mat = transpose(mat)
    mat, done = cover_up(mat)
    mat, points, done = merge(mat, done)
    mat = cover_up(mat)[0]
    mat = transpose(mat)
    return mat, points, done


def down(mat):
    mat = reverse(transpose(mat))
    mat, done = cover_up(mat)
    mat, points, done = merge(mat, done)
    mat = cover_up(mat)[0]
    mat = transpose(reverse(mat))
    return mat, points, done


def left(mat):
    # return matrix after shifting left
    mat, done = cover_up(mat)
    mat, points, done = merge(mat, done)
    mat = cover_up(mat)[0]
    return mat, points, done


def right(mat):
    # return matrix after shifting right
    mat = reverse(mat)
    mat, done = cover_up(mat)
    mat, points, done = merge(mat, done)
    mat = cover_up(mat)[0]
    mat = reverse(mat)
    return mat, points, done
