import random
class Game():
    def get_user_item(self):
        while True:
            print("Welcome to the new game")
            print("Choose one of the following options: enter r for rock, p for paper, or s for scissors.\n")
            user_input = input("Enter r for rock, p for paper, or s for scissors: ").lower()
            if user_input in ['r', 'p', 's']:
                return user_input
            print("Invalid input. Please try again.")
    def get_computer_item(self):
        return random.choice(['r', 'p', 's'])
    def get_game_result(self,user_item,computer_item):
        if user_item == computer_item:
            return "It's a draw!"
        elif (user_item == 'r' and computer_item == 's') or (user_item == 'p' and computer_item == 'r') or (user_item == 's' and computer_item == 'p'):
            return "You win!"
        else:
            return "You lose!"
    def play(self):
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)
        print(f"You chose: {user_item}, Computer chose: {computer_item}. Result: {result.capitalize()}.\n")
        if result == "You win!":
            return "win"
        elif result == "You lose!":
            return "lose"
        else:           
            return "draw"