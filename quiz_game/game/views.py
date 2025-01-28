import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse

# In-memory storage for demo purposes (use database for production)
rooms = {}

def index(request):
    """
    Renders the homepage where users input their name and join or create a room.
    """
    return render(request, 'game/index.html')
def room(request, room_code):
    """
    Renders the room page with the given room code.
    """
    return render(request, 'game/room.html', {'room_code': room_code})

def create_room(request):
    """
    API endpoint to create a new room and return its code.
    """
    if request.method == 'POST':
        # Parse the player's name from the request (assumes JSON payload)
        import json
        data = json.loads(request.body)
        player_name = data.get('name')

        if not player_name:
            return JsonResponse({'error': 'Player name is required'}, status=400)

        # Generate a unique room code
        room_code = generate_unique_room_code()
        while room_code in rooms:
            room_code = generate_unique_room_code()

        # Initialize room data with the player as the leader
        rooms[room_code] = {
            'players': [{
                'name': player_name,
                'is_leader': True,
                'is_ready': False,
                'score': 0
            }],
            'game_started': False
        }

        return JsonResponse({'room_code': room_code})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

def join_room(request, room_code):
    """
    Checks if the room exists and allows the user to join it.
    """
    room_code = room_code.upper()
    if room_code in rooms:
        return JsonResponse({'success': True, 'room_code': room_code})
    else:
        return JsonResponse({'success': False, 'error': 'Room not found'}, status=404)

def generate_unique_room_code():
    """
    Generates a unique room code.
    """
    from django.utils.crypto import get_random_string
    room_code = get_random_string(6).upper()
    while room_code in rooms:
        room_code = get_random_string(6).upper()
    return room_code
