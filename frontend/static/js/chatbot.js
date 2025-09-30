// Ultra-Modern Enhanced Chatbot JavaScript
class K2Chatbot {
    constructor() {
        this.isTyping = false;
        this.messageHistory = [];
        this.particleSystem = null;
        this.animationQueue = [];
        this.soundEnabled = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupElements();
        this.initParticleSystem();
        this.showWelcomeMessage();
        this.initEnhancedAnimations();
    }

    bindEvents() {
        // Message input and sending
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-message');
        
        if (messageInput) {
            messageInput.addEventListener('input', () => this.handleInputChange());
            messageInput.addEventListener('keypress', (e) => this.handleKeyPress(e));
        }
        
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }

        // Quick action buttons
        document.querySelectorAll('.quick-action').forEach(button => {
            button.addEventListener('click', (e) => {
                const message = e.target.getAttribute('data-message');
                if (message) {
                    this.sendQuickAction(message);
                }
            });
        });

        // Clear chat
        const clearButton = document.getElementById('clear-chat');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearChat());
        }

        // Sidebar toggle for mobile
        const sidebarToggle = document.getElementById('sidebar-toggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => this.toggleSidebar());
        }

        // Settings button (placeholder)
        const settingsButton = document.getElementById('settings');
        if (settingsButton) {
            settingsButton.addEventListener('click', () => this.openSettings());
        }

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            const sidebar = document.querySelector('.sidebar');
            const sidebarToggle = document.getElementById('sidebar-toggle');
            
            if (window.innerWidth <= 768 && 
                sidebar && sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !sidebarToggle.contains(e.target)) {
                this.closeSidebar();
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                this.closeSidebar();
            }
        });
    }

    setupElements() {
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-message');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.welcomeMessage = document.querySelector('.welcome-message');
    }

    handleInputChange() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isTyping;
        
        // Add visual feedback
        this.sendButton.style.opacity = hasText && !this.isTyping ? '1' : '0.5';
    }

    handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }

    async sendMessage(message = null) {
        const text = message || this.messageInput.value.trim();
        if (!text || this.isTyping) return;

        // Clear input
        this.messageInput.value = '';
        this.handleInputChange();

        // Hide welcome message
        this.hideWelcomeMessage();

        // Add user message
        this.addMessage(text, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        // Simulate API call delay
        await this.simulateTyping();

        // Hide typing indicator
        this.hideTypingIndicator();

        // Generate bot response
        const botResponse = this.generateBotResponse(text);
        this.addMessage(botResponse, 'bot');

        // Focus back to input
        this.messageInput.focus();
    }

    sendQuickAction(message) {
        this.sendMessage(message);
    }

// Original addMessage method replaced with enhanced version below

    formatMessage(text) {
        // Basic text formatting - can be enhanced
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    generateBotResponse(userMessage) {
        // Placeholder bot responses - integrate with your actual chatbot API
        const responses = {
            'policy': 'I can help you analyze policy documents and provide insights. What specific policy would you like to discuss?',
            'regulation': 'I have access to various regulations and compliance guidelines. Which area of regulation are you interested in?',
            'compliance': 'I can assist with compliance guidance and requirements. What compliance area do you need help with?',
            'analyze': 'I\'d be happy to analyze that for you. Could you please provide more details or upload the document?',
            'search': 'I can search through our policy database. What specific terms or topics would you like me to search for?',
            'help': 'I\'m here to help! I can assist with policy analysis, regulation searches, compliance guidance, and more. What can I help you with today?',
            'default': 'I understand you\'re asking about that topic. As an AI assistant specialized in policy analysis, I can help you with various policy-related questions. Could you provide more specific details about what you\'d like to know?'
        };

        // Simple keyword matching - replace with actual AI integration
        const lowerMessage = userMessage.toLowerCase();
        
        for (const [keyword, response] of Object.entries(responses)) {
            if (keyword !== 'default' && lowerMessage.includes(keyword)) {
                return response;
            }
        }
        
        return responses.default;
    }

    async simulateTyping() {
        this.isTyping = true;
        this.handleInputChange();
        
        // Random delay between 1-3 seconds to simulate thinking
        const delay = Math.random() * 2000 + 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
        
        this.isTyping = false;
        this.handleInputChange();
    }

    showTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'block';
            this.typingIndicator.style.opacity = '0';
            
            requestAnimationFrame(() => {
                this.typingIndicator.style.transition = 'opacity 0.3s ease';
                this.typingIndicator.style.opacity = '1';
            });
        }
    }

    hideTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.opacity = '0';
            setTimeout(() => {
                this.typingIndicator.style.display = 'none';
            }, 300);
        }
    }

    showWelcomeMessage() {
        if (this.welcomeMessage) {
            this.welcomeMessage.style.display = 'block';
        }
    }

    hideWelcomeMessage() {
        if (this.welcomeMessage) {
            this.welcomeMessage.style.transition = 'all 0.3s ease';
            this.welcomeMessage.style.opacity = '0';
            this.welcomeMessage.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                this.welcomeMessage.style.display = 'none';
            }, 300);
        }
    }

    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }

    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            // Remove all messages except welcome
            const messages = this.chatMessages.querySelectorAll('.message');
            messages.forEach(message => message.remove());
            
            // Clear message history
            this.messageHistory = [];
            
            // Show welcome message again
            this.showWelcomeMessage();
            
            // Focus input
            if (this.messageInput) {
                this.messageInput.focus();
            }
        }
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
    }

    closeSidebar() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.remove('active');
        }
    }

    openSettings() {
        // Placeholder for settings functionality
        alert('Settings panel coming soon! This will allow you to customize your chat experience.');
    }

    // Method to integrate with your backend API
    async sendToAPI(message) {
        try {
            // Replace with your actual API endpoint
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            return data.response || 'Sorry, I couldn\'t process that request.';
        } catch (error) {
            console.error('Error sending message to API:', error);
            return 'I\'m sorry, I\'m having trouble connecting right now. Please try again later.';
        }
    }

    // Method to handle file uploads (when implemented)
    handleFileUpload(file) {
        // Placeholder for file upload functionality
        console.log('File upload:', file);
        this.addMessage(`I received your file: ${file.name}. File upload processing will be implemented soon.`, 'bot');
    }

    // Method to export chat history
    exportChatHistory() {
        const chatData = {
            timestamp: new Date().toISOString(),
            messages: this.messageHistory
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `k2-chat-history-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }

    // Method to load chat history
    loadChatHistory(chatData) {
        this.hideWelcomeMessage();
        this.messageHistory = chatData.messages || [];
        
        // Clear current messages
        const messages = this.chatMessages.querySelectorAll('.message');
        messages.forEach(message => message.remove());
        
        // Add historical messages with staggered animation
        this.messageHistory.forEach((msg, index) => {
            setTimeout(() => {
                this.addMessage(msg.text, msg.sender);
            }, index * 200);
        });
    }

    // Initialize particle system for background effects
    initParticleSystem() {
        const particleBg = document.getElementById('particle-bg');
        if (!particleBg) return;

        this.particleSystem = {
            particles: [],
            maxParticles: 15,
            container: particleBg
        };

        this.createParticles();
        this.animateParticles();
    }

    createParticles() {
        for (let i = 0; i < this.particleSystem.maxParticles; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random properties
            const size = Math.random() * 6 + 2;
            const delay = Math.random() * 20;
            const left = Math.random() * 100;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${left}%`;
            particle.style.animationDelay = `${delay}s`;
            particle.style.animationDuration = `${20 + Math.random() * 10}s`;
            
            this.particleSystem.container.appendChild(particle);
            this.particleSystem.particles.push(particle);
        }
    }

    animateParticles() {
        // Particles are animated via CSS, but we can add interaction
        this.particleSystem.particles.forEach(particle => {
            particle.addEventListener('animationiteration', () => {
                // Randomize position on each iteration
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.animationDuration = `${20 + Math.random() * 10}s`;
            });
        });
    }

    // Initialize enhanced animations and micro-interactions
    initEnhancedAnimations() {
        // Add hover effects to interactive elements
        this.addHoverEffects();
        
        // Add typing animation to input
        this.addTypingEffects();
        
        // Add smooth scrolling to chat
        this.addSmoothScrolling();
        
        // Add entrance animations
        this.addEntranceAnimations();
    }

    addHoverEffects() {
        // Enhanced button hover effects
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', (e) => {
                this.createRippleEffect(e);
                this.addButtonGlow(button);
            });
            
            button.addEventListener('mouseleave', () => {
                this.removeButtonGlow(button);
            });
        });

        // Message hover effects
        this.chatMessages.addEventListener('mouseenter', (e) => {
            if (e.target.closest('.message-bubble')) {
                const bubble = e.target.closest('.message-bubble');
                bubble.style.transform = 'translateY(-3px) scale(1.02)';
                bubble.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
            }
        }, true);

        this.chatMessages.addEventListener('mouseleave', (e) => {
            if (e.target.closest('.message-bubble')) {
                const bubble = e.target.closest('.message-bubble');
                bubble.style.transform = 'translateY(0) scale(1)';
            }
        }, true);
    }

    createRippleEffect(e) {
        const button = e.currentTarget;
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.6) 0%, transparent 70%);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            pointer-events: none;
            z-index: 1000;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    addButtonGlow(button) {
        button.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.6), 0 0 40px rgba(102, 126, 234, 0.4)';
    }

    removeButtonGlow(button) {
        button.style.boxShadow = '';
    }

    addTypingEffects() {
        let typingTimer;
        this.messageInput.addEventListener('input', () => {
            clearTimeout(typingTimer);
            this.messageInput.classList.add('typing-active');
            
            typingTimer = setTimeout(() => {
                this.messageInput.classList.remove('typing-active');
            }, 1000);
        });
    }

    addSmoothScrolling() {
        // Enhanced smooth scrolling with easing
        this.originalScrollToBottom = this.scrollToBottom.bind(this);
        this.scrollToBottom = this.smoothScrollToBottom.bind(this);
    }

    smoothScrollToBottom() {
        if (!this.chatMessages) return;
        
        const start = this.chatMessages.scrollTop;
        const end = this.chatMessages.scrollHeight - this.chatMessages.clientHeight;
        const distance = end - start;
        const duration = Math.min(800, Math.abs(distance) * 2);
        
        if (distance === 0) return;
        
        const startTime = performance.now();
        
        const animateScroll = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out-cubic)
            const easeOutCubic = 1 - Math.pow(1 - progress, 3);
            
            this.chatMessages.scrollTop = start + distance * easeOutCubic;
            
            if (progress < 1) {
                requestAnimationFrame(animateScroll);
            }
        };
        
        requestAnimationFrame(animateScroll);
    }

    addEntranceAnimations() {
        // Staggered animation for sidebar items
        const sidebarItems = document.querySelectorAll('.session-item');
        sidebarItems.forEach((item, index) => {
            item.style.animationDelay = `${0.2 + index * 0.1}s`;
        });
        
        // Enhanced welcome message animation
        const welcomeElements = document.querySelectorAll('.welcome-message > *');
        welcomeElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.animation = `fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) ${0.3 + index * 0.2}s forwards`;
        });
    }

    // Enhanced message addition with better animations
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const timestamp = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageDiv.innerHTML = `
            <div class="message-bubble glass-effect">
                ${this.formatMessage(text)}
                <span class="message-time">${timestamp}</span>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        
        // Add to message history
        this.messageHistory.push({ text, sender, timestamp });
        
        // Enhanced entrance animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(30px) scale(0.8)';
        messageDiv.style.filter = 'blur(5px)';
        
        requestAnimationFrame(() => {
            messageDiv.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0) scale(1)';
            messageDiv.style.filter = 'blur(0)';
        });
        
        // Scroll to bottom with animation
        setTimeout(() => {
            this.scrollToBottom();
        }, 100);
        
        // Add sparkle effect for bot messages
        if (sender === 'bot') {
            this.addSparkleEffect(messageDiv);
        }
    }

    addSparkleEffect(element) {
        const sparkles = 5;
        for (let i = 0; i < sparkles; i++) {
            setTimeout(() => {
                const sparkle = document.createElement('div');
                sparkle.style.cssText = `
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: radial-gradient(circle, #667eea, transparent);
                    border-radius: 50%;
                    pointer-events: none;
                    animation: sparkle 1.5s ease-out forwards;
                    z-index: 1000;
                `;
                
                const rect = element.getBoundingClientRect();
                sparkle.style.left = `${rect.left + Math.random() * rect.width}px`;
                sparkle.style.top = `${rect.top + Math.random() * rect.height}px`;
                
                document.body.appendChild(sparkle);
                
                setTimeout(() => sparkle.remove(), 1500);
            }, i * 200);
        }
    }
}

// Utility functions
function formatTime(date) {
    return new Date(date).toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new K2Chatbot();
    
    // Add some helpful keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus message input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const messageInput = document.getElementById('message-input');
            if (messageInput) {
                messageInput.focus();
            }
        }
        
        // Escape to close sidebar on mobile
        if (e.key === 'Escape') {
            window.chatbot.closeSidebar();
        }
    });
    
    // Add visual feedback for better UX
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('focus', () => {
            messageInput.parentElement.style.borderColor = 'var(--primary-color)';
        });
        
        messageInput.addEventListener('blur', () => {
            messageInput.parentElement.style.borderColor = 'var(--border-color)';
        });
    }
});

// Service Worker registration for offline capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when you have a service worker file
        // navigator.serviceWorker.register('/static/js/sw.js')
        //     .then((registration) => {
        //         console.log('SW registered: ', registration);
        //     })
        //     .catch((registrationError) => {
        //         console.log('SW registration failed: ', registrationError);
        //     });
    });
}

// Export for use in other scripts if needed
window.K2Chatbot = K2Chatbot;
