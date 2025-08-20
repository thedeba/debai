const API_URL = "https://thedeba-debai.hf.space/generate";
// Elements
const chatBody = document.getElementById('chat-body');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');
const chatList = document.getElementById('chat-list');
const toggleSidebarBtn = document.getElementById('toggle-sidebar');
const appContainer = document.querySelector('.app-container');

// Chat memory
let conversations = [];
let activeConversation = null;

// Create new conversation
function createConversation() {
  const conv = {id: Date.now(), messages: []};
  conversations.push(conv);
  activeConversation = conv;
  renderChatList();
  renderChat();
}

newChatBtn.addEventListener('click', createConversation);

// Toggle sidebar
toggleSidebarBtn.addEventListener('click', () => {
  appContainer.classList.toggle('sidebar-collapsed');
});

// Render sidebar
function renderChatList() {
  chatList.innerHTML = '';
  conversations.forEach(conv => {
    const div = document.createElement('div');
    div.className = 'chat-item' + (conv === activeConversation ? ' active' : '');

    // Use first user message as title
    let title = 'New Chat';
    const firstUserMsg = conv.messages.find(m => m.role === 'user');
    if (firstUserMsg) title = firstUserMsg.content.slice(0, 25);

    div.textContent = title;
    div.addEventListener('click', () => {
      activeConversation = conv;
      renderChatList();
      renderChat();
    });
    chatList.appendChild(div);
  });
}

// Render chat body
function renderChat() {
  chatBody.innerHTML = '';
  if (!activeConversation) return;
  activeConversation.messages.forEach(msg => {
    const div = document.createElement('div');
    div.className = 'chat-message ' + msg.role;
    div.textContent = msg.content;
    chatBody.appendChild(div);
  });
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Send message
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message || !activeConversation) return;

  // User message
  const userMsg = {role:'user', content: message};
  activeConversation.messages.push(userMsg);
  renderChat();
  userInput.value = '';

  // Typing indicator
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chat-message bot typing-indicator';
  typingDiv.innerHTML = '<span></span><span></span><span></span>';
  chatBody.appendChild(typingDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: message})
    });
    const data = await response.json();
    const botMessage = data.response || "No response";

    activeConversation.messages.push({role:'bot', content: botMessage});
    chatBody.removeChild(typingDiv);
    renderChat();
  } catch (err) {
    console.error(err);
    chatBody.removeChild(typingDiv);
    const errorMsg = {role:'bot', content:'Error: Could not reach API'};
    activeConversation.messages.push(errorMsg);
    renderChat();
  }
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});

// Initialize with one conversation
createConversation();
