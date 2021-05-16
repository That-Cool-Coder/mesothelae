const messageInput = wrk.dom.id('messageInput');
const messageHolder = wrk.dom.id('messageHolder');

const keyWatcher = new wrk.KeyWatcher(document);

messageInput.addEventListener('keypress', e => {
    if (keyWatcher.keyIsDown('Enter') &&
        keyWatcher.keyIsDown('ShiftLeft')) {
        e.preventDefault();
        sendMessage();
    }
})

function sendMessage() {
    // Send a request to the api trying to send a message

    var message = messageInput.value;
    messageInput.value = '';

    const requestData = {
        content : message,
        sessionId : localStorage.getItem(sessionIdKey)
    };

    fetch(urls.sendMessage, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(json => {
        if (json.status == 'WARNING') {
            alert('You must sign in to talk in chat');
            window.location = '/mesothelae/';
        }
    });
}

function getMessages() {
    const requestData = {
        amount : 15,
        sessionId : localStorage.getItem(sessionIdKey)
    };

    fetch(urls.getMessages, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(json => {
        if (json.status == 'OK') {
            displayMessages(json.messages);
        }
        else if (json.status == 'WARNING') {
            alert('You are not signed in');
            window.location = urls.frontEnd.home;
        }
        else {
            alert('Error!');
        }
    })
}

function displayMessages(messages) {
    messageHolder.innerText = '';
    messages.forEach(message => {
        var date = new Date(message.timestamp * 1000);
        messageHolder.innerText += message.senderUsername + '\n';
        messageHolder.innerText += date.toLocaleTimeString() + '\n';
        messageHolder.innerText += message.content + '\n\n';
    })
}

// Make sure person is signed in
if (localStorage.getItem(sessionIdKey) == null) {
    alert('You must sign in to talk in chat');
    window.location = urls.frontEnd.signIn;
}
// Only setup message getter if person is signed in
else {
    var messageInterval = setInterval(getMessages, 1000);
}