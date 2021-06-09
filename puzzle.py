from tkinter import Frame, Label, CENTER
import tkinter.messagebox
import constants as c
import gameai
import matrix

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.move = {'UP': matrix.up, 'DOWN': matrix.down, 'LEFT': matrix.left, 'RIGHT': matrix.right}
        
        self.grid_cells = []
        self.init_grid()

        self.game = matrix.Matrix()
        self.update_grid_ui()

# for testing
#        self.game.setData([[2, 8, 4, 0], [16, 512, 32, 16], [32, 2048, 256, 64], [4, 16, 8, 2]])

        self.ai_state = True
        self.ai_run()     # Execute GameAI before starting main-loop.

        self.mainloop()

    def init_grid(self):
        bg = Frame(self, bg=c.BG_COLOR_GAME, width=400, height=400)
        bg.grid()

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = Frame(bg, bg=c.BG_COLOR_CELL_EMPTY, width=100, height=100)
                cell.grid(row=i, column=j, padx=10, pady=10)
                t = Label(master=cell, text="", bg=c.BG_COLOR_CELL_EMPTY, justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
        
    def update_grid_ui(self):
        mat = self.game.getData()  # Get values from current matrix
        for i in range(4):
            for j in range(4):
                num = mat[i][j]
                if num == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BG_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(num), bg=c.BG_COLOR_DICT[num], fg=c.CELL_COLOR_DICT[num])

    def check_game_state(self):
        if self.game.getState() == 'win':
            self.ai_state = False   # means 'Stop'
            tkinter.messagebox.showinfo('Game Over', 'You win')
            print('\nSuccess')
        if self.game.getState() == 'lose':
            self.ai_state = False   # means 'Stop'
            tkinter.messagebox.showinfo('Game Over', 'You lose')
            print('\nFailed')

    def ai_run(self):
        direction = 'NONE'
        score = 0
        if self.ai_state:
            self.after(c.AI_ENGINE_DELAY, self.ai_run)
            print('\n\n\nAI is running...')
            direction, score = gameai.get_decision(self.game, c.AI_SEARCH_DEPTH)
            print(f'Decision : {direction} with {score}')
            if direction != 'NONE':
                self.ai_move(direction) 

    def ai_move(self, direction):
        mat = self.game.getData()  # Get values from current matrix
        mat, points, done = self.move[direction](mat)
        if done:
            self.game.setData(mat)
            self.game.addPoints(points)
            self.game.addNewNum()
            self.game.printMatrix()
            self.update_grid_ui()
        self.check_game_state()

game = GameGrid()

