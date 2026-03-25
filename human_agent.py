import pygame

class HumanAgent:
    def __init__(self, player, env, graphics):
        self.env = env  #הוספת מאפיין סביבה לסוכן האנושי כדי לאפשר לו לבדוק אם הפעולה חוקית
        self.player = player #הוספת מאפיין שחקן לסוכן האנושי כדי לדעת איזה שחקן הוא מייצג
        self.graphics = graphics #הוספת מאפיין גרפיקה לסוכן האנושי כדי לאפשר לו לחשב את הפעולה על סמך מיקום העכבר

    def get_action(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: #בדיקה אם נלחץ כפתור העכבר
                pos = pygame.mouse.get_pos() #קבלת מיקום העכבר בעת לחיצה
                action = self.graphics.pitChoice(pos) #הוספת חישוב הפעולה על סמך מיקום העכבר

                if action is not None and self.env.isLegal(action): #הוספת בדיקה אם הפעולה חוקית לפני החזרת הפעולה
                    return action

        return None #אם לא נבחרה פעולה חוקית, מחזיר None

    def __call__(self, events):
        return self.get_action(events) 
    # לאפשר לקרוא לסוכן האנושי כמו פונקציה ולקבל את הפעולה שלו על סמך האירועים שהתקבלו