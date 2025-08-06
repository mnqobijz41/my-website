// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    if (hamburger && navMenu) {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }
}));

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (header) {
        const currentTheme = document.body.getAttribute('data-theme');
        
        if (window.scrollY > 100) {
            if (currentTheme === 'dark') {
                header.style.background = 'rgba(10, 10, 10, 0.98)';
                header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.5)';
            } else {
                header.style.background = 'rgba(255, 255, 255, 0.98)';
                header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            }
        } else {
            if (currentTheme === 'dark') {
                header.style.background = 'rgba(10, 10, 10, 0.95)';
                header.style.boxShadow = 'none';
            } else {
                header.style.background = 'rgba(255, 255, 255, 0.95)';
                header.style.boxShadow = 'none';
            }
        }
    }
});

// Theme Toggle Functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const body = document.body;

    if (!themeToggle || !themeIcon) {
        console.log('Theme toggle elements not found');
        return;
    }

    // Get saved theme or default to light
    const savedTheme = localStorage.getItem('theme');
    const currentTheme = savedTheme || 'light';
    
    // Set the theme
    body.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme, themeIcon);
    updateHeaderBackground(currentTheme);
    
    console.log('Initial theme set to:', currentTheme);

    // Remove any existing event listeners to prevent duplicates
    themeToggle.removeEventListener('click', handleThemeToggle);
    
    // Theme toggle click handler
    themeToggle.addEventListener('click', handleThemeToggle);
}

// Separate function for theme toggle handling
function handleThemeToggle() {
    console.log('Theme toggle clicked!');
    
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    console.log('Toggling theme from', currentTheme, 'to', newTheme);
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme, themeIcon);
    updateHeaderBackground(newTheme);
    
    console.log('Theme changed to:', newTheme);
    
    // Debug the new state
    setTimeout(() => {
        debugThemeState();
    }, 100);
}

// Update header background based on theme
function updateHeaderBackground(theme) {
    const header = document.querySelector('.header');
    if (header) {
        if (theme === 'dark') {
            header.style.background = 'rgba(10, 10, 10, 0.95)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    }
}

// Update theme icon based on current theme
function updateThemeIcon(theme, themeIcon) {
    if (!themeIcon) {
        console.log('Theme icon element not found');
        return;
    }
    
    if (theme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        console.log('Icon set to sun (dark mode active)');
    } else {
        themeIcon.className = 'fas fa-moon';
        console.log('Icon set to moon (light mode active)');
    }
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Ensure light mode is default if no theme is set
    if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', 'light');
    }
    
    initializeThemeToggle();
    console.log('MNQOBI LISBON JEZA - Personal Website loaded successfully!');
});

// Also initialize immediately in case DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!localStorage.getItem('theme')) {
            localStorage.setItem('theme', 'light');
        }
        initializeThemeToggle();
    });
} else {
    if (!localStorage.getItem('theme')) {
        localStorage.setItem('theme', 'light');
    }
    initializeThemeToggle();
}

// Function to reset theme to light mode (for debugging)
function resetToLightMode() {
    localStorage.setItem('theme', 'light');
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    body.setAttribute('data-theme', 'light');
    updateThemeIcon('light', themeIcon);
    updateHeaderBackground('light');
    
    console.log('Theme reset to light mode');
}

// Uncomment the line below to force light mode (for testing)
// resetToLightMode();

// Function to sync theme state across all pages
function syncThemeState() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme, themeIcon);
    updateHeaderBackground(savedTheme);
    
    console.log('Theme state synced to:', savedTheme);
}

// Add this to test the theme toggle
console.log('Current theme:', localStorage.getItem('theme'));
console.log('Body data-theme:', document.body.getAttribute('data-theme'));

// Sync theme state on page load
syncThemeState();

// Debug function to check current theme state
function debugThemeState() {
    const savedTheme = localStorage.getItem('theme');
    const bodyTheme = document.body.getAttribute('data-theme');
    const themeIcon = document.getElementById('themeIcon');
    const iconClass = themeIcon ? themeIcon.className : 'not found';
    
    console.log('=== Theme Debug Info ===');
    console.log('Saved theme:', savedTheme);
    console.log('Body theme:', bodyTheme);
    console.log('Icon class:', iconClass);
    console.log('Icon element found:', !!themeIcon);
    console.log('========================');
}

// Run debug on page load
debugThemeState();

// Analytics Tracking
function trackPageView(pageName) {
    // Only track if we're running on the analytics server
    if (window.location.hostname === 'localhost' && window.location.port === '5000') {
        fetch('/api/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                page: pageName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('📊 Page view tracked:', pageName);
            }
        })
        .catch(error => {
            console.log('📊 Analytics not available (normal for local development)');
        });
    }
}

// Track page views on page load
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    trackPageView(currentPage);
});

// Track page views on navigation (for SPA-like behavior)
window.addEventListener('popstate', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    trackPageView(currentPage);
});
