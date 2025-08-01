// construction-popup.js - Simple reusable popup system
(function() {
  // Popup configurations
  const popupConfig = {
    'donation': {
      icon: '🚧',
      title: 'Feature Under Construction',
      message: "We're currently working on implementing our donation system to make it as secure and user-friendly as possible.",
      email: 'jesse.wimer@wsu.edu',
      emailText: 'For donation options, please email:',
      thankYou: 'Thank you for your patience and interest in supporting Foodcheqr!'
    },
    'login': {
      icon: '🚧',
      title: 'Login System Under Development',
      message: "We're working on implementing a secure login system for our users.",
      email: 'jesse.wimer@wsu.edu',
      emailText: 'For access questions, please email:',
      thankYou: 'Thank you for your patience!'
    },
    'registration': {
      icon: '🚧',
      title: 'Registration Coming Soon',
      message: "We're currently developing our user registration system to ensure the best experience for our users.",
      email: 'jesse.wimer@wsu.edu',
      emailText: 'For early access, please contact:',
      thankYou: 'Thank you for your interest in joining Foodcheqr!'
    },
    'default': {
      icon: '🚧',
      title: 'Feature Under Construction',
      message: "This feature is currently under development. We're working hard to bring it to you soon.",
      email: 'jesse.wimer@wsu.edu',
      emailText: 'For more information, please contact:',
      thankYou: 'Thank you for your patience!'
    }
  };

  // Create popup HTML on page load
  function createPopup() {
    if (document.getElementById('constructionPopup')) return;

    const popupHTML = `
      <div id="constructionPopup" class="construction-popup-overlay" onclick="hideConstructionPopup()">
        <div class="construction-popup-content" onclick="event.stopPropagation()">
          <div class="construction-popup-icon" id="popupIcon">🚧</div>
          <h2 class="construction-popup-title" id="popupTitle">Feature Under Construction</h2>
          <p class="construction-popup-message" id="popupMessage">This feature is under development.</p>
          <div class="construction-popup-email">
            <p><strong id="popupEmailText">For more information, please email:</strong></p>
            <p><strong id="popupEmail">jesse.wimer@wsu.edu</strong></p>
          </div>
          <p class="construction-popup-message" id="popupThankYou">Thank you for your patience!</p>
          <button class="construction-popup-close" onclick="hideConstructionPopup()">Got it!</button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', popupHTML);

    // Add CSS
    const style = document.createElement('style');
    style.textContent = `
      .construction-popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6);
        display: none;
        justify-content: center;
        align-items: center;
        z-index: 9999;
      }
      .construction-popup-content {
        background: white;
        padding: 40px 30px;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        text-align: center;
        max-width: 500px;
        width: 90%;
        position: relative;
        animation: popupAppear 0.3s ease-out;
      }
      @keyframes popupAppear {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
      }
      .construction-popup-title {
        color: #ff6b35;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: 600;
      }
      .construction-popup-message {
        color: #333;
        margin-bottom: 20px;
        line-height: 1.6;
        font-size: 16px;
      }
      .construction-popup-email {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        border-left: 4px solid #2a7ae2;
      }
      .construction-popup-email strong {
        color: #2a7ae2;
        font-size: 18px;
      }
      .construction-popup-close {
        background-color: #2a7ae2;
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
      }
      .construction-popup-close:hover {
        background-color: #1f5bbf;
      }
      .construction-popup-icon {
        font-size: 48px;
        margin-bottom: 15px;
      }
    `;
    document.head.appendChild(style);
  }

  // Show popup function
  window.showConstructionPopup = function(type = 'default') {
    const config = popupConfig[type] || popupConfig['default'];
    
    document.getElementById('popupIcon').textContent = config.icon;
    document.getElementById('popupTitle').textContent = config.title;
    document.getElementById('popupMessage').textContent = config.message;
    document.getElementById('popupEmailText').textContent = config.emailText;
    document.getElementById('popupEmail').textContent = config.email;
    document.getElementById('popupThankYou').textContent = config.thankYou;
    
    document.getElementById('constructionPopup').style.display = 'flex';
  };

  // Hide popup function
  window.hideConstructionPopup = function() {
    document.getElementById('constructionPopup').style.display = 'none';
  };

  // Escape key handler
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      hideConstructionPopup();
    }
  });

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createPopup);
  } else {
    createPopup();
  }
})();