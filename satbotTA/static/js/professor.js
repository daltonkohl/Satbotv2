const addNewEntryButton = document.getElementById("add-new-entry");
const addCloseButton = document.getElementById("close-button");
const previewContainer = document.getElementById("preview-container");
const overlay = document.getElementById("overlay");
const addIntentButton = document.getElementById("add-intent-button");
const addNewPublicEntryButton = document.getElementById("add-new-public-entry");
const editButtons = document.querySelectorAll(".edit");
const editContainer = document.getElementById("edit-container");
const editCloseButton = document.getElementById("edit-close-button");
const removeSelectionsButton = document.getElementById("remove-selections");


function getCookie(name) {
    // function to retrieve a cookie by its name
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue[2] : null;
}

function addIntent(){
    var question = document.getElementById('add-question-textbox').value.trim();
    var answer = document.getElementById('add-answer-textbox').value.trim();

    const url = window.location.href;
    const data = new FormData();
    data.append('type', 'add-intent');
    data.append('question', question);
    data.append('answer', answer);
    
    const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken' : csrftoken
        },
        body : data
    })
    .then(response => response.json())
    .then(data => {
        updateIntents(data.response.intent);
    })
    .then(closeAddButtonWindow())
    .catch(error =>  console.error(error));
}

function loadIntents(){
  const url = window.location.href;
  const data = new FormData();
  data.append('type', 'get-intents');

  const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken' : csrftoken
        },
        body : data
    })
    .then(response => response.json())
    .then(data => {
      for(const intent of Object.entries(data.response)){
        updateIntents(intent[1].intent);

      }
    })
    .catch(error => console.error(error));
}

function updateIntents(question){
    var intentList = document.getElementById("intent-list");
    var intent = document.createElement("li");

    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";

    var span = document.createElement("span");
    span.textContent = question;

    var button = document.createElement("button");
    button.classList.add("btn", "btn-primary", "btn-xs", "side-button", "edit");
    button.style.fontFamily = "'Product Sans', sans-serif;";
    button.type = "side";
    button.textContent = "Edit";

    intent.appendChild(checkbox);
    intent.appendChild(span);
    intent.appendChild(button);


    intentList.appendChild(intent);
}


function loadPublicIntents(){
  const url = window.location.href;
  const data = new FormData();
  data.append('type', 'get-public-intents');

  const csrftoken = getCookie('csrftoken');

    fetch(url, {
        method : 'POST',
        headers : {
            'X-CSRFToken' : csrftoken
        },
        body : data
    })
    .then(response => response.json())
    .then(data => {
      for(const intent of Object.entries(data.response)){
        updatePublicIntent(intent[1].intent);
      }
    })
    .catch(error => console.error(error));
}

function updatePublicIntent(question){
  var intentList = document.getElementById("public-intent-list");
  var intent = document.createElement("li");

  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";

  var span = document.createElement("span");
  span.textContent = question;

  var button = document.createElement("button");
  button.classList.add("btn", "btn-primary", "btn-xs", "side-button", "edit");
  button.style.fontFamily = "'Product Sans', sans-serif;";
  button.type = "side";
  button.textContent = "Edit";

  intent.appendChild(checkbox);
  intent.appendChild(span);
  intent.appendChild(button);


  intentList.appendChild(intent);
}

function deleteSelectedIntents(){
  const myList = document.getElementById('intent-list');
  const checkedItems = myList.querySelectorAll('li input[type="checkbox"]:checked');
  if(checkedItems.length == 0){
    return;
  }
  const url = window.location.href;
  const data = new FormData();
  data.append('type', 'delete-intent')


  for(var i = 0; i < checkedItems.length; i++){
    data.append(i, checkedItems[i].parentNode.querySelector("span").textContent);
  }


  const csrftoken = getCookie('csrftoken');

  fetch(url, {
      method : 'POST',
      headers : {
          'X-CSRFToken' : csrftoken
      },
      body : data
  })
  .then(response => response.json())
  .then(data => {
    for(var i = 0; i < checkedItems.length; i++){
     checkedItems[i].parentNode.parentNode.removeChild(checkedItems[i].parentNode);
    }
  })
  .catch(error => console.error(error));


}


function closeAddButtonWindow(){
    previewContainer.style.display = "none";
    overlay.style.display = "none";
}



addNewEntryButton.addEventListener("click", () => {
  previewContainer.style.display = "block";
  overlay.style.display = "block";
});

addCloseButton.addEventListener("click", closeAddButtonWindow);

addNewPublicEntryButton.addEventListener("click", () => {
  previewContainer.style.display = "block";
  overlay.style.display = "block";
});

editButtons.forEach((editButton) => {
  editButton.addEventListener("click", () => {
    editContainer.style.display = "block";
    overlay.style.display = "block";
  });
});

editCloseButton.addEventListener("click", () => {
  editContainer.style.display = "none";
  overlay.style.display = "none";
});

addIntentButton.addEventListener("click", addIntent);

removeSelectionsButton.addEventListener("click", deleteSelectedIntents);

document.addEventListener('DOMContentLoaded', function(){
  loadIntents();
  loadPublicIntents();
});