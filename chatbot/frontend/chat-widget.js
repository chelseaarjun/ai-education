// Enhanced Chatbot Widget with session history, typing indicator, and disclaimer
(function() {
  const PRIMARY_COLOR = '#2563eb';
  const MODAL_WIDTH = '350px';
  const MODAL_HEIGHT = '500px';
  const SESSION_KEY = 'chatbot_conversation_history';
  const PROFICIENCY_KEY = 'chatbot_proficiency_level';
  
  // Default proficiency level
  let proficiencyLevel = sessionStorage.getItem(PROFICIENCY_KEY) || 'Intermediate';

  // Find the chat button and fix styling immediately
  const btn = document.querySelector('.footer-chat-btn');
  if (btn) {
    // Remove disabled attribute
    btn.removeAttribute('disabled');
    
    // Force override any disabled styling with !important
    btn.style.setProperty('opacity', '1', 'important');
    btn.style.setProperty('cursor', 'pointer', 'important');
    btn.style.setProperty('pointer-events', 'auto', 'important');
    btn.style.setProperty('filter', 'none', 'important');
    btn.style.setProperty('color', 'inherit', 'important');
    btn.style.setProperty('background-color', 'transparent', 'important');
    
    // Add hover effect for better feedback
    btn.addEventListener('mouseenter', () => {
      btn.style.setProperty('opacity', '0.8', 'important');
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.setProperty('opacity', '1', 'important');
    });
    
    // Add click event
    btn.addEventListener('click', openChatModal);
    
    // Debug info
    console.log("Chat button found and enabled!");
  } else {
    console.error("Chat button not found!");
  }

  function getHistory() {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY)) || [];
    } catch {
      return [];
    }
  }
  function setHistory(history) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(history));
  }

  function openChatModal() {
    if (document.getElementById('chatbot-modal')) return;
    const modal = document.createElement('div');
    modal.id = 'chatbot-modal';
    modal.style.position = 'fixed';
    modal.style.bottom = '80px';
    modal.style.right = '40px';
    modal.style.width = MODAL_WIDTH;
    modal.style.height = MODAL_HEIGHT;
    modal.style.background = 'white';
    modal.style.border = `1.5px solid ${PRIMARY_COLOR}`;
    modal.style.borderRadius = '10px';
    modal.style.boxShadow = '0 2px 16px rgba(37,99,235,0.18)';
    modal.style.padding = '0';
    modal.style.zIndex = '9999';
    modal.style.display = 'flex';
    modal.style.flexDirection = 'column';

    modal.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 16px 8px 16px;">
        <span style="font-weight:bold;color:${PRIMARY_COLOR};font-size:1.1em;">AI Course Assistant</span>
        <div>
          <button id="new-chat-btn" style="background:none;border:none;color:${PRIMARY_COLOR};font-size:13px;margin-right:12px;cursor:pointer;padding:3px 8px;border:1px solid ${PRIMARY_COLOR};border-radius:4px;">New Chat</button>
          <button id="close-chatbot-modal" style="background:none;border:none;font-size:20px;cursor:pointer;">&times;</button>
        </div>
      </div>
      <div id="chatbot-messages" style="flex:1;min-height:60px;max-height:340px;overflow-y:auto;font-size:14px;padding:0 16px 0 16px;"></div>
      <div id="chatbot-typing" style="padding:0 16px 8px 16px;display:none;color:${PRIMARY_COLOR};font-size:13px;align-items:center;gap:6px;">
        <span class="spinner" style="display:inline-block;width:16px;height:16px;vertical-align:middle;border:2px solid #e0e7ef;border-top:2px solid ${PRIMARY_COLOR};border-radius:50%;animation:spin 1s linear infinite;"></span>
        <span>Thinking…</span>
      </div>
      <div style="display:flex;align-items:center;padding:8px 16px 8px 16px;border-top:1px solid #f0f0f0;">
        <input id="chatbot-input" type="text" placeholder="How can I help?..." style="flex:1;padding:7px 10px;border:1px solid #ccc;border-radius:4px;font-size:14px;">
        <button id="chatbot-send" style="padding:7px 14px;background:${PRIMARY_COLOR};color:white;border:none;border-radius:4px;margin-left:8px;font-weight:500;">Send</button>
      </div>
      <div style="padding:6px 16px 0px 16px;border-top:1px solid #f0f0f0;">
        <div id="proficiency-selector" style="display:flex;gap:8px;margin-bottom:8px;">
          <button class="proficiency-btn" data-level="Beginner" style="flex:1;padding:5px;border-radius:15px;font-size:13px;cursor:pointer;border:1px solid #e5e7eb;background:#f9fafb;color:#6b7280;transition:all 0.2s;">Beginner</button>
          <button class="proficiency-btn" data-level="Intermediate" style="flex:1;padding:5px;border-radius:15px;font-size:13px;cursor:pointer;border:1px solid #e5e7eb;background:#f9fafb;color:#6b7280;transition:all 0.2s;">Intermediate</button>
          <button class="proficiency-btn" data-level="Expert" style="flex:1;padding:5px;border-radius:15px;font-size:13px;cursor:pointer;border:1px solid #e5e7eb;background:#f9fafb;color:#6b7280;transition:all 0.2s;">Expert</button>
        </div>
      </div>
      <div style="font-size:11px;color:#6b7280;padding:4px 16px 10px 16px;text-align:left;">
        <span>*Powered by Claude 3.5 Haiku (2024 knowledge). Course content last updated June 2025. Answers may be outdated—please verify important info.</span>
      </div>
      <style>
        @keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }
        #chatbot-modal input:focus { outline: 1.5px solid ${PRIMARY_COLOR}; }
        #chatbot-modal::-webkit-scrollbar { width: 8px; background: #f0f0f0; }
        #chatbot-modal::-webkit-scrollbar-thumb { background: #e0e7ef; border-radius: 4px; }
        #chatbot-modal .proficiency-btn.active {
          background-color: ${PRIMARY_COLOR} !important;
          color: white !important;
          border-color: ${PRIMARY_COLOR} !important;
          font-weight: 500 !important;
          box-shadow: 0 2px 4px rgba(37,99,235,0.2) !important;
        }
      </style>
    `;
    document.body.appendChild(modal);
    document.getElementById('close-chatbot-modal').onclick = () => modal.remove();
    document.getElementById('new-chat-btn').onclick = clearHistory;
    document.getElementById('chatbot-send').onclick = sendMessage;
    document.getElementById('chatbot-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') sendMessage();
    });
    
    // Set up proficiency buttons
    const proficiencyBtns = document.querySelectorAll('.proficiency-btn');
    proficiencyBtns.forEach(btn => {
      const level = btn.getAttribute('data-level');
      
      // Make sure to mark active button with !important styles
      if (level === proficiencyLevel) {
        btn.classList.add('active');
        console.log(`Set ${level} as active`); // Debug log
      }
      
      // Add click handlers
      btn.addEventListener('click', () => {
        // Update UI
        proficiencyBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        console.log(`Changed to ${level}`); // Debug log
        
        // Update state
        proficiencyLevel = level;
        sessionStorage.setItem(PROFICIENCY_KEY, level);
        
        // Show feedback
        const messages = document.getElementById('chatbot-messages');
        messages.innerHTML += `<div style="text-align:center;padding:8px;color:#6b7280;font-size:12px;background:#f9fafb;border-radius:4px;margin:8px 0;">Proficiency level set to: ${level}</div>`;
        messages.scrollTop = messages.scrollHeight;
      });
    });
    
    renderHistory();
  }

  function renderHistory() {
    const messages = document.getElementById('chatbot-messages');
    if (!messages) return;
    messages.innerHTML = '';
    const history = getHistory();
    
    // Show initial proficiency level message
    if (history.length === 0) {
      messages.innerHTML = `<div style="text-align:center;padding:8px;color:#6b7280;font-size:12px;background:#f9fafb;border-radius:4px;margin:8px 0;">Proficiency level is set to: ${proficiencyLevel}</div>`;
    }
    
    history.forEach(msg => {
      if (msg.role === 'user') {
        messages.innerHTML += `<div style='margin-bottom:4px;'><b>You:</b> ${escapeHTML(msg.content)}</div>`;
      } else {
        messages.innerHTML += `<div style='margin-bottom:4px;'><b>Bot:</b> ${escapeHTML(msg.content)}</div>`;
      }
    });
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');
    const typing = document.getElementById('chatbot-typing');
    const text = input.value.trim();
    if (!text) return;
    let history = getHistory();
    history.push({ role: 'user', content: text });
    setHistory(history);
    renderHistory();
    input.value = '';
    typing.style.display = 'flex';
    fetch('/chatbot/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: history,
        proficiencyLevel: proficiencyLevel
      })
    })
      .then(r => r.json())
      .then(data => {
        typing.style.display = 'none';
        const reply = data.reply || JSON.stringify(data);
        history = getHistory();
        history.push({ role: 'bot', content: reply });
        setHistory(history);
        renderHistory();
      })
      .catch(err => {
        typing.style.display = 'none';
        messages.innerHTML += `<div style='color:red;'>Error: ${escapeHTML(err.message)}</div>`;
      });
  }

  function clearHistory() {
    // Clear session storage
    sessionStorage.removeItem(SESSION_KEY);
    
    // Clear messages display
    const messages = document.getElementById('chatbot-messages');
    if (messages) {
      messages.innerHTML = '<div style="text-align:center;padding:15px;color:#6b7280;font-size:13px;">Chat history cleared. Ask a new question to start the conversation.</div>';
    }
    
    console.log("Chat history cleared");
  }

  function escapeHTML(str) {
    return str.replace(/[&<>"']/g, function(tag) {
      const charsToReplace = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      };
      return charsToReplace[tag] || tag;
    });
  }
})(); 