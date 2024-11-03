import socketio

# Create a Socket.IO client
sio = socketio.Client()

# Connect to the WebSocket server
sio.connect('http://localhost:5000')

# Event handler for connection
@sio.event
def connect():
    print('Connected to the server')

# Event handler for real-time vote updates
@sio.on('vote_update')
def on_vote_update(data):
    print('Received updated election results:')
    for candidate, votes in data.items():
        print(f'{candidate}: {votes} votes')

# Event handler for disconnection
@sio.event
def disconnect():
    print('Disconnected from the server')

# Keep the client running to listen for updates
try:
    sio.wait()
except KeyboardInterrupt:
    print("\nClient stopped.")
