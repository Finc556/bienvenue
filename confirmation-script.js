// CONFIRMATION PAGE SCRIPT WITH CONDITIONAL LOGIC

// CONFIGURATION
const CONFIG = {
    // URLs for downloads and access (replace with actual links)

    LINKEDIN_URL: 'https://www.linkedin.com/company/elan-vital',
    
    // Particles configuration
    PARTICLES_CONFIG: {
        particles: {
            number: {
                value: 50,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: "#D4AF37"
            },
            shape: {
                type: "circle",
                stroke: {
                    width: 0,
                    color: "#000000"
                }
            },
            opacity: {
                value: 0.3,
                random: false,
                anim: {
                    enable: false,
                    speed: 1,
                    opacity_min: 0.1,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                anim: {
                    enable: false,
                    speed: 40,
                    size_min: 0.1,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: "#D4AF37",
                opacity: 0.2,
                width: 1
            },
            move: {
                enable: true,
                speed: 3,
                direction: "none",
                random: false,
                straight: false,
                out_mode: "out",
                bounce: false,
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: {
                    enable: true,
                    mode: "repulse"
                },
                onclick: {
                    enable: true,
                    mode: "push"
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 400,
                    line_linked: {
                        opacity: 1
                    }
                },
                bubble: {
                    distance: 400,
                    size: 40,
                    duration: 2,
                    opacity: 8,
                    speed: 3
                },
                repulse: {
                    distance: 200,
                    duration: 0.4
                },
                push: {
                    particles_nb: 4
                },
                remove: {
                    particles_nb: 2
                }
            }
        },
        retina_detect: true
    }
};

// STATE MANAGEMENT
const state = {
    hasUpsell: false,
    pageStartTime: Date.now(),
    particlesInitialized: false
};

// DOM ELEMENTS
const elements = {
    loadingOverlay: document.getElementById('loadingOverlay'),
    upsellProduct: document.getElementById('upsellProduct'),
    successModal: document.getElementById('successModal'),
    particlesContainer: document.getElementById('particles-js')
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    checkUpsellStatus();
    initializeParticles();
    setupEventListeners();
    addAccessibilityFeatures();
    trackPageView();
});

// PAGE INITIALIZATION
function initializePage() {
    // Hide loading overlay after a delay
    setTimeout(() => {
        if (elements.loadingOverlay) {
            elements.loadingOverlay.classList.add('hidden');
            document.body.classList.remove('loading');
        }
    }, 1500);
    
    console.log('✅ Página de confirmação inicializada');
}

    // CRITICAL: UPSELL CONDITIONAL LOGIC
function checkUpsellStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotmartProductId = urlParams.get('hotmart_product_id');
    
    // IMPORTANT: Replace 'YOUR_UPSELL_PRODUCT_ID_HERE' with the actual Hotmart product ID for the upsell (47€ product)
    const UPSELL_PRODUCT_ID = 'YOUR_UPSELL_PRODUCT_ID_HERE'; 

    state.hasUpsell = (hotmartProductId === UPSELL_PRODUCT_ID);
    
    // Apply conditional display
    if (state.hasUpsell && elements.upsellProduct) {
        showUpsellProduct();
    } else if (elements.upsellProduct) {
        hideUpsellProduct();
    }
    
    console.log(`🎯 Status do upsell: ${state.hasUpsell ? 'POSSUI' : 'NÃO POSSUI'}`);
    console.log(`Hotmart Product ID na URL: ${hotmartProductId || 'Nenhum'}`);
    console.log(`ID do produto upsell esperado: ${UPSELL_PRODUCT_ID}`);
}

function showUpsellProduct() {
    if (elements.upsellProduct) {
        elements.upsellProduct.classList.remove('hidden');
        elements.upsellProduct.style.display = 'block'; // Ensure it's block if it was display:none
        
        // Add entrance animation
        setTimeout(() => {
            elements.upsellProduct.style.opacity = '0';
            elements.upsellProduct.style.transform = 'translateY(30px)';
            elements.upsellProduct.style.transition = 'all 0.8s ease-out';
            
            setTimeout(() => {
                elements.upsellProduct.style.opacity = '1';
                elements.upsellProduct.style.transform = 'translateY(0)';
            }, 100);
        }, 500);
        
        console.log('✅ Produto upsell exibido');
    }
}

function hideUpsellProduct() {
    if (elements.upsellProduct) {
        elements.upsellProduct.classList.add('hidden');
        elements.upsellProduct.style.display = 'none';
        console.log('❌ Produto upsell ocultado');
    }
}

// PARTICLES INITIALIZATION
function initializeParticles() {
    if (typeof particlesJS !== 'undefined' && elements.particlesContainer) {
        particlesJS('particles-js', CONFIG.PARTICLES_CONFIG);
        state.particlesInitialized = true;
        console.log('✅ Partículas inicializadas');
    } else {
        console.warn('⚠️ Biblioteca particles.js não encontrada');
    }
}

// EVENT LISTENERS SETUP
function setupEventListeners() {
    // Scroll animations
    window.addEventListener('scroll', handleScrollAnimations);
    
    // Resize handling
    window.addEventListener('resize', handleResize);
    
    // Keyboard navigation
    document.addEventListener('keydown', handleKeyboardNavigation);
    
    // Close modal on backdrop click
    if (elements.successModal) {
        const backdrop = elements.successModal.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.addEventListener('click', closeModal);
        }
    }
}




// UTILITY FUNCTIONS
function handleScrollAnimations() {
    // Add scroll-based animations here if needed
    const sections = document.querySelectorAll('section');
    
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        
        if (isVisible && !section.classList.contains('animated')) {
            section.classList.add('animated');
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }
    });
}

function handleResize() {
    if (state.particlesInitialized && typeof pJSDom !== 'undefined') {
        pJSDom[0].pJS.fn.particlesRefresh();
    }
}

function handleKeyboardNavigation(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
}

function addAccessibilityFeatures() {
    // Add ARIA labels and keyboard navigation
    const buttons = document.querySelectorAll('button, a[role="button"]');
    buttons.forEach(button => {
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
        
        // Add keyboard support
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                button.click();
            }
        });
    });
    
    // Add focus indicators
    const style = document.createElement('style');
    style.textContent = `
        button:focus,
        a:focus {
            outline: 2px solid #D4AF37;
            outline-offset: 2px;
        }
    `;
    document.head.appendChild(style);
}

// ANALYTICS
function trackEvent(eventName, data = {}) {
    const eventData = {
        event_name: eventName,
        timestamp: new Date().toISOString(),
        page_url: window.location.href,
        user_agent: navigator.userAgent,
        viewport: {
            width: window.innerWidth,
            height: window.innerHeight
        },
        ...data
    };
    
    console.log('📊 Event tracked:', eventData);
    
    // Google Analytics 4
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    }
    
    // Facebook Pixel
    if (typeof fbq !== 'undefined') {
        fbq('track', 'CustomEvent', eventData);
    }
    
    // Hotmart tracking
    if (typeof _hmq !== 'undefined') {
        _hmq.push(['track', eventName, eventData]);
    }
    
    // Custom analytics endpoint
    if (CONFIG.ANALYTICS_ENDPOINT) {
        fetch(CONFIG.ANALYTICS_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(eventData)
        }).catch(console.error);
    }
}

function trackPageView() {
    trackEvent('confirmation_page_view', {
        has_upsell: state.hasUpsell,
        referrer: document.referrer,
        timestamp: new Date().toISOString()
    });
}

// TESTING FUNCTIONS (for development)
function testUpsellShow() {
    state.hasUpsell = true;
    showUpsellProduct();
    console.log('🧪 Teste: Produto upsell forçado a aparecer');
}

function testUpsellHide() {
    state.hasUpsell = false;
    hideUpsellProduct();
    console.log('🧪 Teste: Produto upsell forçado a esconder');
}

// URL PARAMETER HELPERS
function setUpsellParameter(hasUpsell) {
    const url = new URL(window.location);
    url.searchParams.set('upsell', hasUpsell ? 'true' : 'false');
    window.history.replaceState({}, '', url);
}

function simulateUpsellPurchase() {
    // Simulate upsell purchase for testing
    localStorage.setItem('purchase', JSON.stringify({
        includesUpsell: true,
        timestamp: Date.now()
    }));
    
    sessionStorage.setItem('hasUpsell', 'true');
    setUpsellParameter(true);
    
    // Reload to test
    window.location.reload();
}

function simulateBasicPurchase() {
    // Simulate basic purchase for testing
    localStorage.setItem('purchase', JSON.stringify({
        includesUpsell: false,
        timestamp: Date.now()
    }));
    
    sessionStorage.setItem('hasUpsell', 'false');
    setUpsellParameter(false);
    
    // Reload to test
    window.location.reload();
}

// EXPORT FOR DEBUGGING
if (typeof window !== 'undefined') {
    window.ConfirmationPage = {
        state,
        elements,
        checkUpsellStatus,
        showUpsellProduct,
        hideUpsellProduct,

        followLinkedIn,
        trackEvent,
        CONFIG,
        // Testing functions
        testUpsellShow,
        testUpsellHide,
        simulateUpsellPurchase,
        simulateBasicPurchase
    };
    
    console.log('🔧 Funções de debug disponíveis em window.ConfirmationPage');
}

