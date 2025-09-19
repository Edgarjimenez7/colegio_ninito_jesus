'use strict';

/**
 * Main menu functionality with security considerations
 */
(function() {
    // Strict mode and IIFE to avoid polluting global scope
    'use strict';

    // Configuration
    const CONFIG = {
        maxImageLoadTime: 2000, // 2 seconds
        animationFrameRate: 60, // Target FPS
        debounceTime: 100, // ms
        maxParallaxOffset: 30, // pixels
        minViewportWidth: 320 // pixels
    };

    // State management
    const state = {
        isInitialized: false,
        lastAnimationFrame: null,
        lastMousePosition: { x: 0, y: 0 },
        windowSize: {
            width: window.innerWidth,
            height: window.innerHeight
        }
    };

    // DOM Elements
    let menuItems = [];

    /**
     * Initialize the menu functionality
     */
    function init() {
        try {
            if (state.isInitialized) return;
            
            // Get menu items safely
            const items = document.querySelectorAll('.menu-item');
            if (!items.length) {
                console.warn('No menu items found');
                return;
            }

            menuItems = Array.from(items).map(item => ({
                element: item,
                img: item.querySelector('img'),
                speed: parseFloat(item.getAttribute('data-speed') || '1') * 0.5,
                bounds: null
            }));

            // Set up event listeners
            setupEventListeners();
            
            // Initial setup
            updateElementBounds();
            
            // Mark as initialized
            state.isInitialized = true;
            
            console.log('Menu initialized successfully');
            
        } catch (error) {
            console.error('Error initializing menu:', error);
            // Fallback: Disable animations on error
            document.body.classList.add('no-animations');
        }
    }

    /**
     * Set up event listeners with proper cleanup
     */
    function setupEventListeners() {
        // Window events
        const debouncedResize = debounce(handleResize, CONFIG.debounceTime);
        window.addEventListener('resize', debouncedResize, { passive: true });
        window.addEventListener('orientationchange', debouncedResize, { passive: true });
        
        // Mouse movement with passive listener for better performance
        document.addEventListener('mousemove', handleMouseMove, { passive: true });
        
        // Clean up on page unload
        window.addEventListener('beforeunload', cleanup);
        
        // Handle reduced motion preference
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addEventListener('change', handleMotionPreference);
        handleMotionPreference(mediaQuery);
        
        // Menu item click handlers
        menuItems.forEach(item => {
            item.element.addEventListener('click', handleMenuItemClick, false);
            
            // Add keyboard navigation support
            item.element.setAttribute('tabindex', '0');
            item.element.addEventListener('keydown', handleKeyDown);
            
            // Handle image loading errors
            if (item.img) {
                item.img.addEventListener('error', handleImageError);
                
                // Set loading="lazy" for better performance
                item.img.loading = 'lazy';
                
                // Add loading state
                item.element.classList.add('loading');
                
                // Handle image load timeout
                const loadTimer = setTimeout(() => {
                    if (!item.img.complete) {
                        handleImageError({ target: item.img });
                    }
                }, CONFIG.maxImageLoadTime);
                
                item.img.addEventListener('load', function() {
                    clearTimeout(loadTimer);
                    item.element.classList.remove('loading');
                    item.element.classList.add('loaded');
                }, { once: true });
            }
        });
    }

    /**
     * Handle mouse movement for parallax effect
     */
    function handleMouseMove(event) {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        // Store mouse position for animation frame
        state.lastMousePosition = {
            x: event.clientX,
            y: event.clientY
        };

        // Use requestAnimationFrame for smooth animations
        if (!state.lastAnimationFrame) {
            state.lastAnimationFrame = window.requestAnimationFrame(updateParallax);
        }
    }

    /**
     * Update parallax effect based on mouse position
     */
    function updateParallax() {
        const centerX = state.windowSize.width / 2;
        const centerY = state.windowSize.height / 2;
        
        // Calculate normalized position (-1 to 1)
        const posX = (state.lastMousePosition.x - centerX) / centerX;
        const posY = (state.lastMousePosition.y - centerY) / centerY;

        menuItems.forEach(item => {
            if (!item.img) return;
            
            // Calculate movement with bounds checking
            const moveX = Math.min(Math.max(posX * item.speed * 20, -CONFIG.maxParallaxOffset), CONFIG.maxParallaxOffset);
            const moveY = Math.min(Math.max(posY * item.speed * 20, -CONFIG.maxParallaxOffset), CONFIG.maxParallaxOffset);
            
            // Apply transform with hardware acceleration
            item.img.style.transform = `translate3d(${moveX}px, ${moveY}px, 0) scale(1.1)`;
        });

        state.lastAnimationFrame = null;
    }

    /**
     * Handle window resize
     */
    function handleResize() {
        state.windowSize = {
            width: window.innerWidth,
            height: window.innerHeight
        };
        updateElementBounds();
    }

    /**
     * Update element bounds for better performance
     */
    function updateElementBounds() {
        menuItems.forEach(item => {
            if (item.element) {
                item.bounds = item.element.getBoundingClientRect();
            }
        });
    }

    /**
     * Handle menu item clicks
     */
    function handleMenuItemClick(event) {
        event.preventDefault();
        
        // Get the text content safely
        const textElement = this.querySelector('span');
        const menuText = textElement ? textElement.textContent.trim().toLowerCase() : 'unknown';
        
        try {
            // Add your navigation logic here
            console.log(`Navigating to: ${menuText}`);
            
            // Example: window.location.href = `/${menuText}`;
            
        } catch (error) {
            console.error('Navigation error:', error);
            // Fallback behavior
            window.location.href = '/';
        }
    }

    /**
     * Handle keyboard navigation
     */
    function handleKeyDown(event) {
        // Handle Enter or Space key
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            this.click();
        }
    }

    /**
     * Handle image loading errors
     */
    function handleImageError(event) {
        const img = event.target;
        const parent = img.closest('.menu-item');
        
        if (parent) {
            parent.classList.remove('loading');
            parent.classList.add('error');
            
            // Set a fallback background color
            parent.style.background = '#f0f0f0';
            
            // Add error message for screen readers
            const errorMessage = document.createElement('span');
            errorMessage.className = 'sr-only';
            errorMessage.textContent = 'Error loading image';
            parent.appendChild(errorMessage);
        }
    }

    /**
     * Handle reduced motion preference
     */
    function handleMotionPreference(mediaQuery) {
        if (mediaQuery.matches) {
            document.documentElement.classList.add('reduced-motion');
        } else {
            document.documentElement.classList.remove('reduced-motion');
        }
    }

    /**
     * Debounce function for performance
     */
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }

    /**
     * Clean up event listeners and animations
     */
    function cleanup() {
        // Cancel any pending animation frame
        if (state.lastAnimationFrame) {
            window.cancelAnimationFrame(state.lastAnimationFrame);
            state.lastAnimationFrame = null;
        }
        
        // Remove event listeners
        window.removeEventListener('resize', handleResize);
        window.removeEventListener('orientationchange', handleResize);
        document.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('beforeunload', cleanup);
        
        // Clean up menu item event listeners
        menuItems.forEach(item => {
            if (item.element) {
                item.element.removeEventListener('click', handleMenuItemClick);
                item.element.removeEventListener('keydown', handleKeyDown);
            }
            if (item.img) {
                item.img.removeEventListener('error', handleImageError);
            }
        });
    }

    // Initialize when DOM is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOMContentLoaded has already fired
        init();
    }

    // Expose public API (if needed)
    window.menuController = {
        init,
        cleanup,
        updateElementBounds
    };

})();
