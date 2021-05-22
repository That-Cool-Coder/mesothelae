if (localStorage.getItem(sessionIdKey) == null) {
    alert('Not signed in therefore can\'t sign out');

    window.location = urls.frontEnd.home;
}
else {
    var requestData = {
        sessionId : localStorage.getItem(sessionIdKey)
    }
    fetch(urls.api.signOut, {
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
            localStorage.removeItem(sessionIdKey);
        }
        else if (json.status == 'WARNING') {
            alert('Error signing out,\n' + json.statusCode);
        }
        handleErrors(json);

        window.location = urls.frontEnd.home;
    })
}