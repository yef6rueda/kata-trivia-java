class GameOld:
    def __init__(self):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [False] * 6
        
        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []
        
        for i in range(50):
            self.pop_questions.append("Pop Question " + str(i))
            self.science_questions.append("Science Question " + str(i))
            self.sports_questions.append("Sports Question " + str(i))
            self.rock_questions.append("Rock Question " + str(i))
            
        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

    def is_playable(self):
        return len(self.players) >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[len(self.players) - 1] = 0
        self.purses[len(self.players) - 1] = 0
        self.in_penalty_box[len(self.players) - 1] = False
        
        print(player_name + " was added")
        print("They are player number " + str(len(self.players)))
        return True

    def roll(self, roll):
        print(self.players[self.current_player] + " is the current player")
        print("They have rolled a " + str(roll))
        
        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(self.players[self.current_player] + " is getting out of the penalty box")
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12
                
                print(self.players[self.current_player] + "'s new location is " + str(self.places[self.current_player]))
                print("The category is " + self._current_category())
                self._ask_question()
            else:
                print(self.players[self.current_player] + " is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12
                
            print(self.players[self.current_player] + "'s new location is " + str(self.places[self.current_player]))
            print("The category is " + self._current_category())
            self._ask_question()

    def _ask_question(self):
        if self._current_category() == 'Pop':
            print(self.pop_questions.pop(0))
        if self._current_category() == 'Science':
            print(self.science_questions.pop(0))
        if self._current_category() == 'Sports':
            print(self.sports_questions.pop(0))
        if self._current_category() == 'Rock':
            print(self.rock_questions.pop(0))

    def _current_category(self):
        if self.places[self.current_player] == 0 or self.places[self.current_player] == 4 or self.places[self.current_player] == 8:
            return 'Pop'
        if self.places[self.current_player] == 1 or self.places[self.current_player] == 5 or self.places[self.current_player] == 9:
            return 'Science'
        if self.places[self.current_player] == 2 or self.places[self.current_player] == 6 or self.places[self.current_player] == 10:
            return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + " now has " + str(self.purses[self.current_player]) + " Gold Coins.")
                
                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True
        else:
            print("Answer was correct!!!!")
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + " now has " + str(self.purses[self.current_player]) + " Gold Coins.")
            
            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0
            return winner

    def wrong_answer(self):
        print("Question was incorrectly answered")
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True
        
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)