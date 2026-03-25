import pygame
from graphics import Graphics, FPS
from state import State
from environment import Environment
from human_agent import HumanAgent
import random

pygame.init() #אתחול pygame
clock = pygame.time.Clock() #אובייקט ששולט בקצב הריצה של המשחק
graphics = Graphics() # אובייקט גרפיקה שאחראי על הצגת המשחק
env = Environment(State()) # אובייקט של הסביבה

#יצירת שני שחקנים
player1 = HumanAgent(1, env, graphics) 
player2 = HumanAgent(2, env, graphics)

#פונקציה שמחליפה בין השחקנים בתור
def switchPlayers(player): 
    if player == player1:
        return player2
    else:
        return player1

#הלולאה של המשחק
def main():
    env.state = State() 
    run = True
    player = None
    game_over = False
    winner_message = ""
    buttonRect = None

    #---מסך פתיחה - הוראות--- 
    graphics.openningMessage() #הצגת הודעת פתיחה עם כללי המשחק והוראות להתחלה
    waiting = True
    while waiting:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # יוצאים ממסך הפתיחה

    #---בחירת שחקן ראשון--- 
    player1Dice = 1
    player2Dice = 1
    message = "click anywhere to roll the dice"
    waiting = True
    rolled = False

    while waiting:
        graphics.chooseStartingPlayer(player1Dice, player2Dice, message) #הצגת הודעה עם תוצאות הגרלת הקוביות לבחירת השחקן הראשון, והוראות להמשך
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN: #אם נלחץ על העכבר, מבצעים את הגרלת הקוביות לבחירת השחקן הראשון
                if rolled == False:
                    player1Dice = random.randint(1, 6) #הגרלה לשחקן 1
                    player2Dice = random.randint(1, 6) #הגרלה לשחקן 2

                    if player1Dice > player2Dice: #מי ניצח בהגרלה - מי שמתחיל
                        player = player1
                        env.state.player = 1 #עדכון השחקן הנוכחי בסביבה כדי שהשחקן הראשון יוכל לבצע את המהלכים שלו
                        message = "Player 1 starts - click to continue"
                        rolled = True
                    elif player2Dice > player1Dice:
                        player = player2
                        env.state.player = 2 #עדכון השחקן הנוכחי בסביבה כדי שהשחקן השני יוכל לבצע את המהלכים שלו
                        message = "Player 2 starts - click to continue"
                        rolled = True
                    else:
                        message = "Tie - click to roll again"

                else:
                    waiting = False

    #---המשחק עצמו--- 
    while run:
        events = pygame.event.get() 
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN: #אם המשחק נגמר ונלחץ על העכבר, בודקים אם נלחץ על כפתור ההתחלה מחדש כדי להתחיל משחק חדש
                pos = pygame.mouse.get_pos() #קבלת מיקום העכבר בעת לחיצה
                if buttonRect is not None and buttonRect.collidepoint(pos): #בדיקה אם הלחיצה הייתה בתוך כפתור ההתחלה מחדש
                    main() #קריאה לפונקציה הראשית כדי להתחיל משחק חדש
                    return

        if not game_over:
            if not env.hasLegalMoves(): #בדיקה אם לשחקן הנוכחי אין מהלכים חוקיים, במקרה כזה עוברים לשחקן השני
                player = switchPlayers(player) #החלפת שחקן
                env.state.player = player.player #עדכון השחקן הנוכחי בסביבה כדי שהשחקן השני יוכל לבצע את המהלכים שלו
            else:
                action = player.__call__(events) #קבלת הפעולה מהשחקן הנוכחי על סמך האירועים שהתקבלו, כלומר לחיצות העכבר

                if action is not None: #אם נבחרה פעולה חוקית, מבצעים את המהלך על הסביבה כדי לעדכן את המצב בהתאם לפעולה שנבחרה
                    env.move(action)

                    if env.isEndOfGame(env.state):
                        game_over = True
                        winner_message = env.getWinnerMessage() #קבלת הודעת המנצח מהסביבה כדי להציג אותה על המסך בסוף המשחק
                        env.state.winner_message = winner_message #עדכון הודעת המנצח במצב כדי שהגרפיקה תוכל להציג אותה על המסך בסוף המשחק
                    else:
                        if env.state.player == 1:
                            player = player1
                        else:
                            player = player2
        graphics(env.state) #עדכון הגרפיקה

        if game_over:
            buttonRect = graphics.drawRestartButton()
        
        pygame.display.update()

        clock.tick(FPS) #שליטה בקצב הריצה של המשחק, כדי שהמשחק לא יתקדם מהר מדי ויאפשר לשחקנים לראות את המהלכים בצורה נוחה

    #---סיום המשחק--- 
    pygame.quit()

if __name__ == '__main__':
    main()