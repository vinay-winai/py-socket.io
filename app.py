from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    rooms, close_room, send
from db import save_event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})
    save_event('my event')


@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)
    save_event('my broadcast event')

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    save_event('connected')

@socketio.on('disconnect')
def test_disconnect():
    save_event('disconnected')

@socketio.on('join')
def on_join(message):
    room = message['room']
    emit('my_response',{'data':f"{rooms()[0]} entered the room"},to=room)
    join_room(room)
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})
    save_event('join')

@socketio.event
def leave(message):
    room = message['room']
    leave_room(room)
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})
    emit('my_response',{'data':f"{rooms()[0]} left the room"},to=room)
    save_event('leave')

@socketio.on('close_room')
def on_close_room(message):
    room = message['room']
    emit('my_response',{'data':f"Room {room} is closing"},to=room)
    close_room(message['room'])
    save_event('close_room')


@socketio.on('my_room_event')
def on_my_room_event(message):
    emit('my_response',
         {'data': message['data']},
         to=message['room'])
    save_event('my_room_event')

if __name__ == '__main__':
    socketio.run(app)

