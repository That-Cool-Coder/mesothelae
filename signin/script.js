async function signIn() {
    // Send a request to the api trying to sign in
    // planned: save a session id
    // planned: and then go to a home page or something

    // First, read the inputs and save the values
    var username = wrk.dom.id('usernameInput').value;
    var password = wrk.dom.id('passwordInput').value;

    // If there haven't been any issues, organise data and create request
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
        console.log(json)
    });
}