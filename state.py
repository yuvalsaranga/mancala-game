class State:
    def __init__(self, board=None, player=1):
        self.winner_message = "" #הוספת מאפיין להודעת המנצח, כדי להציג אותה על המסך בסוף המשחק
        if board is None:
            self.board = self.init_board() #אם לא סופק לוח, מאתחלים לוח חדש עם 4 אבנים בכל גומה ו-0 אבנים במחסנים
        else:
            self.board = board #אם סופק לוח, משתמשים בו

        self.player = player #הוספת מאפיין לשחקן הנוכחי, כדי לדעת מי התור במשחק ולבדוק חוקיות מהלכים בהתאם

    def init_board(self):
        # 0-5 גומות שחקן 1
        # 6 מחסן שחקן 1
        # 7-12 גומות שחקן 2
        # 13 מחסן שחקן 2
        return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]