# Robert Farino
# IT 140 Intro to Scripting


def main():

    # A dictionary for the murder mystery text game.
    # The dictionary links a room to other rooms, contains
    # room items, values indicating if the rooms are dark,
    # and text prefixes to assist with prints to the screen.
    rooms = {
        'Hotel Corridor': {'south': 'Kitchen', 'north': 'Guest Room 100', 'east': 'Front Desk', 'west': 'Broken Elevator',
                           'isDark': 'False', 'roomPrintPrefix': 'in the'},

        'Kitchen': {'north': 'Hotel Corridor', 'east': 'Dining Hall',
                    'isDark': 'True', 'roomPrintPrefix': 'in the',
                    'item': 'Buffalo chicken pizza', 'itemPrintPrefix': 'a'},

        'Dining Hall': {'west': 'Kitchen',
                        'isDark': 'True', 'roomPrintPrefix': 'in the',
                        'Villain': 'True' },

        'Guest Room 100': {'east': 'Storage Closet', 'south': 'Hotel Corridor',
                           'isDark': 'True', 'roomPrintPrefix': 'in',
                           'item': 'Taser', 'itemPrintPrefix': 'a' },

        'Storage Closet': {'west': 'Guest Room 100',
                           'isDark': 'True', 'roomPrintPrefix': 'in the',
                           'item': 'Spray bleach', 'itemPrintPrefix': 'some'},

        'Broken Elevator': {'east': 'Hotel Corridor',
                            'isDark': 'True', 'roomPrintPrefix': 'in the',
                            'item': 'Journal', 'itemPrintPrefix': 'a'},

        'Front Desk': {'north': 'Activity Center', 'west': 'Hotel Corridor',
                       'isDark': 'False', 'roomPrintPrefix': 'at the',
                       'item': 'Flashlight', 'itemPrintPrefix': 'a', },

        'Activity Center': {'south': 'Front Desk',
                            'isDark': 'True', 'roomPrintPrefix': 'in the',
                            'item': 'Skate pads', 'itemPrintPrefix': 'some'}
    }

    # Print game title, instructions, and valid moves.
    display_game_title_and_instructions()

    # Set up inventory
    inventory = []

    # Set starting location.
    currentRoom = 'Hotel Corridor'

    # Initiate the gameplay loop. The game will continue until the player collects all items and corners
    # the murderer or enters the room without all items and the murderer is able to escape.
    while currentRoom != 'Exit':

        # Display the current room, room item (if available), and inventory.
        display_status(rooms, currentRoom, inventory)

        # Ask the player to enter a move.
        currentMove = str(input('Enter your move: ')).lower()


        # Determine if the player is moving North, South, East, or West.
        if (currentMove == 'go north' or currentMove == 'go south'
                or currentMove == 'go east' or currentMove == 'go west'):

            # Process the "go <direction>" command which may result in the
            # player moving into another room.
            currentRoom = move_between_rooms(currentMove, rooms, currentRoom, inventory)

        # Determine if the player is trying to get an item in the current room.
        elif currentMove.startswith('get '):

            # Process the "get <item>" command which may result in an
            # item being picked up in the current room.
            get_item(currentMove, rooms, currentRoom, inventory)

        # Print an error message if the move is invalid.
        else:
            print('Please enter a valid command!')

        # Check if the villain is in the current room.
        # If so, encounter the villain and end the game.
        if 'Villain' in rooms[currentRoom]:
            encounter_villain(rooms)
            currentRoom = 'Exit'

    # Print a message confirming the game has concluded.
    print('Thanks for playing the game! Hope you enjoyed it.')



def display_game_title_and_instructions():
    # Print game title, instructions, and valid moves.
    print('Murder Mystery Text Adventure Game')
    print('Collect six items to win the game, or the murderer will escape out the back door!')
    print('Move commands: go South, go North, go East, go West')
    print("Add to Inventory: get 'item name'")


def display_current_room(rooms, currentRoom):
    # Print current room. Include the appropriate room name prefix.
    print('You are currently', rooms[currentRoom]['roomPrintPrefix'], currentRoom)


def display_inventory(inventory):
    # Print the contents of the player's inventory.
    print('Inventory:', inventory)


def display_room_item(rooms, currentRoom):
    # Print item in current room if the room has an available item.
    # Include the appropriate item name prefix.
    if 'item' in rooms[currentRoom]:
        print('You see', rooms[currentRoom]['itemPrintPrefix'], rooms[currentRoom]['item'])


def display_status(rooms, currentRoom, inventory):
    # Display the current room, room item (if available), and inventory.
    print('******************************************')
    display_current_room(rooms, currentRoom)
    display_inventory(inventory)
    display_room_item(rooms, currentRoom)


def move_between_rooms(currentMove, rooms, currentRoom, inventory):
    # Processes a "go <direction>" command which will cause the player
    # to enter another room if the move is valid. If the next room is dark,
    # the player must contain the flashlight in their inventory in order
    # for the game to allow them to enter the room. currentMove contains
    # the "go <direction>" command entered by the user.

    # Extract the move direction from currentMove by obtaining the substring from
    # the fourth character (index 3) to the end, e.g., "North", and assign the result
    # to the moveDirection variable.
    searchDirection = currentMove[3:].lower()

    # Use an if statement to determine if the moveDirection value has a key-value pair in the rooms
    # dictionary for the current room.
    if searchDirection in rooms[currentRoom]:

        # Use dictionary to set nextRoom based on the direction chosen.
        nextRoom = rooms[currentRoom][searchDirection]

        # Print an error message saying that the room is too dark to enter
        # if the room is dark and the player does not have the flashlight.
        if rooms[nextRoom]['isDark'] == 'True' and ('Flashlight' in inventory) == False:
            print('The room is too dark to enter!')

        # Else, the user can enter the room. Set currentRoom to nextRoom.
        else:
            currentRoom = nextRoom

    # Else, the move direction is not valid. Display a message indicating they can't go that way.
    else:
        print('You can\'t go that way!')

    # Return the value or currentRoom, which will have been modified
    # if the player was able to move into the next room.
    return currentRoom


def get_item(currentMove, rooms, currentRoom, inventory):
    # Processes a "get <item>" command, which will cause an item to be
    # picked up in the current room if it is available. currentMove
    # contains the "get <item>" command entered by the user.

    # Extract the name of the item to get by obtaining the substring from
    # the fourth character (index 3) to the end, and assign the result
    # to the inventoryItem variable.
    itemToPickUp = currentMove[4:]

    # If the item exists in the room
    if 'item' in rooms[currentRoom] and rooms[currentRoom]['item'].lower() == itemToPickUp.lower():

        # Get item to pick up name with correct capitalization
        itemToPickUp = rooms[currentRoom]['item']

        # Add item to inventory.
        inventory.append(itemToPickUp)

        # Remove item from rooms dictionary
        del rooms[currentRoom]['item']

        # Print a message indicating that the item was picked up.
        print('You picked up the', itemToPickUp)

    # Else, the entered item name was already picked up or
    # never existed in this room. Print an error message.
    else:
        print('The room does not contain this item!')


def encounter_villain(rooms):
    # Prints the villain encounter text to the user and the
    # outcome of the game. The player will win the game if
    # they have collected all items before encountering
    # the villain.

    # Print a message indicating that the player found the villain.
    print()
    print('You see the murderer.')

    # Determine if the player has found all the items
    # by seeing if there is still an 'item' entry in
    # one of the rooms.
    allItemsClaimed = True
    for roomName in rooms:
        if 'item' in rooms[roomName]:
            allItemsClaimed = False

    # Print a message telling the player if they won or
    # lost the game, depending on if all items were collected
    # before finding the villain.

    if allItemsClaimed == True:
        print('You catch him by surprise and subdue him.')
        print('Congratulations! You defeated the murderer!')
    else:
        print('A struggle ensues. The murderer knocks you down and escapes through the back door. GAME OVER!')


if __name__ == "__main__":
    # Call main() function.
    main()
