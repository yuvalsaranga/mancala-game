from state import State

class Environment:
    def __init__(self, state):
        self.state = state

    #הפעולה בודקת שהשחקן לא לוקח אבנים ממקום ריק ושהוא לוקח רק מהצד שלו - שהפעולה חוקית בגדול
    def LegalMoves(self):
        for i in range(14):
            if self.state.player == 1 and i < 6 and self.state.board[i] > 0:
                return True
            elif self.state.player == 2 and i > 6 and i < 13 and self.state.board[i] > 0:
                return True
        return False
    
    #הפעולה מבצעת את המהלך על הלוח ומעדכנת את התור בהתאם ובודקת אם יש עוד תור
    def move(self, action):
        #action = מספר הגומה שנבחרה על ידי השחקן
        if not self.isLegal(action):
            return
        
        stones = self.state.board[action] #מספר האבנים בגומה שנבחרה
        self.state.board[action] = 0 #מרוקנים את הגומה שנבחרה
        index = action

        while stones > 0: #כל עוד יש אבנים לחלק
            index = (index + 1) % 14 #מעבירים לגומה הבאה, עם מודולו כדי לחזור להתחלה אם הגענו לסוף הלוח
            # דילוג על הבית של היריב
            if self.state.player == 1 and index == 13: 
                continue 
            if self.state.player == 2 and index == 6:
                continue
            self.state.board[index] += 1 #התקדמנו באחד, אז צריך להוסיף לנוכחי אבן לפני שממשיכים לבאים בתור
            stones -= 1 #מקטינים את מספר האבנים שנותרו לחלק
        self.specialMove(index) #בדיקה אם נפלנו על גומה ריקה בצד שלנו, במקרה כזה לוקחים את האבנים מהגומה הזו ומהגומה שמולה ומכניסים לבית שלנו

        # אם האבן האחרונה לא במחסן שלך - מחליפים תור
        if index != 6 and self.state.player == 1: 
            self.state.player = 2
        elif index != 13 and self.state.player == 2:
            self.state.player = 1

    #פעולה הבודקת אם נשאר לשחקן מהלכים - לא נגמרו לו האבנים
    def hasLegalMoves(self):
        if self.state.player == 1:
            for i in range(6):
                if self.state.board[i] > 0:
                    return True
            return False
        else:
            for i in range(7, 13):
                if self.state.board[i] > 0:
                    return True
            return False

    #הפעולה בודקת אם המשחק נגמר, כלומר אם לשני השחקנים אין מהלכים חוקיים
    def isEndOfGame(self, state):
        side1_empty = True
        for i in range(6):
            if state.board[i] > 0:
                side1_empty = False

        side2_empty = True
        for i in range(7, 13):
            if state.board[i] > 0:
                side2_empty = False

        return side1_empty and side2_empty

    #הפעולה מחזירה הודעה עם המנצח והפרש הניצחון, או הודעה על תיקו אם התוצאה שווה
    def getWinnerMessage(self):
        player1Score = self.state.board[6] #כמות האבנים בבית של שחקן 1
        player2Score = self.state.board[13] #כמות האבנים בבית של שחקן 2

        if player1Score > player2Score:
            return "Player 1 wins by " + str(player1Score - player2Score) + " points! Score: " + str(player1Score) + " - " + str(player2Score)
        elif player2Score > player1Score:
            return "Player 2 wins by " + str(player2Score - player1Score) + " points! Score: " + str(player2Score) + " - " + str(player1Score)
        else:
            return "It's a tie! Play again to break the tie!"

    #  אם האבן האחרונה נחתה בגומה ריקה בצד של השחקן, לוקחים לבית שלו את האבן הזו ואת האבנים שממול
    def specialMove(self, index):
        matchIndex = abs(12 - index) #הגומה המקבילה

        if self.state.player == 1 and index < 6 and self.state.board[index] == 1 and self.state.board[matchIndex] > 0:
            self.state.board[6] += 1 + self.state.board[matchIndex] #הוספת האבן שנחתה בבית של השחקן והאבנים מהגומה המקבילה לבית של השחקן
            self.state.board[index] = 0 #ריקון הגומה שבה נחתה האבן
            self.state.board[matchIndex] = 0 #ריקון הגומה המקבילה כי האבנים שלה נלקחו לבית של השחקן

        elif self.state.player == 2 and index > 6 and index < 13 and self.state.board[index] == 1 and self.state.board[matchIndex] > 0:
            self.state.board[13] += 1 + self.state.board[matchIndex] #הוספת האבן שנחתה בבית של השחקן והאבנים מהגומה המקבילה לבית של השחקן
            self.state.board[index] = 0 #ריקון הגומה שבה נחתה האבן
            self.state.board[matchIndex] = 0 #ריקון הגומה המקבילה כי האבנים שלה נלקחו לבית של השחקן

    #בודקת אם המהלך חוקי
    def isLegal(self, action):
        if action is None:
            return False
        # אסור לבחור בתים או גומה ריקה
        if action == 6 or action == 13 or self.state.board[action] == 0:
            return False
        # בדיקה לפי שחקן
        if self.state.player == 1:
            return action <= 5
        else:
            return action >= 7