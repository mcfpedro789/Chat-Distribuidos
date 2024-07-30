const username = sessionStorage.getItem('username');
if (!username) {
    window.location.href = 'login.html';
}

const roomContainer = document.getElementById('room-container');
const createRoomButton = document.getElementById('create-room-button');
const roomListElement = document.getElementById('room-list');
const messageContainer = document.getElementById('message-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const emojiButton = document.getElementById('emoji-button');
let currentRoom = '';

// Emoji picker initialization
document.addEventListener('DOMContentLoaded', () => {
    const picker = new EmojiButton();

    emojiButton.addEventListener('click', () => {
        picker.togglePicker(emojiButton);
    });

    picker.on('emoji', emoji => {
        messageInput.value += emoji;
    });
});

createRoomButton.addEventListener('click', () => {
    const roomName = prompt('Enter room name:');
    const roomPassword = prompt('Enter room password:');
    fetch('http://localhost:8080/create_room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ room_name: roomName, room_password: roomPassword }),
    })
    .then(response => {
        if (response.ok) {
            loadRooms();
        } else {
            alert('Failed to create room');
        }
    })
    .catch(error => {
        console.error('Error creating room:', error);
    });
});

function loadRooms() {
    fetch('http://localhost:8080/rooms')
    .then(response => response.json())
    .then(rooms => {
        roomListElement.innerHTML = '';
        rooms.forEach(room => {
            const roomElement = document.createElement('div');
            roomElement.textContent = room;
            roomElement.addEventListener('click', () => {
                const roomPassword = prompt('Enter room password:');
                fetch('http://localhost:8080/join_room', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ room_name: room, room_password: roomPassword }),
                })
                .then(response => {
                    if (response.ok) {
                        currentRoom = room;
                        messageContainer.style.display = 'block';
                        roomContainer.style.display = 'none';
                        fetchMessages();
                    } else {
                        alert('Failed to join room');
                    }
                })
                .catch(error => {
                    console.error('Error joining room:', error);
                });
            });
            roomListElement.appendChild(roomElement);
        });
    })
    .catch(error => {
        console.error('Error loading rooms:', error);
    });
}

sendButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (message && currentRoom) {
        sendMessage(message);
        messageInput.value = '';
    }
});

function sendMessage(message) {
    fetch('http://localhost:8080/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: username, room_name: currentRoom, message }),
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}

function fetchMessages() {
    if (currentRoom) {
        fetch(`http://localhost:8080/messages?room_name=${currentRoom}`)
        .then(response => response.json())
        .then(messages => {
            const messagesElement = document.getElementById('messages');
            messagesElement.innerHTML = '';
            messages.forEach(msg => {
                const messageElement = document.createElement('div');
                messageElement.textContent = msg;
                messagesElement.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
    }
}

loadRooms();
setInterval(fetchMessages, 1000);
