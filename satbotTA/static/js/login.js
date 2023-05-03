/* 
function for creating a post request to connect to the server.

*/

const userField = document.querySelector('input[type="text"]');
const passField = document.querySelector('input[type="password"]');
const loginbtn = document.getElementById('login-btn');

function getCookie(name) {
    // function to retrieve a cookie by its name
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue[2] : null;
}

function sendPostRequest() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    const url = window.location.href;
    const data = new FormData();
    data.append('username', username);
    data.append('password', password);

    const csrftoken = getCookie('csrftoken');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: data
        })
        .then(response => {
            if(response.redirected){
                window.location.href = response.url
            }
            else{
                console.log(response);
                return response;
            }
        })
        .then(response => response.json())
        .then(data => data.response)
        .then(response => resolve(response))
        .catch(error => {
            console.error(error);
            reject(error)
        });
    });


} 

function handleLoginAtempt() {

    let postResponse = {}
    sendPostRequest()
        .then(response => {
            postResponse = response;
            if(postResponse === "unauthorized"){
                alert("Username and password combination not found.")
            }
        });


}

loginbtn.addEventListener('click', handleLoginAtempt);
userField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        handleLoginAtempt();
    }
});
passField.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        handleLoginAtempt();
    }
});