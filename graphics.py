import pygame

FPS = 60 #המשחק רץ 60 פעמים בשניה
WIDTH = 1000
HEIGHT = 500

# הצבעים של האבנים
stonecolors = [
    (0, 84, 77),        # טורקיז כהה
    (120, 214, 221),    # טורקיז בהיר
    (167, 199, 231),    # כחול בהיר
    (179, 200, 245),    # כחול פסטל
    (230, 198, 206),    # ורוד פסטל
    (247, 201, 208),    # ורוד בהיר
    (255, 176, 119),    # כתום בהיר
    (255, 153, 181),    # ורוד בהיר
    (255, 199, 217),    # ורוד פסטל
    (255, 214, 153),    # צהוב בהיר
    (255, 205, 135),    # צהוב פסטל
    (191, 219, 210),    # טורקיז פסטל
]

#צבעים
backgroundColor = (197, 217, 228)
pitColor = (205, 170, 125)
borderColor = (60, 40, 30)
textColor = (30, 30, 30)

class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mancala")
        self.font = pygame.font.SysFont("calibri", 28)

        # תמונת הלוח
        self.wood_image = pygame.image.load("/Users/yuvalsaranga/mancala/images/wood6.PNG")
        self.wood_image = pygame.transform.scale(self.wood_image, (880, 320))

        # יצירת הגומות והבתים עם מיקומים מדויקים על המסך
        self.pits = self.create_pits()

    # מאפשר לחשב את הפעולה המתאימה ללחיצה על המסך, כלומר איזה מספר גומה נבחרה על סמך מיקום העכבר
    def __call__(self, state):
        self.draw(state)

    #יוצר בתים וגומות
    def create_pits(self):
        pits = {}

        # בתים
        pits[13] = pygame.Rect(90, 120, 125, 260)   # שחקן 2
        pits[6] = pygame.Rect(800, 120, 125, 260)   # שחקן 1

        # גומות
        top_y = 135 #מיקום הגומות העליונות
        bottom_y = 270 #מיקום הגומות התחתונות
        start_x = 230 #מיקום הגומה הראשונה משמאל, משם מחשבים את שאר הגומות עם רווח קבוע ביניהן
        gap = 90 #הרווח בין הגומות
        pit_width = 80 #רוחב הגומה
        pit_height = 80 #גובה הגומה

        # שורה עליונה (7–12)
        index = 12
        for i in range(6):
            x = start_x + i * gap
            pits[index] = pygame.Rect(x, top_y, pit_width, pit_height)
            index -= 1

        # שורה תחתונה (0–5)
        index = 0
        for i in range(6):
            x = start_x + i * gap
            pits[index] = pygame.Rect(x, bottom_y, pit_width, pit_height)
            index += 1
        
        return pits

    #ליצור הכל על המסך
    def draw(self, state):
        # רקע
        self.screen.fill(backgroundColor)

        # הלוח הראשי
        self.screen.blit(self.wood_image, (60, 90))
        pygame.draw.rect(self.screen, borderColor, (60, 90, 880, 320), 4)

        # ציור מחסנים
        pygame.draw.ellipse(self.screen, pitColor, self.pits[13])
        pygame.draw.ellipse(self.screen, borderColor, self.pits[13], 3)

        pygame.draw.ellipse(self.screen, pitColor, self.pits[6])
        pygame.draw.ellipse(self.screen, borderColor, self.pits[6], 3)

        # ציור גומות
        for i in range(6):
            pygame.draw.ellipse(self.screen, pitColor, self.pits[i])
            pygame.draw.ellipse(self.screen, borderColor, self.pits[i], 3)

        for i in range(7, 13):
            pygame.draw.ellipse(self.screen, pitColor, self.pits[i])
            pygame.draw.ellipse(self.screen, borderColor, self.pits[i], 3)

        # ציור אבנים לפי המצב (state)
        self.drawAllStones(state)

        # כתיבת התור
        if state.winner_message != "":
            self.write(state.winner_message, (300, 30))
        else:
            if state.player == 1:
                self.write("Player 1 turn", (390, 30))
            else:
                self.write("Player 2 turn", (390, 30))

        #pygame.display.update()

    def drawAllStones(self, state):
        # גומות תחתונות 0-5
        for i in range(6):
            self.drawStonesInPit(self.pits[i], state.board[i], stonecolors[i + 6])
        # גומות עליונות 7-12
        for i in range(7, 13):
            self.drawStonesInPit(self.pits[i], state.board[i], stonecolors[12 - i])

        # בתים
        self.drawStonesInStore(self.pits[13], state.board[13], (220, 220, 220))
        self.drawStonesInStore(self.pits[6], state.board[6], (240, 240, 240))
        
    def drawStonesInPit(self, pitRect, stones, color):
        outline_color = (40, 40, 40)

        #רשימה של איפה לצייר כל אבן בתוך הגומה
        positions = [
            (pitRect.x + 22, pitRect.y + 22),
            (pitRect.x + 52, pitRect.y + 22),
            (pitRect.x + 22, pitRect.y + 52),
            (pitRect.x + 52, pitRect.y + 52),
            (pitRect.x + 37, pitRect.y + 37),
            (pitRect.x + 37, pitRect.y + 18),
            (pitRect.x + 18, pitRect.y + 37),
            (pitRect.x + 56, pitRect.y + 37),
        ]

        maxStones = 8 #מספר מקסימלי של אבנים שניתן לצייר בתוך גומה אחת, אם יש יותר מזה מציירים רק 8 אבנים כדי לא להעמיס על הגרפיקה
        if stones < maxStones:
            count = stones
        else:
            count = maxStones
        i = 0
        while i < count:
            pygame.draw.circle(self.screen, color, positions[i], 10) #ציור האבן
            pygame.draw.circle(self.screen, outline_color, positions[i], 10, 2) #ציור קו מתאר לאבן כדי להבליט אותה על המסך
            i += 1

    def drawStonesInStore(self, storeRect, stones, color):
        outline_color = (40, 40, 40)

        # רשימה של איפה לצייר כל אבן בתוך הבית, עם יותר מרווחים כדי לאפשר יותר אבנים בבית
        positions = [
            (storeRect.x + 35, storeRect.y + 35),
            (storeRect.x + 80, storeRect.y + 35),
            (storeRect.x + 35, storeRect.y + 80),
            (storeRect.x + 80, storeRect.y + 80),
            (storeRect.x + 35, storeRect.y + 125),
            (storeRect.x + 80, storeRect.y + 125),
            (storeRect.x + 35, storeRect.y + 170),
            (storeRect.x + 80, storeRect.y + 170),
            (storeRect.x + 35, storeRect.y + 215),
            (storeRect.x + 80, storeRect.y + 215),
        ]

        if stones > 10:
            stones = 10
        for i in range(stones):
            pygame.draw.circle(self.screen, color, positions[i], 10) #ציור האבן
            pygame.draw.circle(self.screen, outline_color, positions[i], 10, 2) #ציור קו מתאר לאבן כדי להבליט אותה על המסך
    
    # פונקציה לכתיבת טקסט על המסך, למשל להודיע על תור השחקן או על המנצח בסוף המשחק
    def write(self, text, pos):
        textSurface = self.font.render(text, True, textColor) #יצירת תמונה של הטקסט
        self.screen.blit(textSurface, pos) #ציור הטקסט על המסך במיקום שנבחר


    def pitChoice(self, pos): 
        # מחזיר את מספר הגומה שעליה לחצו
        for index in range(14):
            if self.pits[index].collidepoint(pos): #פונקציה שבודקת אם נקודת הלחיצה נמצאת בתוך הגומה הנוכחית, שלוחצים מקבלים את מספר הגומה שנבחרה
                return index
        return None
    
    #   פונקציה להצגת הודעת פתיחה עם כללי המשחק והוראות להתחלה
    def openningMessage(self):
        self.screen.fill(backgroundColor)
        self.write("Welcome to Mancala!", (70, 50))
        self.write("Mancala Rules:", (70, 80))
        self.write("- Each player takes stones from one of their pits.", (100, 110))
        self.write("- Move the stones one by one to the next pits.", (100, 140))
        self.write("- Skip your opponent’s store.", (100, 170))
        self.write("- If your last stone lands in your store → play again.", (100, 200))
        self.write("- If your last stone lands in an empty pit on your side → take stones", (100, 230))
        self.write("from the opposite pit.", (120, 260))
        self.write("- The game ends when both sides are empty.", (100, 290))
        self.write("- The player with more stones in the store wins.", (100, 320))
        self.write("Click anywhere to start!", (70, 350))
        self.write("Good luck!", (70, 380))
        pygame.display.update()
    
    #מצייר קובייה
    def drawDice(self, x, y, size, value):
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, size, size), border_radius=10) #ציור הריבוע של הקובייה עם פינות מעוגלות
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, size, size), 2, border_radius=10) #ציור קו מתאר לקובייה כדי להבליט אותה על המסך

        cx = x + size // 2 #חישוב מרכז הקובייה כדי לדעת איפה לצייר את הנקודות של הקובייה בהתאם לערך שלה
        cy = y + size // 2 #חישוב מרכז הקובייה כדי לדעת איפה לצייר את הנקודות של הקובייה בהתאם לערך שלה
        offset = size // 4 #מרחק מהמרכז שבו מציירים את הנקודות של הקובייה, כדי שהנקודות לא יהיו על המרכז אלא מפוזרות בתוך הקובייה בצורה אסתטית

        # רשימה של מיקומים לציור הנקודות של הקובייה בהתאם לערך שלה, עם שימוש במרכז ובאופסט כדי למקם את הנקודות בצורה נכונה בתוך הקובייה
        positions = {
            1: [(cx, cy)],
            2: [(cx - offset, cy - offset), (cx + offset, cy + offset)],
            3: [(cx, cy), (cx - offset, cy - offset), (cx + offset, cy + offset)],
            4: [(cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx - offset, cy + offset), (cx + offset, cy + offset)],
            5: [(cx, cy),
                (cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx - offset, cy + offset), (cx + offset, cy + offset)],
            6: [(cx - offset, cy - offset), (cx + offset, cy - offset),
                (cx - offset, cy), (cx + offset, cy),
                (cx - offset, cy + offset), (cx + offset, cy + offset)]
        }

        # ציור הנקודות של הקובייה בהתאם לערך שלה, עם בדיקה אם הערך הוא בין 1 ל-6 כדי למנוע שגיאות במידה ומתקבל ערך לא חוקי
        for pos in positions[value]:
            pygame.draw.circle(self.screen, (0, 0, 0), pos, size // 10)
    
    #הצגה של מי ניצח בהגרלה
    def chooseStartingPlayer(self, player1Dice, player2Dice, message):
        self.screen.fill(backgroundColor)
        self.write("Roll the dice to see who starts", (280, 50))
        self.write("Player 1", (200, 130))
        self.drawDice(200, 170, 100, player1Dice)
        self.write("Player 2", (630, 130))
        self.drawDice(630, 170, 100, player2Dice)
        self.write(message, (270, 300)) #ההודעה - מי ניצח או תיקו
        # self.write("Click to roll", (400, 360))
        pygame.display.update()

    # ציור כפתור התחלה מחדש בסיום המשחק
    def drawRestartButton(self):
        buttonRect = pygame.Rect(400, 415, 200, 50)
        pygame.draw.rect(self.screen, (200, 200, 200), buttonRect)
        pygame.draw.rect(self.screen, (0, 0, 0), buttonRect, 2)
        self.write("Play Again", (430, 425))
        return buttonRect