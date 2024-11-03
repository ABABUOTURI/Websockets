from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store voting results in memory
votes = {'Joe Biden': 0, 'Donald Trump': 0, 'Ron DeSantis': 0}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    option = data.get('option')
    if option in votes:
        votes[option] += 1
        socketio.emit('vote_update', votes, to='/')  # Updated to use 'to=/'
        return jsonify({"message": "Vote recorded successfully!", "votes": votes}), 201
    else:
        return jsonify({"error": "Invalid option"}), 400

@socketio.on('connect')
def on_connect():
    print("Client connected!")
    emit('vote_update', votes)

@socketio.on('disconnect')
def on_disconnect():
    print("Client disconnected!")

if __name__ == '__main__':
    socketio.run(app, debug=True)
