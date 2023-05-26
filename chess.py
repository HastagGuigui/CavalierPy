import sys, pygame

knightPos = [16, 15]
knightSpritePos = [0, 0]

# les variables de base
size = width, height = 700, 700 #Taille de l'écran
white = 247, 237, 203 #Couleur des cases blanches
black = 102, 66, 42 #Couleur des cases noires
green = 0, 255, 0, 50 #Couleur des cases où l'on peut aller

boardSize = 1920, 1920, 32, 32 #Variables du plateau de jeu (Longueur, largeur, nombre de cases sur chaque côté.)

camPos = [((knightPos[0]+0.5) * boardSize[0] // boardSize[2]) - width//2, ((knightPos[1]+0.5) * boardSize[1] // boardSize[3]) - height//2]

knightMoves = []

firstMove = input("Input first move (x;y)").split(";")
if firstMove == ["00", "00"]: #Mouvement de cavalier de base
    knightMoves = [
        [1, 2],
        [2, 1],
        [-1, 2],
        [-2, 1],
    ]
elif firstMove == ["01", "00"]: #Mouvement de cavalier de base
    knightMoves = [
        [1, 2],
        [-1, 2],
        [-2, 1],
    ]
else:
    # raise NotImplementedError("sorry, recoding the base movement system")
    knightMoves.append( [int(firstMove[0]), int(firstMove[1])] )

    # Prédiction du second mouvement:
    xn = 0 - knightMoves[0][0]
    yn = 1 - knightMoves[0][1]

    secondMove = input("Input second move (x;y)").split(";")

    # knightMoves.append( [xn, yn] )
    knightMoves.append( [int(secondMove[0]), int(secondMove[1])] )

pygame.init() #Démarre l'application
screen = pygame.display.set_mode(size) #Mettre en place la taille de l'écran

knight = pygame.image.load("./knight.png") #Cavalier
knightrect = knight.get_rect()

theFont = pygame.font.Font("./04B03.otf", 16) #Police de caractères, peu important

positionsThatWeWentTo = [ #Pour pouvoir rajouter des carrés rouges là où on est
    knightPos
]

# le jeu en lui-même
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() #Pour quitter le jeu

        if event.type == pygame.MOUSEBUTTONDOWN:
            #Ici, on transforme un clic de souris en déplacement de cavalier
            mousepos = pygame.mouse.get_pos()
            if mousepos[0] - (width-boardSize[0])/2 > 0 and mousepos[0] - (width-boardSize[0])/2 < boardSize[0]: # good on the X-axis
                if mousepos[1] - (width-boardSize[1])/2 > 0 and mousepos[1] - (width-boardSize[1])/2 < boardSize[1]: # good on the Y-axis
                    selSquare = [
                        int(((mousepos[0]+camPos[0]) - ((width - boardSize[0])/2)) / (boardSize[0]/boardSize[2])-0.5) -10,
                        int(((mousepos[1]+camPos[1]) - ((height- boardSize[1])/2)) / (boardSize[1]/boardSize[3])-0.5) -10,
                    ]
                    print(selSquare, knightPos, [knightPos[i] - selSquare[i] for i in range(2)])

                    # maintenant trouver si ce carré est sélectionnable

                    selsqToMove = [
                        selSquare[0] - knightPos[0],
                        selSquare[1] - knightPos[1]
                    ]
                    opposMove = [
                        -selsqToMove[0],
                        -selsqToMove[1]
                    ]
                    if selsqToMove in knightMoves or opposMove in knightMoves:
                        knightPos = selSquare
                        positionsThatWeWentTo.append(selSquare)

                    camPos = [((knightPos[0]+0.5) * boardSize[0] // boardSize[2]) - width//2, ((knightPos[1]+0.5) * boardSize[1] // boardSize[3]) - height//2]



    #Taille de chaque case, utilisée pour afficher les cases à l'écran
    square_w = boardSize[0] / boardSize[2]
    square_h = boardSize[1] / boardSize[3]

    #Position du cavalier à l'écran
    knightPos[0] = max(min(knightPos[0],boardSize[2]), 0)

    knightrect.x = 40 - (knight.get_width()/2) + 60*knightPos[0] - camPos[0]
    knightrect.y = 40 - (knight.get_height()/2) + 60*knightPos[1] - camPos[1]

    #------------ [CE QUI EST VISIBLE A L'ECRAN] ------------#
    screen.fill((0,0,0))
    for y in range(boardSize[3]): #Dessiner la grille
        for x in range(boardSize[2]):
            if (x+y) % 2 == 0:
                pygame.draw.rect(screen, white, pygame.rect.Rect(x*square_w+10 - camPos[0], y*square_h+10 - camPos[1], square_w,square_h))
            else:
                pygame.draw.rect(screen, black, pygame.rect.Rect(x*square_w+10 - camPos[0], y*square_h+10 - camPos[1], square_w,square_h))


    for move in knightMoves:
        square_x = knightPos[0] + move[0]
        square_y = knightPos[1] + move[1]
        oppsqr_x = knightPos[0] - move[0]
        oppsqr_y = knightPos[1] - move[1]
        pygame.draw.rect(screen, green, pygame.rect.Rect(square_x*square_w+20 - camPos[0], square_y*square_h+20 - camPos[1], square_w - 20,square_h - 20))
        pygame.draw.rect(screen, green, pygame.rect.Rect(oppsqr_x*square_w+20 - camPos[0], oppsqr_y*square_h+20 - camPos[1], square_w - 20,square_h - 20))

    for pos in range(len(positionsThatWeWentTo)): #Afficher les cases où l'on est allé
        pygame.draw.rect(screen, (255,0,0), pygame.rect.Rect(positionsThatWeWentTo[pos][0]*square_w+30 - camPos[0],positionsThatWeWentTo[pos][1]*square_h+30 - camPos[1],square_w - 40,square_h - 40))

    for ç in range(boardSize[2]): #Afficher les lettres sur la première ligne
        col = white
        if (ç+(boardSize[2]-1)) % 2 == 0: 
            col = black
        printedText = theFont.render(chr(ord("a")+ç), False, pygame.color.Color(col[0], col[1], col[2]))
        printedTextRect = printedText.get_rect()
        printedTextRect.x = 57 + (ç*square_w) - camPos[0]
        printedTextRect.y = 50 + (7*square_h) - camPos[1]
        screen.blit(printedText, printedTextRect)

    for é in range(boardSize[3]): #Afficher les chiffres sur la première colonne
        col = white
        if é % 2 == 0:
            col = black
        printedText = theFont.render(chr(ord("8")-é), False, pygame.color.Color(col[0], col[1], col[2]))
        printedTextRect = printedText.get_rect()
        printedTextRect.x = 15 + (0*square_w) - camPos[0]
        printedTextRect.y = 15 + (é*square_h) - camPos[1]
        screen.blit(printedText, printedTextRect)
        
    screen.blit(knight, knightrect) #Afficher le cavalier
    
    #Il faudrait que je fasse un cours sur la manière dont les 
    # jeux vidéos dessinnent une image si jamais je dois expliquer ça
    #En gros, ça permet d'afficher l'image qu'on a dessinnée avec les actions au dessus
    pygame.display.flip() 