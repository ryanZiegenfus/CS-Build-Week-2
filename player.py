class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
    def travel(self, direction, show_rooms = False):
        next_room = self.current_room.get_room_in_direction(direction)
        if next_room is not None:
            self.current_room = next_room
            if (show_rooms):
                next_room.print_room_description(self)
        else:
            print("****************************************************************************")
            print(f'These are from player.py ------- direction: {direction}')
            print(f'These are from player.py ------- room: {self.current_room.id}')
            print(f'These are from player.py ------- {"You cannot move in that direction."}')
            print("****************************************************************************")