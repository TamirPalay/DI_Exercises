from menu_manger import MenuManager

def load_manager():
    return MenuManager()

mm = load_manager()

def show_user_menu():
    while True:
        print("\nPlease choose an option:")
        print("a - Add item")
        print("r - Remove item")
        print("v - View menu")
        print("e - Exit")
        input_choice = input("Enter your choice: ").lower()

        if input_choice == 'a':
            add_item_to_menu()
        elif input_choice == 'r':
            remove_item_from_menu()
        elif input_choice == 'v':
            show_restaurant_menu()
        elif input_choice == 'e':
            mm.save_to_file()
            print("Menu saved. Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def add_item_to_menu():
    name = input("Enter the name of the item: ")
    price = float(input("Enter the price of the item: "))
    mm.add_item(name, price)
    print("Item was added successfully.")  # ← exact wording from instructions

def remove_item_from_menu():
    name = input("Enter the name of the item to remove: ")
    if mm.remove_item(name):
        print(f"Item '{name}' removed successfully.")
    else:
        print("Error: item not found in the menu.")  # ← exact wording from instructions

def show_restaurant_menu():
    print("\n--- Restaurant Menu ---")
    items = mm.menu["items"]  # ← access the list under "items" key
    if not items:
        print("No items in the menu.")
        return
    for item in items:
        print(f"{item['name']}: ${item['price']:.2f}")
    print("-----------------------")

show_user_menu()