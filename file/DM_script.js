function getMessagesFromLocalStorage() {
  const messages = localStorage.getItem('messages');
  return messages ? JSON.parse(messages) : {};
}


function saveMessagesToLocalStorage(messages) {
  localStorage.setItem('messages', JSON.stringify(messages));
}


function getMessagesForUser(userId) {
  const messages = getMessagesFromLocalStorage();
  return messages[userId] || [];
}


function saveMessageForUser(userId, message) {
  const messages = getMessagesFromLocalStorage();
  if (!messages[userId]) {
      messages[userId] = [];
  }
  messages[userId].push(message);
  saveMessagesToLocalStorage(messages);
}

function selectUser(userId) {
  const chatContainer = document.getElementById('chat-container');
  chatContainer.style.display = 'flex';
  chatContainer.dataset.currentUserId = userId;

  const messagesContainer = document.getElementById('messages');
  messagesContainer.innerHTML = ''; // 既存のメッセージをクリア

  // ユーザーごとのDM履歴をロードする
  const messages = getMessagesForUser(userId);
  messages.forEach(message => {
      const messageElement = document.createElement('div');
      messageElement.classList.add('message', message.sender === 'user' ? 'user' : 'other');

      const senderElement = document.createElement('span');
      senderElement.textContent = message.sender === 'user' ? 'あなた' : userId;
      senderElement.classList.add('sender');
      messageElement.appendChild(senderElement);

      const textElement = document.createElement('span');
      textElement.textContent = message.text;
      messageElement.appendChild(textElement);

      messagesContainer.appendChild(messageElement);
  });

  // 自動スクロール
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
  const input = document.getElementById('message-input');
  const message = input.value.trim();
  const userId = document.getElementById('chat-container').dataset.currentUserId;

  if (message !== '' && userId) {
      const messagesContainer = document.getElementById('messages');
      const messageElement = document.createElement('div');
      messageElement.classList.add('message', 'user');

      const senderElement = document.createElement('span');
      senderElement.textContent = 'あなた';
      senderElement.classList.add('sender');
      messageElement.appendChild(senderElement);

      const textElement = document.createElement('span');
      textElement.textContent = message;
      messageElement.appendChild(textElement);

      messagesContainer.appendChild(messageElement);


      saveMessageForUser(userId, { text: message, sender: 'user' });


      input.value = '';


      messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}
