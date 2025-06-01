// Enhanced Chatbot Widget with session history, typing indicator, and disclaimer
(function() {
  // Check if GoatCounter is already initialized
  if (typeof window.goatcounter === 'undefined') {
    // Function to initialize GoatCounter
    const initGoatCounter = function() {
      // Only initialize if not already loaded
      if (typeof window.goatcounter === 'undefined') {
        // Check if on localhost
        const isLocalhost = window.location.hostname === 'localhost' || 
                           window.location.hostname === '127.0.0.1';
        
        // Skip actual tracking on localhost, just log to console
        if (isLocalhost) {
          // Create mock goatcounter for development
          window.goatcounter = {
            count: function(params) {
              console.log('GoatCounter (DEV MODE):', params);
            }
          };
          console.log('GoatCounter initialized in development mode');
          return;
        }
        
        // Add GoatCounter script
        const script = document.createElement('script');
        script.async = true;
        script.dataset.goatcounter = 'https://ai-foundation-course.goatcounter.com/count'; // Replace with your actual GoatCounter URL
        script.src = '//gc.zgo.at/count.js';
        
        // Append script to document
        document.head.appendChild(script);
        console.log('GoatCounter script added to page');
      }
    };
    
    // Initialize GoatCounter
    initGoatCounter();
  }

  const PRIMARY_COLOR = '#2563eb';
  const MODAL_WIDTH = '350px';
  const MODAL_HEIGHT = '500px';
  const SESSION_KEY = 'chatbot_conversation_history';
  const PROFICIENCY_KEY = 'chatbot_proficiency_level';
  const SUMMARY_KEY = 'chatbot_conversation_summary';
  const SESSION_START_KEY = 'chatbot_session_start_time';
  
  // API URL configuration - select based on environment
  const API_CONFIG = {
    local: 'http://localhost:3000/api/chat/',
    production: 'https://ai-education-ryuu.onrender.com/api/chat/'
  };
  
  // Analytics tracking functions
  const Analytics = {
    // Initialize session data
    initSession: function() {
      if (!sessionStorage.getItem(SESSION_START_KEY)) {
        sessionStorage.setItem(SESSION_START_KEY, Date.now().toString());
        this.trackEvent('chatbot_session_start');
      }
    },
    
    // Track a user question
    trackQuestion: function(question) {
      this.trackEvent('chatbot_question', {
        // Optional: truncate long questions to avoid URL length issues
        question: question.substring(0, 100) + (question.length > 100 ? '...' : '')
      });
    },
    
    // Track session end with duration
    trackSessionEnd: function() {
      const startTime = parseInt(sessionStorage.getItem(SESSION_START_KEY) || Date.now());
      const duration = Math.floor((Date.now() - startTime) / 1000); // duration in seconds
      
      // Get number of questions in this session
      const history = JSON.parse(sessionStorage.getItem(SESSION_KEY) || '[]');
      const questionCount = history.filter(item => item.role === 'user').length;
      
      this.trackEvent('chatbot_session_end', {
        duration_seconds: duration,
        questions_count: questionCount
      });
    },
    
    // Generic event tracking function using GoatCounter
    trackEvent: function(eventName, params = {}) {
      if (typeof window.goatcounter !== 'undefined') {
        // Convert params to URL query parameters
        const paramString = Object.entries(params)
          .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
          .join('&');
          
        // Track event in GoatCounter
        window.goatcounter.count({
          path: `${eventName}${paramString ? '?' + paramString : ''}`,
          event: true
        });
        
        console.log(`Tracked event: ${eventName}`, params);
      } else {
        console.log('GoatCounter not available, event not tracked:', eventName, params);
      }
    }
  };
  
  // Default proficiency level
  let proficiencyLevel = sessionStorage.getItem(PROFICIENCY_KEY) || 'Intermediate';
  
  // Track conversation summary
  let conversationSummary = sessionStorage.getItem(SUMMARY_KEY) || '';

  // Debug info about what we're looking for
  console.log("Chat widget initializing - looking for chat buttons");
  
  // Try to find any chat button - let's try multiple selectors
  let btn = document.querySelector('.footer-chat-btn');
  if (!btn) {
    console.log("No .footer-chat-btn found, trying .floating-chat-btn");
    btn = document.querySelector('.floating-chat-btn');
  }
  
  // Log which button was found
  if (btn) {
    console.log("Chat button found with class: " + btn.className);
    
    // Remove disabled attribute
    btn.removeAttribute('disabled');
    
    // Apply new styles that match test-chatbot.html
    btn.style.setProperty('background-color', '#2563eb', 'important');
    btn.style.setProperty('color', 'white', 'important');
    btn.style.setProperty('border', 'none', 'important');
    btn.style.setProperty('padding', '10px 20px', 'important');
    btn.style.setProperty('border-radius', '50px', 'important');
    btn.style.setProperty('cursor', 'pointer', 'important');
    btn.style.setProperty('position', 'fixed', 'important');
    btn.style.setProperty('bottom', '20px', 'important');
    btn.style.setProperty('right', '20px', 'important');
    btn.style.setProperty('box-shadow', '0 4px 12px rgba(37, 99, 235, 0.2)', 'important');
    btn.style.setProperty('display', 'flex', 'important');
    btn.style.setProperty('align-items', 'center', 'important');
    btn.style.setProperty('gap', '8px', 'important');
    btn.style.setProperty('font-weight', '500', 'important');
    btn.style.setProperty('transition', 'all 0.2s ease', 'important');
    btn.style.setProperty('opacity', '1', 'important');
    btn.style.setProperty('pointer-events', 'auto', 'important');
    btn.style.setProperty('filter', 'none', 'important');
    btn.style.setProperty('z-index', '1000', 'important');
    
    // Debug click handler
    const originalClickHandler = btn.onclick;
    if (originalClickHandler) {
      console.log("Button already had a click handler - replacing it");
    }
    
    // Update content with SVG icon - check if it has .btn-label or .footer-label
    const labelClass = btn.querySelector('.btn-label') ? 'btn-label' : 'footer-label';
    btn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <span class="${labelClass}">Ask AI Assistant</span>
    `;
    
    // Add hover effect for better feedback
    btn.addEventListener('mouseenter', () => {
      btn.style.setProperty('background-color', '#1d4ed8', 'important');
      btn.style.setProperty('transform', 'translateY(-2px)', 'important');
      btn.style.setProperty('box-shadow', '0 6px 16px rgba(37, 99, 235, 0.3)', 'important');
    });
    
    btn.addEventListener('mouseleave', () => {
      btn.style.setProperty('background-color', '#2563eb', 'important');
      btn.style.setProperty('transform', 'translateY(0)', 'important');
      btn.style.setProperty('box-shadow', '0 4px 12px rgba(37, 99, 235, 0.2)', 'important');
    });
    
    // Add click event that toggles the chat modal
    btn.onclick = function(e) {
      console.log("Chat button clicked");
      toggleChatModal();
    };
    
    // Debug info
    console.log("Chat button found and enabled!");
    
    // Log the button HTML
    console.log("Button HTML: " + btn.outerHTML);
  } else {
    console.error("Chat button not found! Looking for .footer-chat-btn or .floating-chat-btn");
    console.log("Available buttons on page:");
    document.querySelectorAll('button').forEach(b => {
      console.log("- Button with class: " + b.className);
    });
  }

  // Toggle function to open or close the chat modal
  function toggleChatModal() {
    const existingModal = document.getElementById('chatbot-modal');
    
    if (existingModal) {
      // If modal exists, close it
      console.log("Closing existing chat modal");
      Analytics.trackSessionEnd(); // Track session end when closing
      existingModal.remove();
    } else {
      // If no modal exists, open a new one
      console.log("Opening new chat modal");
      openChatModal();
      Analytics.initSession(); // Initialize session when opening
    }
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
        <button id="chatbot-send" style="padding:6px;min-width:36px;height:36px;background:${PRIMARY_COLOR};color:white;border:none;border-radius:4px;margin-left:8px;display:flex;align-items:center;justify-content:center;">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="transform: rotate(45deg);">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
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
        
        /* Message styling */
        .chatbot-user-msg {
          background-color: #e2f2ff;
          padding: 10px 12px;
          border-radius: 12px 12px 0 12px;
          margin: 8px 0 8px auto;
          max-width: 85%;
          align-self: flex-end;
          text-align: right;
        }
        
        .chatbot-bot-msg {
          background-color: #f0f2f5;
          padding: 10px 12px;
          border-radius: 12px 12px 12px 0;
          margin: 8px auto 8px 0;
          max-width: 85%;
          align-self: flex-start;
        }
        
        .chatbot-citation {
          font-size: 12px;
          color: #666;
          margin-top: 6px;
          font-style: italic;
          text-align: left;
        }
        
        .chatbot-suggestions {
          display: flex;
          flex-wrap: wrap;
          gap: 6px;
          margin: 8px 0;
        }
        
        .chatbot-suggestion-btn {
          background-color: #f0f2f5;
          color: ${PRIMARY_COLOR};
          font-size: 12px;
          padding: 6px 10px;
          border-radius: 12px;
          border: 1px solid #e5e7eb;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .chatbot-suggestion-btn:hover {
          background-color: #e2f2ff;
        }
        
        /* Responsive design for mobile devices */
        @media (max-width: 768px) {
          #chatbot-modal {
            width: 90% !important;
            max-width: 400px !important;
            right: 5% !important;
            left: 5% !important;
            margin: 0 auto !important;
            bottom: 70px !important;
            height: 60% !important;
            max-height: 500px !important;
          }
          
          #new-chat-btn {
            font-size: 12px !important;
            padding: 3px 6px !important;
          }
          
          #chatbot-send {
            min-width: 32px !important;
            height: 32px !important;
          }
          
          #chatbot-send svg {
            width: 16px !important;
            height: 16px !important;
          }
          
          #proficiency-selector {
            gap: 4px !important;
          }
          
          .proficiency-btn {
            font-size: 12px !important;
            padding: 4px 2px !important;
          }
        }
        
        /* Small phones */
        @media (max-width: 480px) {
          #chatbot-modal {
            width: 95% !important;
            height: 70% !important;
            right: 2.5% !important;
            left: 2.5% !important;
            bottom: 60px !important;
          }
          
          #chatbot-messages {
            max-height: 38vh !important;
          }
          
          #chatbot-input {
            flex: 1 1 auto !important;
            padding: 6px 6px !important;
            font-size: 13px !important;
            width: calc(100% - 42px) !important;
          }
          
          #chatbot-send {
            min-width: unset !important;
            width: 26px !important;
            height: 26px !important;
            padding: 2px !important;
            margin-left: 4px !important;
            flex: 0 0 auto !important;
          }
          
          #chatbot-send svg {
            width: 13px !important;
            height: 13px !important;
          }
          
          .proficiency-btn {
            padding: 4px 0px !important;
            font-size: 11px !important;
          }
          
          /* Adjust the container padding */
          #chatbot-modal > div:nth-of-type(4) {
            padding: 8px 12px 8px 12px !important;
          }
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
      messages.innerHTML = `<div style="text-align:center;padding:15px;color:#6b7280;font-size:13px;">Welcome to the AI Education Chatbot! I can answer questions about AI concepts from the course. What would you like to know?</div>`;
    }
    
    history.forEach(msg => {
      if (msg.role === 'user') {
        messages.innerHTML += `<div class="chatbot-user-msg">${escapeHTML(msg.content)}</div>`;
      } else if (msg.role === 'assistant') {
        const botMsg = document.createElement('div');
        botMsg.className = 'chatbot-bot-msg';
        botMsg.textContent = escapeHTML(msg.content);
        
        // Add citations if present
        if (msg.citations && msg.citations.length > 0) {
          const citationsDiv = document.createElement('div');
          citationsDiv.className = 'chatbot-citation';
          
          const citationsList = msg.citations.map(citation => 
            `[${citation.id}] ${citation.text} (${citation.location || 'Unknown location'})`
          ).join('<br>');
          
          citationsDiv.innerHTML = `<strong>Sources:</strong><br>${citationsList}`;
          botMsg.appendChild(citationsDiv);
        }
        
        messages.appendChild(botMsg);
        
        // Add follow-up questions if present
        if (msg.followUpQuestions && msg.followUpQuestions.length > 0) {
          displayFollowUpQuestions(msg.followUpQuestions);
        }
      }
    });
    messages.scrollTop = messages.scrollHeight;
  }

  function displayFollowUpQuestions(questions) {
    const messages = document.getElementById('chatbot-messages');
    if (!messages) return;
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'chatbot-suggestions';
    
    questions.forEach(question => {
      const btn = document.createElement('button');
      btn.className = 'chatbot-suggestion-btn';
      btn.textContent = question;
      btn.onclick = () => {
        // Track follow-up question selection
        Analytics.trackEvent('chatbot_followup_click', {
          question: question.substring(0, 100) + (question.length > 100 ? '...' : '')
        });
        
        document.getElementById('chatbot-input').value = question;
        sendMessage();
      };
      suggestionsDiv.appendChild(btn);
    });
    
    messages.appendChild(suggestionsDiv);
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const messages = document.getElementById('chatbot-messages');
    const typing = document.getElementById('chatbot-typing');
    const text = input.value.trim();
    if (!text) return;
    
    // Track the user question
    Analytics.trackQuestion(text);
    
    // Add user message to UI with new styling
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'chatbot-user-msg';
    userMsgDiv.textContent = text;
    messages.appendChild(userMsgDiv);
    messages.scrollTop = messages.scrollHeight;
    
    // Format conversation history
    let history = getHistory();
    history.push({ role: 'user', content: text });
    setHistory(history);
    
    // Clear input and show typing indicator
    input.value = '';
    typing.style.display = 'flex';
    
    // Get API URL based on current environment
    const apiUrl = getApiUrl();
    
    // Format request based on new Python API format
    fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        conversationHistory: history.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        proficiencyLevel: proficiencyLevel,
        conversationSummary: conversationSummary
      })
    })
      .then(r => r.json())
      .then(data => {
        typing.style.display = 'none';
        
        // Handle potential malformed response
        let processedData = data;
        
        // Check if we received a string instead of a parsed object
        if (typeof data === 'string') {
          try {
            // Try to parse it as JSON
            processedData = JSON.parse(data);
          } catch (e) {
            console.error('Failed to parse response as JSON:', e);
            // Extract content from malformed string if possible
            const textMatch = data.match(/"text":\s*"([^"]*)"/);
            if (textMatch && textMatch[1]) {
              processedData = {
                answer: { text: textMatch[1] },
                followUpQuestions: [],
                sources: []
              };
            }
          }
        }
        
        // Check if we need to clean up the answer text
        if (processedData.answer && typeof processedData.answer === 'string') {
          try {
            // Sometimes answer might be a JSON string instead of an object
            processedData.answer = JSON.parse(processedData.answer);
          } catch (e) {
            // If it fails, create a proper answer object
            processedData.answer = { text: processedData.answer };
          }
        }
        
        // Extract response data
        const reply = processedData.answer && processedData.answer.text 
          ? processedData.answer.text 
          : (processedData.reply || JSON.stringify(processedData));
        
        // Create bot message with new styling
        const botMsgDiv = document.createElement('div');
        botMsgDiv.className = 'chatbot-bot-msg';
        botMsgDiv.innerHTML = formatMessageWithCitations(reply);
        messages.appendChild(botMsgDiv);
        
        // Add sources/citations if present
        if (processedData.sources && processedData.sources.length > 0) {
          addSourcesSection(botMsgDiv, processedData.sources);
        }
        
        // Add follow-up questions if present
        if (processedData.followUpQuestions && processedData.followUpQuestions.length > 0) {
          displayFollowUpQuestions(processedData.followUpQuestions);
        }
        
        // Update conversation history
        history = getHistory();
        history.push({
          role: 'assistant',
          content: reply,
          followUpQuestions: processedData.followUpQuestions || [],
          sources: processedData.sources || []
        });
        setHistory(history);
        
        // Update conversation summary if provided
        if (processedData.conversationSummary) {
          conversationSummary = processedData.conversationSummary;
          sessionStorage.setItem(SUMMARY_KEY, conversationSummary);
        }
        
        // Scroll to bottom
        messages.scrollTop = messages.scrollHeight;
      })
      .catch(err => {
        typing.style.display = 'none';
        messages.innerHTML += `<div style='color:red;text-align:center;padding:8px;'>Error: ${escapeHTML(err.message)}</div>`;
        messages.scrollTop = messages.scrollHeight;
      });
  }

  // Format message text with citation numbers highlighted and clickable
  function formatMessageWithCitations(text) {
    if (!text) return '';
    // Highlight citation numbers [1], [2], etc. and make them clickable
    return escapeHTML(text).replace(/\[(\d+)\]/g, function(match, citationNumber) {
      return `<a href="#" class="citation-link" data-citation="${citationNumber}" style="color:${PRIMARY_COLOR};font-weight:bold;text-decoration:none;cursor:pointer;">${match}</a>`;
    });
  }

  // Add sources/citations if present
  function addSourcesSection(botMsgDiv, sources) {
    if (!sources || sources.length === 0) return;
    
    const citationsDiv = document.createElement('div');
    citationsDiv.className = 'chatbot-citation';
    
    const citationsList = sources
      .filter(source => source.relevance_score > 0.5) // Only show relevant sources
      .map(source => {
        // Simple fix for duplicate pages/ in URLs
        let sourceUrl = source.url || '';
        
        // Replace any occurrence of pages/pages/ with just pages/
        while (sourceUrl.includes('pages/pages/')) {
          sourceUrl = sourceUrl.replace('pages/pages/', 'pages/');
        }
        
        return `<div id="citation-${source.id}">
          <a href="${sourceUrl}" class="source-link" data-url="${sourceUrl}" style="color:${PRIMARY_COLOR};text-decoration:none;font-weight:bold;">[${source.id}]</a> 
          ${source.title}${source.section_title ? ` - ${source.section_title}` : ''}
          (<a href="${sourceUrl}" class="source-link" data-url="${sourceUrl}" style="color:${PRIMARY_COLOR};">${sourceUrl}</a>)
        </div>`;
      }).join('');
    
    citationsDiv.innerHTML = `<strong>Sources:</strong><br>${citationsList}`;
    botMsgDiv.appendChild(citationsDiv);
    
    // Add event listeners for citation links in the text
    setTimeout(() => {
      document.querySelectorAll('.citation-link').forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          const citationId = this.getAttribute('data-citation');
          const citationElement = document.getElementById(`citation-${citationId}`);
          if (citationElement) {
            // Track citation click
            Analytics.trackEvent('chatbot_citation_click', {
              citation_id: citationId
            });
            
            citationElement.scrollIntoView({ behavior: 'smooth' });
            citationElement.style.backgroundColor = '#fffde7';
            setTimeout(() => {
              citationElement.style.backgroundColor = 'transparent';
              citationElement.style.transition = 'background-color 1.5s ease';
            }, 100);
          }
        });
      });
      
      // Add event listeners for source links
      document.querySelectorAll('.source-link').forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          const url = this.getAttribute('data-url');
          
          // Track source navigation
          Analytics.trackEvent('chatbot_source_navigation', {
            url: url.substring(0, 100)
          });
          
          // Save chat state before navigating
          saveState();
          
          // Navigate to the source URL in the same tab
          window.location.href = url;
        });
      });
    }, 100);
  }
  
  // Save chat state before navigating away
  function saveState() {
    // Already handled by our existing session storage mechanism
    // Just make sure everything is saved before navigating
    setHistory(getHistory());
    sessionStorage.setItem(SUMMARY_KEY, conversationSummary);
    sessionStorage.setItem(PROFICIENCY_KEY, proficiencyLevel);
  }

  function clearHistory() {
    // Track session end before clearing
    Analytics.trackSessionEnd();
    
    // Clear session storage
    sessionStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(SUMMARY_KEY);
    sessionStorage.removeItem(SESSION_START_KEY); // Also clear session start time
    
    // Reset conversation summary
    conversationSummary = '';
    
    // Clear messages display
    const messages = document.getElementById('chatbot-messages');
    if (messages) {
      messages.innerHTML = '<div style="text-align:center;padding:15px;color:#6b7280;font-size:13px;">Welcome to the AI Education Chatbot! I can answer questions about AI concepts from the course. What would you like to know?</div>';
    }
    
    // Start a new session
    Analytics.initSession();
    
    console.log("Chat history cleared");
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, function(tag) {
      const charsToReplace = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      };
      return charsToReplace[tag] || tag;
    });
  }

  // Determine current environment based on hostname
  function getApiUrl() {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      console.log('Using local API endpoint');
      return API_CONFIG.local;
    } else {
      console.log('Using production API endpoint');
      return API_CONFIG.production;
    }
  }
})(); 