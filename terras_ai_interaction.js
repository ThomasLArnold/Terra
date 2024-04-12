function startSpeaking() {
    var responseText = document.getElementById("response-text");
    responseText.value = "Hello, I'm Terra, your personal assistant. How can I assist you today?";
    // Start listening to user input
    listenCommand();
}

function sendCommand(command) {
    // Display the command in the response box
    var responseText = document.getElementById("response-text");
    responseText.value = "User Command: " + command;

    // Send the command to the backend for processing
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: command })
    })
    .then(response => response.json())
    .then(data => {
        // Display the response from the backend in the response box
        responseText.value += "\n\nTerra's Response:\n" + data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function listenCommand() {
    // Code for listening to user's voice input (
    // create a new instance of SpeechRecognition
    const recognition = new webkitSpeechRecognition();

    // set recognition parameters
    recognition.continuous = false;
    recognition.lang = 'en-US';

    // start recognition
    recognition.start();

    // handle recognition result
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;

        // Display the user's voice input in the text box
        document.getElementById("command-input").value = transcript;

        // Send the user's voice input to the backend for processing
        sendCommand(transcript);
    };

    // handle recognition error
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
}

function startListening() {
    var responseText = document.getElementById("response-text");
    responseText.value = "Listening...";

    // Code for listening to user input
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;

        // Display the user's voice input in the text box
        document.getElementById("command-input").value = transcript;

        // Send the user's voice input to the backend for processing
        sendCommand(transcript);
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
}

function toggleCamera() {
    // Code to toggle camera and microphone usage
    const videoContainer = document.getElementById("video-container");
    const cameraFeed = document.getElementById("camera-feed");

    // Check if camera is currently active
    if (videoContainer.style.display === "none") {
        // Activate camera and microphone
        videoContainer.style.display = "block";
        cameraFeed.style.display = "block";
        startListening(); // Start listening for user input
    } else {
        // Deactivate camera and microphone
        videoContainer.style.display = "none";
        cameraFeed.style.display = "none";
    }
}
