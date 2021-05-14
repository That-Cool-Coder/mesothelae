function signIn() {
    // Send a request to the api trying to sign in
    // then save the session id returned from the server
    // planned: and then go to a home page or something

    // First, read the inputs and save the values
    var username = wrk.dom.id('usernameInput').value;
    var password = wrk.dom.id('passwordInput').value;

    const requestData = {
        username : username,
        password : password
    };

    fetch(urls.signIn, {
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
            localStorage.setItem(sessionIdKey, json.sessionId);
            window.location = '/mesothelae/'
        }
        else if (json.status == 'WARNING') {
            alert('Wrong username/password');
        }
        else {
            alert('Error!');
        }
    });
}