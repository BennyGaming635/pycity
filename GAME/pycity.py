class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.connections = {}

    def connect(self, direction, room):
        """Connect this room to another in a specific direction."""
        self.connections[direction] = room

    def get_connection(self, direction):
        """Return the room connected in the given direction, if any."""
        return self.connections.get(direction, None)

    def add_item(self, item):
        """Add an item to this room."""
        self.items.append(item)

    def get_item(self, item_name):
        """Return an item in the room if it exists."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None


class Game:
    def __init__(self):
        # Create house rooms
        self.living_room = Room("Living Room", "A cozy room with a couch and a TV.")
        self.kitchen = Room("Kitchen", "The smell of fresh coffee fills the air.")
        self.garden = Room("Garden", "A beautiful garden with flowers and a small pond.")
        self.bathroom = Room("Bathroom", "A small, clean bathroom.")
        self.basement = Room("Basement", "It's dark and musty. You hear strange noises.")
        self.study = Room("Study", "A quiet room filled with books and a map on the desk.")
        self.attic = Room("Attic", "Dusty and cluttered, with faint light coming through cracks.")
        self.garage = Room("Garage", "A car and some tools are stored here.")
        self.bedroom = Room("Bedroom", "A cozy bedroom with a warm bed and a wardrobe.")
        self.dining_room = Room("Dining Room", "A formal dining room with an elegant table.")

        # Create PyCity rooms
        self.park = Room("Park", "A serene park with a playground and benches.")
        self.library = Room("Library", "A quiet library filled with rows of books.")
        self.shop = Room("Shop", "A small shop selling various items.")
        self.police_station = Room("Police Station", "A bustling station with officers working hard.")

        # Create items
        self.key = Item("Key", "A small, rusty key.")
        self.flashlight = Item("Flashlight", "A flashlight with dim light.")
        self.map = Item("Map", "A map showing the layout of PyCity.")
        self.ticket = Item("Ticket", "A ticket granting access to the park.")
        self.living_room.add_item(self.key)
        self.kitchen.add_item(self.flashlight)
        self.study.add_item(self.map)
        self.shop.add_item(self.ticket)

        # Connect house rooms
        self.living_room.connect("north", self.kitchen)
        self.kitchen.connect("south", self.living_room)
        self.living_room.connect("east", self.garden)
        self.garden.connect("west", self.living_room)
        self.kitchen.connect("west", self.bathroom)
        self.bathroom.connect("east", self.kitchen)
        self.kitchen.connect("down", self.basement)
        self.basement.connect("up", self.kitchen)
        self.living_room.connect("west", self.study)
        self.study.connect("east", self.living_room)
        self.living_room.connect("up", self.attic)
        self.attic.connect("down", self.living_room)
        self.garden.connect("north", self.garage)
        self.garage.connect("south", self.garden)
        self.living_room.connect("south", self.dining_room)
        self.dining_room.connect("north", self.living_room)
        self.dining_room.connect("west", self.bedroom)
        self.bedroom.connect("east", self.dining_room)

        # Connect PyCity rooms
        self.basement.connect("down", self.park)
        self.park.connect("east", self.library)
        self.library.connect("west", self.park)
        self.park.connect("west", self.shop)
        self.shop.connect("east", self.park)
        self.park.connect("north", self.police_station)
        self.police_station.connect("south", self.park)

        # Start the player in the Living Room
        self.current_room = self.living_room
        self.inventory = []
        self.basement_unlocked = False

    def display_help(self):
        """Display a list of available commands."""
        commands = [
            "look around - Describe your surroundings.",
            "go [direction] - Move to a connected room (e.g., 'go north').",
            "take [item] - Pick up an item in the room (e.g., 'take key').",
            "use [item] - Use an item in the correct context (e.g., 'use flashlight').",
            "inventory - Check your current inventory.",
            "about - Show information about the game.",
            "? - Show this help message.",
            "quit - Exit the game."
        ]
        print("\nAvailable Commands:")
        for command in commands:
            print(f"- {command}")

    def display_about(self):
        """Display about page."""
        print("\n=== About PyCity ===")
        print("PyCity: A Text-Based Adventure Game")
        print("Version: 0.1")
        print("Created by: BennyGaming635")
        print("Made for: High Seas Hack Club")
        print("=====================")

    def start(self):
        print("Welcome to PyCity! Type '?' for help or 'quit' to exit the game.\n")
        while True:
            print(f"\nYou are in the {self.current_room.name}.")
            print(self.current_room.description)

            if self.current_room.items:
                print("You see the following items:")
                for item in self.current_room.items:
                    print(f"- {item}")

            command = input("\nWhat would you like to do? ").strip().lower()

            if command == "quit":
                print("Thanks for playing! Goodbye.")
                break
            elif command == "?":
                self.display_help()
            elif command == "about":
                self.display_about()
            elif command == "inventory":
                if self.inventory:
                    print("You are carrying:")
                    for item in self.inventory:
                        print(f"- {item}")
                else:
                    print("Your inventory is empty.")
            elif command == "look around":
                print(f"You see {self.current_room.description}")
            elif command.startswith("go "):
                direction = command[3:]
                next_room = self.current_room.get_connection(direction)
                if next_room:
                    if next_room == self.basement and not self.basement_unlocked:
                        print("It's too dark to enter the basement. You need a flashlight.")
                    else:
                        self.current_room = next_room
                        print(f"You move {direction} to the {self.current_room.name}.")
                else:
                    print("You can't go that way.")
            elif command.startswith("take "):
                item_name = command[5:]
                item = self.current_room.get_item(item_name)
                if item:
                    self.inventory.append(item)
                    self.current_room.items.remove(item)
                    print(f"You take the {item_name}.")
                else:
                    print(f"There is no {item_name} here.")
            elif command.startswith("use "):
                item_name = command[4:]
                if item_name == "flashlight" and self.current_room == self.kitchen:
                    print("You turn on the flashlight. You can now explore the basement.")
                    self.basement_unlocked = True
                elif item_name == "map" and self.current_room == self.study:
                    print("The map shows the layout of PyCity.")
                elif item_name == "ticket" and self.current_room == self.park:
                    print("You use the ticket to enter a special area in the park. It's beautiful!")
                else:
                    print("You can't use that here.")
            else:
                print("I don't understand that command.")


if __name__ == "__main__":
    game = Game()
    game.start()
