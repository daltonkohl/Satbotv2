// This block of code retrieves HTML elements by their IDs or classes
const chatContainer = document.getElementById('chat-container');
const input = document.querySelector('input[type="text"]');
const sendBtn = document.getElementById('send-btn');

// Function to retrieve a cookie by its name
function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue[2] : null;
}


// This function sends a POST request with the message data to the server
function sendPostRequest(message) {
  const url = window.location.href;

  const data = new FormData();
  data.append('type', 'chat')
  data.append('chat', message);

  const csrftoken = getCookie('csrftoken');

  return fetch(url + "?" + JSON.stringify(data), {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: data
  })
    .then(response => response.json())
    .then(data => data.response)
    .catch(error => console.error(error));
}

// This function adds a new message from the user to the chat container
function addUserMessage(post, inputMessage) {
  var userMessage = ""
  if (post) {
    userMessage = input.value.trim();
    var postResponse = ""
    sendPostRequest(userMessage)
      .then(response => {
        postResponse = response;
      });
  }
  else {
    userMessage = inputMessage;
  }


  if (!userMessage) return;

  const messageContainer = document.createElement('div');
  messageContainer.classList.add('user-message-container');

  const message = document.createElement('div');
  message.classList.add('message', 'user-message');
  message.textContent = userMessage;

  messageContainer.appendChild(message);
  chatContainer.appendChild(messageContainer);

  input.value = '';
  input.focus();

  if (post) {
    setTimeout(() => {
      addBotMessage(postResponse);
    }, 1000);
  }
}

// This function loads existing chats from the server when the page loads
function LoadChats() {
  const url = window.location.href;

  const data = new FormData();
  data.append('type', 'load-chats');

  const csrftoken = getCookie('csrftoken');

  return fetch(url + "?" + JSON.stringify(data), {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: data
  })
    .then(response => response.json())
    .then(data => {
      for(const chat of Object.entries(data.response)){
        if(chat[1].sender == 'U'){
          addUserMessage(false, chat[1].text);
        }
        else{
          addBotMessage(chat[1].text)
        }
      }
    })
    .catch(error => console.error(error));
}

// This function adds a new message from the bot to the chat container
function addBotMessage(responseMessage) {
  const botMessage = responseMessage

  const messageContainer = document.createElement('div');
  messageContainer.classList.add('message-container');

  const message = document.createElement('div');
  message.classList.add('message', 'bot-message');
  message.textContent = botMessage;

  messageContainer.appendChild(message);
  chatContainer.appendChild(messageContainer);

  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// These lines of code add event listeners to the send button and the input field
sendBtn.addEventListener('click', addUserMessage);
input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    addUserMessage(true, "");
  }
});

// This line of code loads the existing chats when the page loads
document.addEventListener('DOMContentLoaded', function(){
  LoadChats();
});