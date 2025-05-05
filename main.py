from threading import Thread
import os
from Levels.level import Level
import pygame
import copy
from Levels.CurrentLevels import CurrentLevels
from utils.funcs import *
from Solvers.DFS import *
from Solvers.BFS import *
from Solvers.A_Star import *
from Solvers.GreedyBestFirst import *
from Solvers.IDA import *  
from Solvers.MCTS import * 

APP_FOLDER = os.path.dirname( os.path.realpath( __file__ ) )+os.path.sep+'assets'

# Loading assets

icon = pygame.image.load(os.path.join(APP_FOLDER, "icon.png"))
aStarBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn.png"))
bfsBtn = pygame.image.load(os.path.join(APP_FOLDER, "bfsBtn.png"))
dfsBtn = pygame.image.load(os.path.join(APP_FOLDER, "dfsBtn.png"))
bestBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn2.png"))  # Add a new best search button 
backBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn2.png"))  # Add a new back button 
idaBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn2.png"))  # Add a new IDDFS button 
mctsBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn2.png"))  # MCTS button
hungarianBtn = pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn2.png"))  # Hungarian button

crate = pygame.image.load(os.path.join(APP_FOLDER, "crate.png"))
treasure = pygame.image.load(os.path.join(APP_FOLDER, "treasure.png"))

wb = pygame.image.load(os.path.join(APP_FOLDER, "wb.png"))
wl = pygame.image.load(os.path.join(APP_FOLDER, "wl.png"))
wr = pygame.image.load(os.path.join(APP_FOLDER, "wr.png"))
wt = pygame.image.load(os.path.join(APP_FOLDER, "wt.png"))
wb = pygame.image.load(os.path.join(APP_FOLDER, "wb.png"))
wlt = pygame.image.load(os.path.join(APP_FOLDER, "wlt.png"))
wlb = pygame.image.load(os.path.join(APP_FOLDER, "wlb.png"))
wrt = pygame.image.load(os.path.join(APP_FOLDER, "wrt.png"))
wrb = pygame.image.load(os.path.join(APP_FOLDER, "wrb.png"))

wtb = pygame.image.load(os.path.join(APP_FOLDER, "wtb.png"))
wlr = pygame.image.load(os.path.join(APP_FOLDER, "wlr.png"))
w3l = pygame.image.load(os.path.join(APP_FOLDER, "w3l.png"))
w3r = pygame.image.load(os.path.join(APP_FOLDER, "w3r.png"))
w3t = pygame.image.load(os.path.join(APP_FOLDER, "w3t.png"))
w3b = pygame.image.load(os.path.join(APP_FOLDER, "w3b.png"))
w4 = pygame.image.load(os.path.join(APP_FOLDER, "w4.png"))
charS = pygame.image.load(os.path.join(APP_FOLDER, "charS.png"))

tl = (pygame.image.load(os.path.join(APP_FOLDER, "tl1.png")),pygame.image.load(os.path.join(APP_FOLDER, "tl2.png")))
td = (pygame.image.load(os.path.join(APP_FOLDER, "td1.png")),pygame.image.load(os.path.join(APP_FOLDER, "td2.png")))
tls =(pygame.image.load(os.path.join(APP_FOLDER, "tls1.png")),pygame.image.load(os.path.join(APP_FOLDER, "tls2.png")))
tds = (pygame.image.load(os.path.join(APP_FOLDER, "tds1.png")),pygame.image.load(os.path.join(APP_FOLDER, "tds2.png")))
coin = (pygame.image.load(os.path.join(APP_FOLDER, "c1.png")), pygame.image.load(os.path.join(APP_FOLDER, "c2.png")), pygame.image.load(os.path.join(APP_FOLDER, "c3.png")), pygame.image.load(os.path.join(APP_FOLDER, "c4.png")), pygame.image.load(os.path.join(APP_FOLDER, "c5.png")), pygame.image.load(os.path.join(APP_FOLDER, "c6.png")), pygame.image.load(os.path.join(APP_FOLDER, "c7.png")), pygame.image.load(os.path.join(APP_FOLDER, "c8.png")))
char = (pygame.image.load(os.path.join(APP_FOLDER, "char1.png")), pygame.image.load(os.path.join(APP_FOLDER, "char2.png")))
animPtr = 0

clock = pygame.time.Clock()

levels = []
levelIndex = -1


def render(currLevel, screen):
    '''
    This function helps in the rendering of each items onto the screen. 
    It calculates the pixel value of each element and blits it to its appropriate position in the screen.
    '''
    x = (416-32*currLevel.rows)//2
    for i in range(0, currLevel.rows):
        y = (416-32*currLevel.cols)//2
        for j in range(0, currLevel.cols):
            if currLevel.matrix[i][j]  == 1:
                wallType = wallFreeFaces(currLevel.matrix, (i, j))
                if len(wallType) == 1:
                    if(i+j)%2 == 0:
                        screen.blit(td[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                    if (0, 1) in wallType:
                        screen.blit(wl, (y, x))
                    elif (0, -1) in wallType:
                        screen.blit(wr, (y, x))
                    elif (1, 0) in wallType:
                        screen.blit(wt, (y, x))
                    elif (-1, 0) in wallType:
                        screen.blit(wb, (y, x))
                elif len(wallType) == 2:
                    if(i+j)%2 == 0:
                        screen.blit(td[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                    if (0, 1) in wallType:
                        if (1, 0) in wallType:
                            screen.blit(wlt, (y, x))
                        elif (-1, 0) in wallType:
                            screen.blit(wlb, (y, x))
                        else:
                            screen.blit(wtb, (y, x))
                    elif (0, -1) in wallType:
                        if (1, 0) in wallType:
                            screen.blit(wrt, (y, x))
                        elif (-1, 0) in wallType:
                            screen.blit(wrb, (y, x))
                    else:
                        screen.blit(wlr, (y, x))
                elif len(wallType) == 3:
                    if(i+j)%2 == 0:
                        screen.blit(td[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                    if (0, 1) not in wallType:
                        screen.blit(w3r, (y, x))
                    elif (0, -1) not in wallType:
                        screen.blit(w3l, (y, x))
                    elif (1, 0) not in wallType:
                        screen.blit(w3b, (y, x))
                    elif (-1, 0) not in wallType:
                        screen.blit(w3t, (y, x))
                elif len(wallType) == 4:
                    if(i+j)%2 == 0:
                        screen.blit(td[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                    screen.blit(w4, (y, x))

            elif(currLevel.matrix[i][j]) == 5:
                if(i+j)%2 == 0:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tds[(i*j)%2], (y, x))
                    else:
                        screen.blit(td[(i*j)%2], (y, x))
                else:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tls[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                screen.blit(treasure, (y, x))
            elif(currLevel.matrix[i][j]) == 2:
                if(i+j)%2 == 0:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tds[(i*j)%2], (y, x))
                    else:
                        screen.blit(td[(i*j)%2], (y, x))
                else:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tls[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                if(currLevel.playerY == i-1 and currLevel.playerX == j):
                    screen.blit(charS, (y, x))
                screen.blit(coin[animPtr%8], (y, x))
            elif(currLevel.matrix[i][j]) == 3:
                if(i+j)%2 == 0:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tds[(i*j)%2], (y, x))
                    else:
                        screen.blit(td[(i*j)%2], (y, x))
                else:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tls[(i*j)%2], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                screen.blit(crate, (y, x))
            elif(currLevel.matrix[i][j]) == 0:
                if(i+j)%2 == 0:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tds[(i*j)%2], (y, x))
                    else:
                        screen.blit(td[(i*j)%2], (y, x))
                else:
                    if currLevel.matrix[i-1][j] == 1:
                        screen.blit(tls[(i*j)%2-1], (y, x))
                    else:
                        screen.blit(tl[(i*j)%2], (y, x))
                if(currLevel.playerY == i-1 and currLevel.playerX == j):
                    screen.blit(charS, (y, x))
            if(currLevel.playerX == j and currLevel.playerY == i):
                screen.blit(char[animPtr%2], (y, x))
            y += 32
        x += 32
    
    screen.blit(bfsBtn, (45.5, 360))
    screen.blit(aStarBtn, (169, 360))
    screen.blit(dfsBtn, (292.5, 360))
    
    
    screen.blit(bestBtn, (45.5, 310))  # Best-First button 
    screen.blit(idaBtn, (169, 310))  # IDA* button 
    screen.blit(mctsBtn, (292.5, 310))  # MCTS button
    
    screen.blit(hungarianBtn, (292.5, 10))  # Hungarian heuristic button
    screen.blit(backBtn, (10, 10))  # Back button
    

def automator(moves, state, screen):
    '''
    This function automatically executes moves stored in th list <moves>.
    '''
    global animPtr
    for step in moves:
        move(state, step)
        screen.fill((53, 73, 94))
        animPtr += 1
        render(state, screen)
        pygame.display.update()
        pygame.time.wait(100)

def gameScreen(currLevel, levelIndex, levels):
    '''
    Main game function that will initiate the game loop.
    '''
    buffer = 0
    global animPtr
    pygame.init()
    # pygame.mixer.init()
    
    # Track current heuristic selection
    use_hungarian = False
   
    pygame.display.set_caption("SokoBot")
    pygame.display.set_icon(icon)
    screen2 = pygame.display.set_mode((416, 416))
    
    end = False
    while not end:
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if isLegal(currLevel, (0, -1)):
                        vals = (0, -1)
                        move(currLevel, vals)
                elif event.key == pygame.K_DOWN:
                    vals = (0, 1)
                    if isLegal(currLevel, (0, 1)): move(currLevel, vals)
                elif event.key == pygame.K_LEFT:
                    if isLegal(currLevel, (-1, 0)):
                        vals = (-1, 0)
                        move(currLevel, vals)
                elif event.key == pygame.K_RIGHT:
                    if isLegal(currLevel, (1, 0)):
                        vals = (1, 0)
                        move(currLevel, vals)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 10 <= mouse[0] <= 60 and 10 <= mouse[1] <= 40:  # Back button hit area
                    return "back"  # Return to level selection
                
                # Top row buttons (BFS, A*, DFS)
                if 45.5 <= mouse[0] <= 123.5 and 360 <= mouse[1] <= 393:  # BFS button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    solution = track_complexity(breadthFirstSearch, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                if 169 <= mouse[0] <= 247 and 360 <= mouse[1] <= 393:  # A* button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    if use_hungarian:
                        solution = track_complexity(aStarHungarian, currLevel , levelIndex)
                    else:
                        solution = track_complexity(aStarManhattan, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                if 292.5 <= mouse[0] <= 370.5 and 360 <= mouse[1] <= 393:  # DFS button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    solution = track_complexity(depthFirstSearch, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                # Middle row buttons (Best-First, IDA*, MCTS)
                if 45.5 <= mouse[0] <= 123.5 and 310 <= mouse[1] <= 343:  # Best-First button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    if use_hungarian:
                        solution = track_complexity(GreedyBestFirsthungarian, currLevel , levelIndex)
                    else:
                        solution = track_complexity(GreedyBestFirstManhattan, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                if 169 <= mouse[0] <= 247 and 310 <= mouse[1] <= 343:  # IDA* button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    if use_hungarian:
                        solution = track_complexity(ida_star_hungarian, currLevel , levelIndex)
                    else:
                        solution = track_complexity(ida_star_manhattan, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                if 292.5 <= mouse[0] <= 370.5 and 310 <= mouse[1] <= 343:  # MCTS button
                    currLevel = copy.deepcopy(levels[levelIndex])
                    if use_hungarian:
                        solution = track_complexity(mcts_hungarian, currLevel , levelIndex)
                    else:
                        solution = track_complexity(mcts_manhattan, currLevel , levelIndex)
                    if solution:
                        t1 = Thread(target=automator, args=(solution.timeLine, currLevel, screen2))
                        t1.start()
                        t1.join()
                
                # Toggle Hungarian heuristic
                if 292.5 <= mouse[0] <= 370.5 and 10 <= mouse[1] <= 40:  # Hungarian toggle button
                    use_hungarian = not use_hungarian
                    heuristic_name = "Hungarian" if use_hungarian else "Manhattan"
                    print(f"Switched to {heuristic_name} heuristic")

            if check(currLevel):
                currLevel = copy.deepcopy(levels[levelIndex])
        
        screen2.fill((53, 73, 94))
        buffer += 1
        if not buffer%4:
            animPtr += 1
        render(currLevel, screen2)
        
        pygame.display.update()

def levelSelectScreen(levels_set):
    '''
    Level selection screen that shows all available levels
    '''
    end = False
    pygame.init()
    screen = pygame.display.set_mode((416, 416))
    pygame.display.set_caption("SokoBot")
    pygame.display.set_icon(icon)
    
    
    bg_color = (30, 41, 59)  # Darker blue background
    title_color = (129, 230, 217)  # Teal/cyan
    text_color = (255, 220, 130)  # Warm yellow
    button_color = (79, 70, 229)  # Purple for buttons
    button_hover_color = (99, 102, 241)  # Lighter purple for hover
    
    font = pygame.font.SysFont('Cascadia mono', 40)
    smallFont = pygame.font.SysFont('Cascadia mono', 24)
    title = font.render('Select Level', True, title_color, bg_color)
    backText = smallFont.render('Back', True, text_color, button_color)
    
    # Calculate how many levels to show per page and total pages
    levels_per_page = 7
    total_pages = (len(levels_set) + levels_per_page - 1) // levels_per_page
    current_page = 0
    
    while not end:
        clock.tick(24)
        screen.fill(bg_color)
        screen.blit(title, (125, 20))
        
        # Create level buttons for current page
        start_idx = current_page * levels_per_page
        end_idx = min(start_idx + levels_per_page, len(levels_set))
        
        for i in range(start_idx, end_idx):
            level_idx = i
            level_y = 80 + ((i - start_idx) * 40)
            level_text = smallFont.render(f'Level {level_idx + 1}', True, text_color, button_color)
            pygame.draw.rect(screen, button_color, (150, level_y, 120, 30), 0, border_radius=5)
            screen.blit(level_text, (185, level_y+7))
        
        
        # Back button
        pygame.draw.rect(screen, button_color, (10, 10, 60, 30), 0, border_radius=5)
        screen.blit(backText, (20, 18))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                # Check if back button clicked
                if 10 <= mouse[0] <= 70 and 10 <= mouse[1] <= 40:
                    return "back"
                
                # Check if level buttons clicked
                for i in range(start_idx, end_idx):
                    level_idx = i
                    level_y = 80 + ((i - start_idx) * 40)
                    if 150 <= mouse[0] <= 270 and level_y <= mouse[1] <= level_y + 30:
                        return level_idx
                
                # Check if prev/next page buttons clicked
                if current_page > 0 and 50 <= mouse[0] <= 150 and 360 <= mouse[1] <= 390:
                    current_page -= 1
                if current_page < total_pages - 1 and 266 <= mouse[0] <= 366 and 360 <= mouse[1] <= 390:
                    current_page += 1
        
        pygame.display.update()

def startScreen(levelIndex, levels):
    end = False
    pygame.init()
    screen1 = pygame.display.set_mode((416, 416))
    pygame.display.set_caption("SokoBot")
    pygame.display.set_icon(icon)
    
    # More appealing colors
    bg_color = (30, 41, 59)  # Darker blue background
    title_color = (129, 230, 217)  # Teal/cyan for title
    button_text_color = (255, 220, 130)  # Warm yellow for button text
    button_hover_color = (99, 102, 241)  # Purple for button hover
    
    # Track button hover states
    easy_hover = False
    hard_hover = False
    
    while not end:
        clock.tick(6)
        screen1.fill(bg_color)
        screen1.blit(pygame.transform.scale(icon, (80, 80)), (168, 10))
        font = pygame.font.SysFont('Cascadia mono', 64)
        font2 = pygame.font.SysFont('Cascadia mono', 32)
        title = font.render('SokoBot', True, title_color, bg_color)
        
        # Check if mouse is hovering over buttons
        mouse = pygame.mouse.get_pos()
        easy_hover = 105 <= mouse[0] <= 310 and 200 <= mouse[1] <= 232
        hard_hover = 105 <= mouse[0] <= 310 and 250 <= mouse[1] <= 282
        
        # Draw button backgrounds with hover effect
        easy_bg_color = button_hover_color if easy_hover else (79, 70, 229)
        # hard_bg_color = button_hover_color if hard_hover else (79, 70, 229)
        
        pygame.draw.rect(screen1, easy_bg_color, (110, 200, 200, 32), 0, border_radius=5)
        # pygame.draw.rect(screen1, hard_bg_color, (110, 250, 200, 32), 0, border_radius=5)
        
        # Render button text
        choice1 = font2.render('LEVELS', True, button_text_color)
        # choice2 = font2.render('Hard', True, button_text_color)
        
        screen1.blit(title, (115, 100))
        screen1.blit(choice1, (170, 205))
        # screen1.blit(choice2, (185, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if 105 <= mouse[0] <= 310 and 200 <= mouse[1] <= 232:
                    levels_set = copy.deepcopy(CurrentLevels)
                    while True:
                        selected_level_idx = levelSelectScreen(levels_set)
                        if selected_level_idx == "back":
                            break
                        elif selected_level_idx is None:
                            end = True
                            break
                        else:
                            currLevel = copy.deepcopy(levels_set[selected_level_idx])
                            result = gameScreen(currLevel, selected_level_idx, levels_set)
                            if result == "back":
                                continue
                            else:
                                end = True
                                break

                # if 105 <= mouse[0] <= 310 and 250 <= mouse[1] <= 282:
                #     levels_set = copy.deepcopy(HardLevels)
                #     while True:
                #         selected_level_idx = levelSelectScreen(levels_set)
                #         if selected_level_idx == "back":
                #             break
                #         elif selected_level_idx is None:
                #             end = True
                #             break
                #         else:
                #             currLevel = copy.deepcopy(levels_set[selected_level_idx])
                #             result = gameScreen(currLevel, selected_level_idx, levels_set)
                #             if result == "back":
                #                 continue
                #             else:
                #                 end = True
                #                 break

        pygame.display.update()

startScreen(levelIndex, levels)