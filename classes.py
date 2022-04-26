

class Player(object):
    def __init__(self, user_id):
        self._user = user_id
        self._value = None

    def this_user(self, user_id):
        if self._user == user_id:
            return True
        else:
            return False


class Session(object):
    def __init__(self, identification: int, chat: int):
        self.id = identification
        self.chat_id = chat
        self._started = False
        self._players = []

    def add_players(self, player: Player):
        if len(self._players) <= 1:
            self._players.append(player)
        if len(self._players) >= 2:
            self.start_game()

    def __len__(self):
        return len(self._players)

    def get_players(self):
        return self._players

    def start_game(self):
        self._started = True


def is_correct_number(value):
    try:
        # Check basic exceptions
        if not value.isnumeric() or len(value) != 4 or list(value)[0] == "0":
            return False
    except Exception as e:
        return False
    # Check multiply digits
    used_digits = []
    for digit in list(value):
        if digit in used_digits:
            return False
        else:
            used_digits.append(digit)
    return True
