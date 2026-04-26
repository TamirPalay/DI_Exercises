from game import Game
def get_user_menu_choice():
    print("Welcome to Rock, Paper, Scissors!")
    print("1. Play a new game")
    print("2. Show Scores")
    print("3. Quit\n")
    choice= input("Enter your choice (1, 2, or 3): ")
    if choice in ['1', '2', '3']:
        return choice
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return get_user_menu_choice()
    
def print_results(results):
    print("\nGame Results:")
    print(f"Wins: {results['win']}")
    print(f"Losses: {results['lose']}")
    print(f"Draws: {results['draw']}")
    print("Thank you for playing!\n")

def main():
    results = {"win": 0, "lose": 0, "draw": 0}
    while True:
        choice = get_user_menu_choice()
        if choice == '1':
            game = Game()
            result = game.play()
            results[result] += 1
        elif choice == '2':
            print_results(results)
        elif choice == '3':
            print_results(results)
            break
if __name__ == "__main__":
    main()