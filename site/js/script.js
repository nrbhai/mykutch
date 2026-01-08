// Set slower playback for hero background video
const heroVideo = document.querySelector('.hero-video');
if (heroVideo) {
  heroVideo.playbackRate = 0.5; // half speed
}

// Mobile Menu Toggle
const mobileToggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileToggle.innerText = navLinks.classList.contains('active') ? '✕' : '☰';
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileToggle.innerText = '☰';
        });
    });
}


// Staggered Reveal Animation
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            // Add a small delay for staggered effect if requested
            const delay = entry.target.dataset.delay || 0;
            setTimeout(() => {
                entry.target.classList.add('active');
            }, delay);
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Initialize reveals
document.querySelectorAll('.reveal, .card, .section-title, .essential-item').forEach((el, index) => {
    // Auto-stagger cards in a grid
    if (el.classList.contains('card')) {
        el.dataset.delay = (index % 3) * 150;
    }
    el.classList.add('reveal');
    observer.observe(el);
});

// Smooth Scroll (Native behavior is set in CSS, but this handles edge cases)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (nav) {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
});

// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
const darkModeIcon = document.getElementById('darkModeIcon');
const html = document.documentElement;

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', currentTheme);
updateDarkModeIcon(currentTheme);

// Toggle dark mode
if (darkModeToggle) {
    darkModeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateDarkModeIcon(newTheme);
    });
}

function updateDarkModeIcon(theme) {
    if (darkModeIcon) {
        darkModeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// Preloader Logic
window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        // rapid fade out once everything (images + content) is ready
        setTimeout(() => {
            preloader.classList.add('hidden');
        }, 100); // small buffer to ensure visual smoothness
    }
});
