import constants as c
import matrix
import copy
import numpy as np

TRACE_LEVEL = 1     # 0: disabled, 1: high, 2: low


def evaluate(mat, mat_score, dir, depth):
    way = ['DOWN', 'UP', 'LEFT', 'RIGHT']
    score = mat_score + (np.size(mat) - np.count_nonzero(mat)) * c.AI_ZERO_WEIGHT
    if TRACE_LEVEL >= 2: print(f'EVALUATION:{way[dir]} - {mat}, Score : {score}, Depth : {depth}')
    return score

def get_decision(game, depth):
    comd = ['DOWN', 'UP', 'LEFT', 'RIGHT']
    func = [matrix.down, matrix.up, matrix.left, matrix.right]
    new_matrix = copy.deepcopy(game)
    best_score = 0
    best_index = 0

    if depth >= 1:
        for i in range(0, 4):
            mat2, point, done = func[i](game.getData())
            new_matrix.setData(mat2)
            new_matrix.addPoints(point)
            if done:
                new_matrix.addNewNum()
                score = evaluate(new_matrix.getData(), new_matrix.getScore(), i, depth)
                if score > best_score:
                    best_score = score
                    best_index = i
                if depth > 1:
                    cmd, score = get_decision(new_matrix, depth - 1)
                    if score > best_score:
                        best_score = score
                        best_index = i

    if TRACE_LEVEL >= 2: print(f'[{depth}] Best direction is {comd[best_index]}, {best_score}')
    return comd[best_index], best_score

# Heuristic
# assumption
# 1. 빈칸이 많을 수록 좋다.
# 2. 큰 수를 만들 수 있는 방향으로 이동하는 것이 좋다.
# 3. 주변의 타일과 숫자의 level 차이가 작을 수록 좋다.
