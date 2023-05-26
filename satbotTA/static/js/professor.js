// Retrieving HTML elements by their IDs
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

// function to retrieve a cookie by its name
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue[2] : null;
}

// This function adds a new intent 
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
        updateIntents(data.response.intent, data.response.response);
    })
    .then(closeAddButtonWindow())
    .catch(error =>  console.error(error));
}

// This function loads existing intents
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
        updateIntents(intent[1].intent, intent[1].response);
      }
    })
    .catch(error => console.error(error));
}

// This function updates the intents displayed in the UI
function updateIntents(question, answer){
    var intentList = document.getElementById("intent-list");
    var intent = document.createElement("li");

    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";

    var span = document.createElement("span");
    span.innerHTML = "<b>Q</b>: " + question + "<br><b>A</b>: " + answer;

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

// This function loads the public intents into the UI
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

// This function loads the missed questions into the UI
function loadMissedQuestions(){
  const url = window.location.href;
  const data = new FormData();
  data.append('type', 'load-missed-questions');

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
        updateMissedQuestion(intent[1].chat_text);
      }
    })
    .catch(error => console.error(error));
}

// This function updates the public intents displayed in the UI
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

// This function updates the missed questions displayed in the UI
function updateMissedQuestion(question){
  var missedQuestionList = document.getElementById("missed-question-list");
  var missedQuestion = document.createElement("li");

  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";

  var span = document.createElement("span");
  span.textContent = question;

  var button = document.createElement("button");
  button.classList.add("btn", "btn-primary", "btn-xs", "side-button", "edit");
  button.style.fontFamily = "'Product Sans', sans-serif;";
  button.type = "side";
  button.textContent = "Open Chat Preview";

  missedQuestion.appendChild(checkbox);
  missedQuestion.appendChild(span);
  missedQuestion.appendChild(button);


  missedQuestionList.appendChild(missedQuestion);
}

// This function deletes selected intents
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

// This function closes the preview container and removes the blur effect
function closeAddButtonWindow(){
    previewContainer.style.display = "none";
    overlay.style.display = "none";
}

// Adding event listeners to buttons for different actions
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

// Runs functions once page is loaded
document.addEventListener('DOMContentLoaded', function(){
  loadIntents();
  loadPublicIntents();
  loadMissedQuestions();
});