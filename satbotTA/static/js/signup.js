studentButton = document.getElementById("student-button");
professorButton = document.getElementById("professor-button");

function getCookie(name) {
    // function to retrieve a cookie by its name
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue[2] : null;
}

function createStudent(){
    var firstname = document.getElementById("student-firstname").value.trim();
    var lastname = document.getElementById("student-lastname").value.trim();
    var username = document.getElementById("student-username").value.trim();
    var password = document.getElementById("student-password").value.trim();
    var confirmpassword = document.getElementById("student-confirm-password").value.trim();
    var classcode = document.getElementById("student-classcode").value.trim();

    console.log(password);
    console.log(confirmpassword);
    if(password != confirmpassword){
        alert("Passwords must match.");
        return
    }

    const url = window.location.href;
    const data = new FormData();
    data.append('type', 'create-student');
    data.append('firstname', firstname);
    data.append('lastname', lastname);
    data.append('username', username);
    data.append('password', password);
    data.append('classcode', classcode);



    const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken' : csrftoken
        },
        body : data
    })
    .then(response => {
        if(response.redirected){
            window.location.href = response.url
        }
        else{
            return response;
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.response == "username already exists"){
            alert("The given username already exists.");
            return
        }
        else if(data.response == "class code does not exist"){
            alert("The given class code does not exist");
            return
        }
    })
    .catch(error =>  console.error(error));


}


function createProfessor(){
    var firstname = document.getElementById("professor-firstname").value.trim();
    var lastname = document.getElementById("professor-lastname").value.trim();
    var username = document.getElementById("professor-username").value.trim();
    var password = document.getElementById("professor-password").value.trim();
    var confirmpassword = document.getElementById("professor-confirm-password").value.trim();
    var classname = document.getElementById("professor-classname").value.trim();
    var classcode = document.getElementById("professor-classcode").value.trim();

    console.log(password);
    console.log(confirmpassword);
    if(password != confirmpassword){
        alert("Passwords must match.");
        return
    }

    const url = window.location.href;
    const data = new FormData();
    data.append('type', 'create-professor');
    data.append('firstname', firstname);
    data.append('lastname', lastname);
    data.append('username', username);
    data.append('password', password);
    data.append('classname', classname)
    data.append('classcode', classcode);



    const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken' : csrftoken
        },
        body : data
    })
    .then(response => {
        if(response.redirected){
            window.location.href = response.url
        }
        else{
            return response;
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.response == "username already exists"){
            alert("The given username already exists.");
            return
        }
        else if(data.response == "class code already does exist"){
            alert("The given class code already exists");
            return
        }
    })
    .catch(error =>  console.error(error));


}

studentButton.addEventListener('click', createStudent);
professorButton.addEventListener('click', createProfessor);