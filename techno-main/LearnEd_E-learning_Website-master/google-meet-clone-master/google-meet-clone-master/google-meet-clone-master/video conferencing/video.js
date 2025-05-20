let participants = ['You'];

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value;

    if (message.trim()) {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
        input.value = '';
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
    }
}

function addReaction(reaction) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p><strong>Reaction:</strong> ${reaction}</p>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
}

function toggleCamera() {
    alert("Camera toggled!");
    // Implement camera toggle functionality
}

function toggleMic() {
    alert("Microphone toggled!");
    // Implement microphone toggle functionality
}

// Function to add participants
function addParticipant(name) {
    participants.push(name);
    updateParticipantsList();
}

function updateParticipantsList() {
    const participantsUl = document.getElementById('participants');
    participantsUl.innerHTML = ''; // Clear existing list
    participants.forEach(participant => {
        const li = document.createElement('li');
        li.textContent = participant;
        participantsUl.appendChild(li);
    });
}

// Example of adding a participant
addParticipant('John Doe');
addParticipant('Jane Smith');