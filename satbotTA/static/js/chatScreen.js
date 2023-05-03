const chatContainer = document.getElementById('chat-container');
const input = document.querySelector('input[type="text"]');
const sendBtn = document.getElementById('send-btn');

function getCookie(name) {
  // function to retrieve a cookie by its name
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue[2] : null;
}



function sendPostRequest(message){
  const url = window.location.href;

  const data = new FormData();
  data.append('chat', message);

  const csrftoken = getCookie('csrftoken');

  return fetch(url + "?" + JSON.stringify(data), {
    method : 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: data
  })
  .then(response => response.json())
  .then(data => data.response)
  .catch(error => console.error(error));
}

function addUserMessage() {
  const userMessage = input.value.trim();

  var postResponse = ""
  sendPostRequest(userMessage)
    .then(response => {
      postResponse = response
    });


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

  setTimeout(() => {
    addBotMessage(postResponse);
   }, 1000);
}

function addBotMessage(responseMessage) {
  /*
  const botMessages = [
    'Hi there! How can I help you today?',
    'What kind of problem are you having?',
    'I\'m sorry to hear that. Let me see if I can assist you.'
  ];

  const randomIndex = Math.floor(Math.random() * botMessages.length);
  const botMessage = botMessages[randomIndex];
  */
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

sendBtn.addEventListener('click', addUserMessage);
input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    addUserMessage();
  }
});