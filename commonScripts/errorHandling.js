function handleErrors(responseData) {
    // do something at some point

    if (responseData.status == Status.ERROR) {
        alert('Fatal server error!');
    }
}