export const content_form_submit = async (url, method) => {
    const message_element = document.getElementById('message');
    message_element.innerHTML = "checking";

    const data = {
        'title' : document.getElementById('title').value,
        'body' : document.getElementById('body').innerHTML
    };

    const other_params = {
        headers : {
            "content-type": "application/json; charset=UTF-8",
            "Authorization": `JWT ${localStorage.getItem('token')}`
        },
        body : JSON.stringify(data),
        method : method
    };

    fetch(url, other_params).then(
        async function(response) {
            if (response.ok) {
                alert("Submitted Successfully.");
                location.href = '/src/index.html';
            } else {
                throw new Error("Could not reach the API: " + response.statusText);
            }
        }).then(function(data) {
        message_element.innerHTML = JSON.stringify(data);
    }).catch(function(error) {
        message_element.innerHTML = "";
        alert(error.message + "\n Permission denied!");
    });

    return false;
}
