// Auto-focus no input
        document.querySelector('.message-input').focus();
        
        // Scroll automático para o final do chat
        const chatHistory = document.querySelector('.chat-history');
        if (chatHistory) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        
        // Animação elegante ao enviar
        document.querySelector('.chat-form').addEventListener('submit', function(e) {
            const button = document.querySelector('.send-button');
            const input = document.querySelector('.message-input');
            
            button.style.transform = 'scale(0.95)';
            input.style.transform = 'scale(0.98)';
            
            setTimeout(() => {
                button.style.transform = '';
                input.style.transform = '';
            }, 200);
        });
        
        // Auto-scroll suave e elegante
        function smoothScrollToBottom() {
            const chatHistory = document.querySelector('.chat-history');
            if (chatHistory) {
                chatHistory.scrollTo({
                    top: chatHistory.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }

        // Scroll após carregamento
        window.addEventListener('load', smoothScrollToBottom);

        // Subtle hover effects for messages
        document.addEventListener('DOMContentLoaded', function() {
            const messages = document.querySelectorAll('.message');
            messages.forEach(message => {
                message.addEventListener('mouseenter', function() {
                    this.style.filter = 'brightness(1.05)';
                });
                message.addEventListener('mouseleave', function() {
                    this.style.filter = '';
                });
            });
        });

        // Dynamic star creation
        function createFallingStar() {
            const star = document.createElement('div');
            star.innerHTML = '⭐';
            star.style.position = 'fixed';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = '-20px';
            star.style.fontSize = '1rem';
            star.style.opacity = '0.6';
            star.style.pointerEvents = 'none';
            star.style.zIndex = '0';
            star.style.animation = 'fallingStar 8s linear forwards';
            
            document.body.appendChild(star);
            
            setTimeout(() => {
                star.remove();
            }, 8000);
        }

        // Add falling star animation
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes fallingStar {
                to {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        // Create stars periodically
        setInterval(createFallingStar, 15000);