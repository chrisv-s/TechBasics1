# will work on assignment later

# Player inventory: max 5 items
inventory = []

# Starting room items
items_in_room = [
    {"name": "key", "type": "tool", "uses": 1},
    {"name": "apple", "type": "food", "uses": 1},
    {"name": "torch", "type": "tool", "uses": 3}
]

# Max inventory size
MAX_INVENTORY_SIZE = 5

def show_room_items():
    if items_in_room:
        print("Items in the room:")
        for item in items_in_room:
            print(f"- {item['name']}")
    else:
        print("There are no items in this room.")

def show_inventory():
    if inventory:
        print("Your inventory:")
        for item in inventory:
            print(f"- {item['name']} (uses left: {item.get('uses', '∞')})")
    else:
        print("Your inventory is empty.")

def find_item_by_name(item_name, collection):
    for item in collection:
        if item["name"].lower() == item_name.lower():
            return item
    return None

def pick_up(item_name):
    if len(inventory) >= MAX_INVENTORY_SIZE:
        print("Your inventory is full! Drop something first.")
        return
    item = find_item_by_name(item_name, items_in_room)
    if item:
        inventory.append(item)
        items_in_room.remove(item)
        print(f"You picked up the {item_name}.")
    else:
        print(f"There is no {item_name} here.")

def drop(item_name):
    item = find_item_by_name(item_name, inventory)
    if item:
        inventory.remove(item)
        items_in_room.append(item)
        print(f"You dropped the {item_name}.")
    else:
        print(f"You don't have {item_name} in your inventory.")

def use(item_name):
    item = find_item_by_name(item_name, inventory)
    if not item:
        print(f"You don't have {item_name} to use.")
        return

    # Example: Using the key to escape
    if item["name"].lower() == "key":
        print("You used the key to unlock the door. You escaped! Congratulations!")
        exit()

    # Using apple
    elif item["name"].lower() == "apple":
        print("You eat the apple and feel refreshed.")
        inventory.remove(item)  # Consumed item
    # Using torch
    elif item["name"].lower() == "torch":
        if item["uses"] > 0:
            print("You light the torch. It helps you see better.")
            item["uses"] -= 1
            if item["uses"] == 0:
                print("Your torch burned out.")
                inventory.remove(item)
        else:
            print("Your torch has no uses left.")

    else:
        print(f"You can't use the {item_name} right now.")

def examine(item_name):
    # Look in inventory first, then room
    item = find_item_by_name(item_name, inventory)
    if not item:
        item = find_item_by_name(item_name, items_in_room)

    if item:
        print(f"Examining {item['name']}:")
        if item['type'] == 'tool':
            print("It's a useful tool that might help you.")
        elif item['type'] == 'food':
            print("Something edible, it might restore your energy.")
        else:
            print("An item of interest.")
    else:
        print(f"There is no {item_name} to examine.")

def help_menu():
    print("""
Available commands:
- inventory : Show your inventory
- pickup <item> : Pick up an item
- drop <item> : Drop an item
- use <item> : Use an item
- examine <item> : Examine an item
- help : Show this help menu
- quit : Exit the game
""")

def main():
    print("Welcome to the Escape Room game!")
    print("Find the key and escape. Type 'help' for commands.")
    while True:
        print("\n---")
        show_room_items()
        command = input("What do you want to do? ").strip().lower()

        if command == "inventory":
            show_inventory()
        elif command.startswith("pickup "):
            item_name = command[len("pickup "):]
            pick_up(item_name)
        elif command.startswith("drop "):
            item_name = command[len("drop "):]
            drop(item_name)
        elif command.startswith("use "):
            item_name = command[len("use "):]
            use(item_name)
        elif command.startswith("examine "):
            item_name = command[len("examine "):]
            examine(item_name)
        elif command == "help":
            help_menu()
        elif command == "quit":
            print("Thanks for playing. Goodbye!")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
