// Studio3 Interactive Elements

document.addEventListener('DOMContentLoaded', function() {
    // Animate numbers on scroll
    const animateValue = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Animate numbers
                if (entry.target.classList.contains('animate-number')) {
                    const endValue = parseInt(entry.target.getAttribute('data-value'));
                    animateValue(entry.target, 0, endValue, 2000);
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.arena-card, .phase-indicator, .animate-number').forEach(el => {
        observer.observe(el);
    });

    // Signal Orb interactive effect
    const signalOrbs = document.querySelectorAll('.signal-orb');
    signalOrbs.forEach(orb => {
        orb.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        orb.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        orb.addEventListener('click', function() {
            // Create ripple effect
            const ripple = document.createElement('div');
            ripple.className = 'orb-ripple';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 1000);
        });
    });

    // Phase timeline interactions
    const phaseIndicators = document.querySelectorAll('.phase-timeline .phase-indicator');
    phaseIndicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function() {
            // Create tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'phase-tooltip';
            tooltip.textContent = `Phase ${index + 1}: ${this.textContent}`;
            tooltip.style.cssText = `
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: var(--studio3-navy);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.875rem;
                white-space: nowrap;
                z-index: 1000;
                margin-bottom: 0.5rem;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            this.style.position = 'relative';
            this.appendChild(tooltip);
            
            // Fade in
            setTimeout(() => tooltip.style.opacity = '1', 10);
            
            // Remove after delay
            setTimeout(() => {
                tooltip.style.opacity = '0';
                setTimeout(() => tooltip.remove(), 300);
            }, 2000);
        });
    });

    // Belief/Doubt button effects
    const signalButtons = document.querySelectorAll('.belief-button, .doubt-button');
    signalButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Create pulse effect
            const pulse = document.createElement('span');
            pulse.className = 'button-pulse';
            pulse.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                width: 100%;
                height: 100%;
                border-radius: 8px;
                background: currentColor;
                opacity: 0.3;
                transform: translate(-50%, -50%);
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(pulse);
            
            // Animate pulse
            pulse.animate([
                { transform: 'translate(-50%, -50%) scale(0)', opacity: 0.3 },
                { transform: 'translate(-50%, -50%) scale(2)', opacity: 0 }
            ], {
                duration: 600,
                easing: 'ease-out'
            }).onfinish = () => pulse.remove();
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation to async content
    const loadingElements = document.querySelectorAll('[data-loading]');
    loadingElements.forEach(element => {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        element.appendChild(spinner);
        
        // Simulate content loading
        setTimeout(() => {
            spinner.remove();
            element.classList.add('loaded');
        }, 1000);
    });

    // Create floating particles effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const particleCount = 20;
        const particles = [];
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'hero-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                pointer-events: none;
                animation: float ${10 + Math.random() * 20}s infinite ease-in-out;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 5}s;
            `;
            heroSection.appendChild(particle);
            particles.push(particle);
        }
        
        // Add floating animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0%, 100% {
                    transform: translateY(0) translateX(0);
                }
                25% {
                    transform: translateY(-20px) translateX(10px);
                }
                50% {
                    transform: translateY(10px) translateX(-10px);
                }
                75% {
                    transform: translateY(-10px) translateX(20px);
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Arena card tilt effect on hover
    const arenaCards = document.querySelectorAll('.arena-card');
    arenaCards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // Copy code blocks with feedback
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const pre = block.parentElement;
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '📋';
        copyButton.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: var(--studio3-pink);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            cursor: pointer;
            font-size: 1rem;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        wrapper.appendChild(copyButton);
        
        wrapper.addEventListener('mouseenter', () => {
            copyButton.style.opacity = '1';
        });
        
        wrapper.addEventListener('mouseleave', () => {
            copyButton.style.opacity = '0';
        });
        
        copyButton.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(block.textContent);
                copyButton.innerHTML = '✅';
                setTimeout(() => {
                    copyButton.innerHTML = '📋';
                }, 2000);
            } catch (err) {
                copyButton.innerHTML = '❌';
                setTimeout(() => {
                    copyButton.innerHTML = '📋';
                }, 2000);
            }
        });
    });
});

// Add CSS for animations
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .orb-ripple {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        from {
            transform: translate(-50%, -50%) scale(0);
            opacity: 1;
        }
        to {
            transform: translate(-50%, -50%) scale(2);
            opacity: 0;
        }
    }
    
    .loaded {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;

document.head.appendChild(animationStyles);