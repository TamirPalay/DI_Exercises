import json

class MenuManager():
    def __init__(self):
        with open("restaurant_menu.json", 'r') as file:
            self.menu = json.load(file)  # self.menu = {"items": [...]}

    def add_item(self, name, price):
        # Append a new dict to the items list
        self.menu["items"].append({"name": name, "price": price})

    def remove_item(self, name):
        # Search the items list for a matching name
        for item in self.menu["items"]:
            if item["name"].lower() == name.lower():
                del self.menu["items"][self.menu["items"].index(item)]
                return True
        return False

    def save_to_file(self):
        with open("restaurant_menu.json", 'w') as file:
            json.dump(self.menu, file, indent=4)