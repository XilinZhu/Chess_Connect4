import pygame
from pygame.locals import *
import sys
import time

# 1. parameters
# lengths
diameter = 63 * (1.18/1.11)
diameter = 74
diameter2 = 84
margin_board = diameter / 4 /0.9
# height = int(diameter * 6 + (diameter/4) * 5 + margin_board * 2)
# width = int(diameter * 7 + (diameter/4) * 6 + margin_board * 2)

height = 565
width = 632

margin_width = 0.2 * width
margin_height = 0.25 * width
boundary_left = margin_width + margin_board - (diameter2 - diameter)/2
boundary_right = width + margin_width - margin_board - (diameter2 - diameter)/2 -100
boundary_up = margin_height - diameter2
step = 13 + diameter
x_origin = margin_width + margin_board - 2
y_origin = margin_height + margin_board - 2
# colors
colorYellow = (195, 147, 101)
colorGrey = (208, 206, 206)
colorBlue = (7, 128, 213)
colorRed = (255, 2, 2)


class Hole(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(x_origin , y_origin, diameter2, diameter2)

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def loc(self, x, y):
        self.rect.x += step * x
        self.rect.y += step * (y-1)
        if x > 3 :
            self.rect.x += 2
        if x > 4:
            self.rect.x += 1
            self.rect.y += 1


class Piece(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(boundary_left, boundary_up, diameter2, diameter2)

    def moveLeft(self, x):
        if (self.rect.x > boundary_left):
           self.rect.x -= step
           x -= 1
        return x

    def moveRight(self, x):
        if (self.rect.x < boundary_right):
           self.rect.x += step
           x += 1
        return x

    def update(self, screen):
        screen.blit(self.image, self.rect)


class State():
    def __init__(self):
        self.locs1 = []
        self.locs2 = []
        self.count = 1
        self.empty = [6, 6, 6, 6, 6, 6, 6]
    
    def addable(self, x):
        if self.empty[x] > 0:
            return True
        else:
            return False

    def deepcopy(self):
        y = EmptyClass()
        y.__class__ = self.__class__  
        y.locs1 = self.locs1.copy()
        y.locs2 = self.locs2.copy()
        y.count = self.count
        y.empty = self.empty.copy()
        return y

    def add(self, x, firstAdjust):
        if (self.count + firstAdjust) % 2 == 1:
            self.locs1.append([x, self.empty[x]])
            self.empty[x] -= 1
            return self.empty[x] + 1
        else:
            self.locs2.append([x, self.empty[x]])
            self.empty[x] -= 1 
            return self.empty[x] + 1

    def addAI(self, x, player):
        self.count += 1
        if player == 1:
            self.locs1.append([x, self.empty[x]])
            self.empty[x] -= 1
            return self.empty[x] + 1
        else:
            self.locs2.append([x, self.empty[x]])
            self.empty[x] -= 1 
            return self.empty[x] + 1

    def winner(self):
        if self.count == 43:
            return 3
        if self.count >= 7:
            for locs in [self.locs1, self.locs2]:
                for loc in locs:
                    if loc[0] <= 3:
                        temp = loc[:]
                        temp[0] += 1
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            if count == 4:
                                return 1 if loc in self.locs1 else 2
                        
                        temp = loc[:]
                        temp[1] += 1
                        temp[0] += 1 
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            temp[1] += 1
                            if count == 4:
                                return 1 if loc in self.locs1 else 2

                        temp = loc[:]
                        temp[1] -= 1 
                        temp[0] += 1 
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            temp[1] -= 1
                            if count == 4:
                                return 1 if loc in self.locs1 else 2

                    temp = loc[:]
                    temp[1] += 1 
                    count = 1
                    while (temp in locs):
                        count += 1
                        temp[1] += 1
                        if count == 4:
                            return 1 if loc in self.locs1 else 2           
        return 0

    def preWinner(self):
        if self.count >= 6:
            for locs in [self.locs1, self.locs2]:
                for loc in locs:
                    if loc[0] <= 3:
                        temp = loc[:]
                        temp[0] += 1
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            if count == 3:
                                return 1

                        temp = loc[:]
                        temp[1] += 1
                        temp[0] += 1 
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            temp[1] += 1
                            if count == 3:
                                return 1

                        temp = loc[:]
                        temp[1] -= 1 
                        temp[0] += 1 
                        count = 1
                        while (temp in locs):
                            count += 1
                            temp[0] += 1
                            temp[1] -= 1
                            if count == 3:
                                return 1
                    
                    temp = loc[:]
                    temp[1] += 1 
                    count = 1
                    while (temp in locs):
                        count += 1
                        temp[1] += 1
                        if count == 3:
                            return 1
                    
                    
        return 0


class Score():
    def __init__(self, n, player):
        if player == 1:
            color = colorBlue
        else:
            color = colorRed
        myFont = pygame.font.SysFont('Arial', 80)
        self.text = myFont.render(str(n), True, color)
        self.rect = self.text.get_rect()
        if player == 1:
            self.rect.left = 50
            self.rect.top = 45
        else:
            self.rect.left = 800
            self.rect.top = 45
    
    def update(self, screen):
        screen.blit(self.text, self.rect)


class Game():
    def __init__(self, s1, s2, first):
        self.firstAdjust = first - 1
        self.screen =  pygame.display.set_mode((int(width + margin_width*2), int(height + margin_height)))
        self.state = State()
        self.holes1 = pygame.sprite.Group()
        self.holes2 = pygame.sprite.Group()
        self.chessBoard = pygame.Rect(margin_width, margin_height, width+3, height)
        self.board = pygame.image.load('img/chessBoard.png').convert_alpha()
        self.piece1 = Piece('img/piece1.png')
        self.piece2 = Piece('img/piece2.png')
        self.winner1 = pygame.image.load('img/winner1.png').convert_alpha()
        self.winner2 = pygame.image.load('img/winner2.png').convert_alpha()
        self.draw = pygame.image.load('img/draw.png').convert_alpha()
        winner_width = 457
        winner_height = 142
        margin_winner_w = int((width + margin_width*2 - winner_width)/2)
        margin_winner_h = int((margin_height - winner_height)/2) + 15
        self.winnerBoard = pygame.Rect(margin_winner_w, margin_winner_h, winner_width, winner_height)
        self.score1 = Score(s1, 1)
        self.score2 = Score(s2, 2)
        myFont = pygame.font.SysFont('Arial', 30)
        self.text = myFont.render("Player vs. Player", True, colorYellow)
        self.textRect = self.text.get_rect()
        self.textRect.left = 353
        self.textRect.top = 10
    
    def init(self):   
        pygame.init()  
        pygame.display.set_caption("Game：Connect Four") 
        self.screen.blit(self.board, self.chessBoard)
        self.screen.blit(self.text, self.textRect)
        self.score1.update(self.screen)
        self.score2.update(self.screen)
        if (self.firstAdjust == 0):
            self.piece1.update(self.screen)
        else:
            self.piece2.update(self.screen)
            
        

    def update(self):
        self.screen.fill((0,0,0))
        self.score1.update(self.screen)
        self.score2.update(self.screen)
        self.holes1.update(self.screen)
        self.holes2.update(self.screen)
        self.screen.blit(self.board, self.chessBoard)
        self.screen.blit(self.text, self.textRect)
        if ((self.state.count + self.firstAdjust) % 2 == 1):
            self.piece1.update(self.screen)
        else:
            self.piece2.update(self.screen)
        pygame.display.update()

    def updateWin(self, win, s1, s2):
        self.screen.fill((0,0,0))
        self.holes1.update(self.screen)
        self.holes2.update(self.screen)
        self.screen.blit(self.board, self.chessBoard)
        self.screen.blit(self.text, self.textRect)
        if (win == 1):
            self.screen.blit(self.winner1, self.winnerBoard)
            self.score1 = Score(s1+1, 1)
        elif (win == 2):
            self.screen.blit(self.winner2, self.winnerBoard)
            self.score2 = Score(s2+1, 2)
        else:
            self.screen.blit(self.draw, self.winnerBoard)
        self.score1.update(self.screen)
        self.score2.update(self.screen)
        pygame.display.update()

    def add(self, x, y):
        if (self.state.count + self.firstAdjust) % 2 == 1:
            hole = Hole('img/hole1.png')
            hole.loc(x, y)
            self.holes1.add(hole)
        else:
            hole = Hole('img/hole2.png')
            hole.loc(x, y)
            self.holes2.add(hole)

    def run(self, s1, s2):
        x = 0
        while(self.state.winner() == 0):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        x = self.piece1.moveLeft(x)
                        self.piece2.moveLeft(x)
                    if event.key == pygame.K_RIGHT:
                        x = self.piece1.moveRight(x)
                        self.piece2.moveRight(x)
                    if event.key == pygame.K_DOWN:
                        if self.state.addable(x):
                            y = self.state.add(x, self.firstAdjust)
                            self.add(x, y)
                            self.state.count += 1
                    self.update()
        self.updateWin(self.state.winner(), s1, s2)
    
    def wait(self):
        restart = 0
        while(restart != 1):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_t:
                        restart = 1
                    if event.key == pygame.K_m:
                        return 1
        return 0


class GameAI():
    def __init__(self, s1, s2, first, level):
        self.firstAdjust = first - 1
        self.screen =  pygame.display.set_mode((int(width + margin_width*2), int(height + margin_height)))
        self.state = State()
        self.holes1 = pygame.sprite.Group()
        self.holes2 = pygame.sprite.Group()
        self.chessBoard = pygame.Rect(margin_width, margin_height, width+3, height)
        self.board = pygame.image.load('img/chessBoard.png').convert_alpha()
        self.piece1 = Piece('img/piece1.png')
        self.piece2 = Piece('img/piece2.png')
        self.winner1 = pygame.image.load('img/winner1.png').convert_alpha()
        self.winner2 = pygame.image.load('img/winner2.png').convert_alpha()
        self.draw = pygame.image.load('img/draw.png').convert_alpha()
        winner_width = 457
        winner_height = 142
        margin_winner_w = int((width + margin_width*2 - winner_width)/2)
        margin_winner_h = int((margin_height - winner_height)/2) + 15
        self.winnerBoard = pygame.Rect(margin_winner_w, margin_winner_h, winner_width, winner_height)
        self.score1 = Score(s1, 1)
        self.score2 = Score(s2, 2)
        self.ai = AI()
        self.level = level
        myFont = pygame.font.SysFont('Arial', 30)
        self.text = myFont.render("Player vs. Computer: Level " + str(self.level), True, colorYellow)
        self.textRect = self.text.get_rect()
        self.textRect.left = 284
        self.textRect.top = 10

    def init(self):   
        pygame.init()  
        pygame.display.set_caption("Game：Connect Four") 
        self.screen.blit(self.board, self.chessBoard)
        self.score1.update(self.screen)
        self.score2.update(self.screen)            
        self.piece1.update(self.screen) 
        self.screen.blit(self.text, self.textRect)
       

    def update(self):
        self.screen.fill((0,0,0))
        self.score1.update(self.screen)
        self.score2.update(self.screen)
        self.holes1.update(self.screen)
        self.holes2.update(self.screen)
        self.screen.blit(self.board, self.chessBoard)
        self.screen.blit(self.text, self.textRect)
        if ((self.state.count + self.firstAdjust) % 2 == 1):
            self.piece1.update(self.screen)
        else:
            self.piece2.update(self.screen)
        pygame.display.update()


    def updateWin(self, win, s1, s2):
        self.screen.fill((0,0,0))
        self.holes1.update(self.screen)
        self.holes2.update(self.screen)
        self.screen.blit(self.board, self.chessBoard)
        self.screen.blit(self.text, self.textRect)
        if (win == 1):
            self.screen.blit(self.winner1, self.winnerBoard)
            self.score1 = Score(s1+1, 1)
        elif (win == 2):
            self.screen.blit(self.winner2, self.winnerBoard)
            self.score2 = Score(s2+1, 2)
        else:
            self.screen.blit(self.draw, self.winnerBoard)
        self.score1.update(self.screen)
        self.score2.update(self.screen)
        pygame.display.update()

    def add(self, x, y, player):
        if player == 1:
            hole = Hole('img/hole1.png')
            hole.loc(x, y)
            self.holes1.add(hole)
        else:
            hole = Hole('img/hole2.png')
            hole.loc(x, y)
            self.holes2.add(hole)

    def run(self, s1, s2):
        x = 0
        while(self.state.winner() == 0):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_LEFT:
                        x = self.piece1.moveLeft(x)
                        self.piece2.moveLeft(x)
                    if event.key == pygame.K_RIGHT:
                        x = self.piece1.moveRight(x)
                        self.piece2.moveRight(x)
                    if event.key == pygame.K_DOWN:
                        if self.state.addable(x):
                            y = self.state.addAI(x,1)
                            self.add(x, y, 1)
                            if (self.state.winner() != 0):
                                break
                            self.update()
                            x_ai = self.ai.nextMove(self.state, self.level)
                            y = self.state.addAI(x_ai, 0)
                            self.add(x_ai, y, 0)
                            self.update()
                    self.update()
        self.updateWin(self.state.winner(), s1, s2)
    
    def wait(self):
        restart = 0
        while(restart != 1):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_t:
                        restart = 1
                    if event.key == pygame.K_m:
                        return 1
        return 0


class AI():
    def choise(self, empty):
        choise = []
        for x in range(0,7):
            if empty[x] != 0:
                choise.append(x)
        return choise

    def nextMove(self, stateInput, n):
        empty = stateInput.empty
        choise = self.choise(empty)
        if stateInput.preWinner() != 0:         
            for x in choise:
                temp = stateInput.deepcopy()
                temp.addAI(x, 0)
                if temp.winner() == 2:
                    return x
            for x in choise:
                temp = stateInput.deepcopy()
                temp.addAI(x, 1)
                if temp.winner() == 1:
                    return x
        
        profit = []
        for x in choise:
            temp = stateInput.deepcopy()
            temp.addAI(x, 0)
            profit.append(self.search(temp, n))
        return choise[profit.index(max(profit))]

    def search(self, state, n):
        if n == 1:
            lose = 0
            if state.preWinner() == 0:
                return 0
            for x in self.choise(state.empty):
                temp = state.deepcopy()
                temp.addAI(x, 1)
                if temp.winner() == 1:
                    lose += 1
            return -lose
        else:
            profitSum = 0
            for newState1 in self.moveTry(state, 1):
                if n== 2 and newState1.winner() == 1:
                    profitSum -= 20
                    continue
                for newState in self.moveTry(newState1, 0):
                    if newState.winner() == 2:
                        if n == 3:
                            profitSum += 10
                        if n == 2:
                            profitSum += 60 
                        continue
                    profitSum += self.search(newState, n-1)
            return profitSum
    
    def moveTry(self, state, player):
        states = []
        for x in self.choise(state.empty):
            temp = state.deepcopy()
            temp.addAI(x, player)
            states.append(temp)
        return states


class Welcome():
    
    def __init__(self):
        cover_width = 580
        cover_height = 438
        margin_cover_w = int((width + margin_width*2 - cover_width)/2)
        margin_cover_h = int((height + margin_height - cover_height)/2)
        self.screen =  pygame.display.set_mode((int(width + margin_width*2), int(height + margin_height)))
        self.cover = [pygame.image.load('img/cover1.png'), pygame.image.load('img/cover1.png'), pygame.image.load('img/cover1.png'), 
                       pygame.image.load('img/cover1.png'), pygame.image.load('img/cover1.png'),pygame.image.load('img/cover2.png'),
                       pygame.image.load('img/cover3.png'),pygame.image.load('img/cover4.png'),pygame.image.load('img/cover5.png'),
                       pygame.image.load('img/cover6.png'),pygame.image.load('img/cover5.png'),pygame.image.load('img/cover4.png'),
                       pygame.image.load('img/cover3.png'),pygame.image.load('img/cover2.png')]
        self.coverBoard = pygame.Rect(margin_cover_w, margin_cover_h, cover_width, margin_height)

    def update(self, n):
        self.screen.fill((0,0,0))
        self.screen.blit(self.cover[n - 1], self.coverBoard)
        pygame.display.update()

    def run(self):
        n = 1
        welcomeStay = 1
        self.update(n)
        while(welcomeStay):
            time.sleep(0.15)
            n += 1
            self.update(n % 14)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    welcomeStay = 0


class Menu():
    def __init__(self):
        cover_width = 580
        cover_height = 438
        cover_height_real = 289
        margin_cover_w = int((width + margin_width*2 - cover_width)/2)
        margin_cover_h = int((height + margin_height - cover_height)/2)
        self.screen =  pygame.display.set_mode((int(width + margin_width*2), int(height + margin_height)))
        self.cover = pygame.image.load('img/cover0.png')
        self.coverBoard = pygame.Rect(margin_cover_w, margin_cover_h, cover_width, cover_height_real)       
        myFont = pygame.font.SysFont('Arial', 30)
        self.texts = [myFont.render("0: Player vs. Player", True, colorGrey)]
        self.texts.append(myFont.render("1: Player vs. Computer Level 1", True, colorGrey))
        self.texts.append(myFont.render("2: Player vs. Computer Level 2", True, colorGrey))
        self.texts.append(myFont.render("3: Player vs. Computer Level 3", True, colorGrey))

        self.textRects = [self.texts[0].get_rect()]
        self.textRects[0].left = 280
        self.textRects[0].top = 450
        step = 50
        i = 0 
        for i in range(1,4):
            textRect = self.texts[0].get_rect()
            textRect.left = self.textRects[0].left
            textRect.top = self.textRects[0].top + i* step
            self.textRects.append(textRect)

        

    def update(self):
        self.screen.fill((0,0,0))
        for i in range(0,4):
            self.screen.blit(self.texts[i], self.textRects[i])
        self.screen.blit(self.cover, self.coverBoard)
        pygame.display.update()
    
    def getMode(self):
        menuStay = 1
        self.update()
        while(menuStay):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        return 0
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        return 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        return 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        return 3


class GameStart():
    def __init__(self, mode):
        self.s1, self.s2 = 0, 0 
        self.first = 1
        self.mode = mode
        if mode == 0:  
            self.game = Game(self.s1, self.s2, self.first)
        else:
            self.game = GameAI(self.s1, self.s2, self.first, mode)
    
    def run(self):
        while True:
            self.game.init()
            self.game.update()
            self.game.run(self.s1, self.s2)
            if self.game.state.winner() == 1:
                self.s1 += 1
                self.first = 2
            else:
                self.s2 += 1
                self.first = 1
            if (self.game.wait() == 1):
                break
            if self.mode == 0:
                self.game = Game(self.s1, self.s2, self.first)
            else:
                self.game = GameAI(self.s1, self.s2, 1, mode)


if __name__ == "__main__":
    pygame.init()
    welcome = Welcome()
    welcome.run()

    menu = Menu()
    mode = menu.getMode()



    while(True):  
        gameStart = GameStart(mode)
        gameStart.run()

        menu.update()
        mode = menu.getMode()


