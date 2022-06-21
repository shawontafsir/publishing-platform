import {login_url} from "./env";

export const login_form_submit = async () => {
    document.getElementById('message').innerHTML = "checking";

    const data = {
        'username' : document.getElementById('username').value,
        'password' : document.getElementById('password').value
    };
    const other_params = {
        headers : { "content-type" : "application/json; charset=UTF-8" },
        body : JSON.stringify(data),
        method : "POST"
    };

    fetch(login_url, other_params).then(
        async function(response) {
            if (response.ok) {
                let data = await response.json();
                alert("Logged in Successfully.");
                localStorage.setItem('token', data['access']);
                location.href = './index.html';
            } else {
                throw new Error("Could not reach the API: " + response.statusText);
            }
        }).then(function(data) {
        document.getElementById("message").innerHTML = JSON.stringify(data);
    }).catch(function(error) {
        document.getElementById("message").innerHTML = error.message;
    });

    return false;
}

// window.addEventListener("load", () => {
//     const login_form_element = document.getElementById('login_form');
//     login_form_element.addEventListener('submit', async (event) => {
//         event.preventDefault();
//         await login_form_submit();
//     });
// });
