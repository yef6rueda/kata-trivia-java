MAX_PLAYERS = 6
BOARD_SIZE = 12
WINNING_COINS = 6
QUESTIONS_PER_CATEGORY = 50


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.coins = 0
        self.in_penalty_box = False

    def move(self, roll):
        self.position = (self.position + roll) % BOARD_SIZE

    def add_coin(self):
        self.coins += 1

    def send_to_penalty_box(self):
        self.in_penalty_box = True


class QuestionDeck:
    def __init__(self):
        self.questions = {
            "Pop": [],
            "Science": [],
            "Sports": [],
            "Rock": [],
        }
        for i in range(QUESTIONS_PER_CATEGORY):
            self.questions["Pop"].append("Pop Question " + str(i))
            self.questions["Science"].append("Science Question " + str(i))
            self.questions["Sports"].append("Sports Question " + str(i))
            self.questions["Rock"].append("Rock Question " + str(i))

    def draw_question(self, category):
        return self.questions[category].pop(0)


class Game:
    def __init__(self):
        self.players = []
        self.deck = QuestionDeck()
        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

    def is_playable(self):
        return self.how_many_players() >= 2

    def add(self, player_name):
        self.players.append(Player(player_name))
        print(player_name + " was added")
        print("They are player number " + str(len(self.players)))
        return True

    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        player = self.players[self.current_player]
        print(player.name + " is the current player")
        print("They have rolled a " + str(roll))

        if player.in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                print(player.name + " is getting out of the penalty box")
                player.move(roll)
                print(player.name + "'s new location is " + str(player.position))
                print("The category is " + self.current_category())
                self.ask_question()
            else:
                print(player.name + " is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False
        else:
            player.move(roll)
            print(player.name + "'s new location is " + str(player.position))
            print("The category is " + self.current_category())
            self.ask_question()

    def ask_question(self):
        print(self.deck.draw_question(self.current_category()))

    def current_category(self):
        player = self.players[self.current_player]
        categories = ["Pop", "Science", "Sports", "Rock"]
        return categories[player.position % len(categories)]

    def was_correctly_answered(self):
        player = self.players[self.current_player]
        if player.in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                player.add_coin()
                print(player.name + " now has " + str(player.coins) + " Gold Coins.")
                game_continues = not self.has_player_won()
                self._advance_player()
                return game_continues
            else:
                self._advance_player()
                return True
        else:
            print("Answer was correct!!!!")
            player.add_coin()
            print(player.name + " now has " + str(player.coins) + " Gold Coins.")
            game_continues = not self.has_player_won()
            self._advance_player()
            return game_continues

    def wrong_answer(self):
        player = self.players[self.current_player]
        print("Question was incorrectly answered")
        print(player.name + " was sent to the penalty box")
        player.send_to_penalty_box()
        self._advance_player()
        return True

    def _advance_player(self):
        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0

    def has_player_won(self):
        player = self.players[self.current_player]
        return player.coins == WINNING_COINS