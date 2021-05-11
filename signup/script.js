async function signUp() {
    // Send a request to the api trying to sign up
    // planned: and then go to a home page or something

    // First, read the inputs and save the values
    var username = wrk.dom.id('usernameInput').value;
    var displayName = wrk.dom.id('displayNameInput').value;
    var password = wrk.dom.id('passwordInput').value;
    var confirmPassword = wrk.dom.id('confirmPasswordInput').value;

    // Make sure all fields have value
    if (username == '' || displayName == '' ||
        password == '' || confirmPassword == '') {

        alert('One of the fields is empty; this isn\'t alowed');
        return;
    }
    
    // Check passwords match
    if (password != confirmPassword) {
        alert('Password doesn\'t match confirm password');
        return;
    }

    // If there haven't been any issues, organise data and create request
    const requestData = {
        username : username,
        displayName : displayName,
        password : password
    };

    fetch(urls.signUp, {
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