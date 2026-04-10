// Mobile Menu Toggle
const mobileToggle = document.querySelector('.mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileToggle && navLinks) {
    // Ensure nav is addressable by assistive tech
    if (!navLinks.id) {
        navLinks.id = 'primary-nav';
    }
    mobileToggle.setAttribute('aria-controls', navLinks.id);
    mobileToggle.setAttribute('aria-expanded', 'false');
    navLinks.setAttribute('aria-hidden', 'true');

    const updateMenuState = (isOpen) => {
        mobileToggle.setAttribute('aria-expanded', String(isOpen));
        navLinks.setAttribute('aria-hidden', String(!isOpen));
        mobileToggle.innerText = isOpen ? '✕' : '☰';
    };

    mobileToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('active');
        updateMenuState(isOpen);
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            updateMenuState(false);
        });
    });

    // Close menu on Escape
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            updateMenuState(false);
            mobileToggle.focus();
        }
    });
}


// Staggered Reveal Animation
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const supportsIntersectionObserver = 'IntersectionObserver' in window;

if (!prefersReducedMotion && supportsIntersectionObserver) {
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
} else {
    document.querySelectorAll('.reveal, .card, .section-title, .essential-item').forEach((el) => {
        el.classList.add('active');
    });
}

// Smooth Scroll (Native behavior is set in CSS, but this handles edge cases)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: prefersReducedMotion ? 'auto' : 'smooth'
                });
            }
        }
    });
});

// Gallery Image Fallback (for browsers/devices where some images fail to decode)
const applyGalleryImageFallbacks = () => {
    document.querySelectorAll('.gallery-grid img').forEach((img) => {
        if (img.dataset.galleryFallbackBound === 'true') {
            return;
        }

        img.dataset.galleryFallbackBound = 'true';
        img.addEventListener('error', () => {
            const wrapper = document.createElement('div');
            wrapper.style.display = 'flex';
            wrapper.style.alignItems = 'center';
            wrapper.style.justifyContent = 'center';
            wrapper.style.minHeight = '180px';
            wrapper.style.borderRadius = '0.75rem';
            wrapper.style.background = '#f3f4f6';
            wrapper.style.color = '#6b7280';
            wrapper.style.fontSize = '0.9rem';
            wrapper.textContent = 'Image unavailable on this device';

            if (img.parentNode) {
                img.parentNode.insertBefore(wrapper, img);
                img.remove();
            }
        }, { once: true });
    });
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyGalleryImageFallbacks);
} else {
    applyGalleryImageFallbacks();
}

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

// Swap legacy logo assets to new logo in navbar/footer
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const isRoot = !path.includes('/destinations/') && !path.includes('/crafts/') && !path.includes('/hidden-gems/');
    const assetPrefix = isRoot ? 'assets/' : '../assets/';
    const pagePrefix = isRoot ? '' : '../';
    const newLogo = `${assetPrefix}images/newlogo.png`;
    const absoluteLogo = `${window.location.origin}/assets/images/newlogo.png`;

    const navLists = Array.from(document.querySelectorAll('.nav-links'));
    const primaryNav = document.querySelector('nav .nav-links') || navLists[0];
    navLists.forEach((nav) => {
        if (nav !== primaryNav) {
            nav.remove();
        }
    });

    const footerBlocks = Array.from(document.querySelectorAll('footer.footer-main'));
    if (footerBlocks.length > 1) {
        footerBlocks.forEach((footer, index) => {
            if (index !== footerBlocks.length - 1) {
                footer.remove();
            }
        });
    }

    document.querySelectorAll('img.nav-logo, img[src*="/logo.png"], img[src*="logo.png"]').forEach((img) => {
        img.src = newLogo;
    });

    document.querySelectorAll('meta[property="og:image"], meta[name="twitter:image"]').forEach((meta) => {
        if ((meta.content || '').includes('logo.png')) {
            meta.content = absoluteLogo;
        }
    });

    document.querySelectorAll('link[rel*="icon"]').forEach((link) => {
        if ((link.href || '').includes('logo.png')) {
            link.href = absoluteLogo;
        }
    });

    const footer = document.querySelector('footer.footer-main');
    if (footer) {
        footer.innerHTML = `
            <div class="container">
                <!-- Large Transparent Watermark Logo -->
                <img src="${newLogo}" alt="" class="footer-watermark-bg"/>
                <div class="footer-inner">
                    <div class="footer-brand">
                        <img alt="MyKutch.org" class="footer-logo" src="${newLogo}"/>
                        <p class="footer-tagline">Beyond the endless White Rann lies a land of hidden caves, pristine seashores, and sacred hills. Discover the untold stories of Kutch.</p>
                    </div>
                    
                    <div class="footer-links">
                        <h4 data-i18n="footer.quick_links">Quick Links</h4>
                        <ul>
                            <li><a href="${pagePrefix}geography.html" data-i18n="nav.geography">Geography</a></li>
                            <li><a href="${pagePrefix}crafts.html" data-i18n="nav.crafts">Crafts</a></li>
                            <li><a href="${pagePrefix}distance-matrix.html" data-i18n="nav.distance">Distance Matrix</a></li>
                            <li><a href="${pagePrefix}landscapes.html" data-i18n="nav.landscapes">Landscapes</a></li>
                            <li><a href="${pagePrefix}bookings.html" data-i18n="nav.bookings">Bookings</a></li>
                            <li><a href="${pagePrefix}about.html" data-i18n="nav.about">About</a></li>
                        </ul>
                    </div>

                    <div class="footer-contact">
                        <div class="footer-contact-item">
                            <span data-i18n="footer.contact_label">Contact:</span>
                            <a href="tel:9825034580">+91 98250 34580</a>
                        </div>
                        <div class="footer-contact-item">
                            <span data-i18n="footer.email_label">Email:</span>
                            <a href="mailto:info@mykutch.org">info@mykutch.org</a>
                        </div>
                    </div>
                </div>
                <div class="footer-bottom">
                    <span data-i18n="footer.developed_by">Developed with Love for Kutch by MyKutch.org team</span>
                </div>
            </div>
        `;
    }
});

/**
 * Lightbox Gallery System (Enhanced)
 * Enables full-screen view for all gallery-capable images across the site.
 * Targets: Landscapes, Destinations, Hidden Gems, Crafts, and Featured Cards.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Select all relevant images that should trigger a full view
    const galleryItems = document.querySelectorAll(`
        .photo-card img, 
        .card-img-wrapper img, 
        .attraction-img-wrapper img, 
        .craft-img,
        .attraction-card img,
        .card img
    `);
    
    if (galleryItems.length === 0) return;

    // Create Lightbox Overlay Elements
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.innerHTML = `
        <button class="lightbox-close" aria-label="Close Viewer">&times;</button>
        <img class="lightbox-content" src="" alt="Full size gallery image">
        <div class="lightbox-caption"></div>
    `;
    document.body.appendChild(lightbox);

    const lightboxImg = lightbox.querySelector('.lightbox-content');
    const lightboxCaption = lightbox.querySelector('.lightbox-caption');
    const closeBtn = lightbox.querySelector('.lightbox-close');

    // Function to open the lightbox
    const openLightbox = (imgSrc, alt, caption) => {
        lightboxImg.src = imgSrc;
        lightboxImg.alt = alt;
        lightboxCaption.textContent = caption;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    // Close on click or button
    const closeLightbox = () => {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => { 
            if (!lightbox.classList.contains('active')) lightboxImg.src = ''; 
        }, 300);
    };

    galleryItems.forEach(img => {
        // We attach the listener to the image itself
        img.addEventListener('click', (e) => {
            // Priority: If user clicks the image, we show the lightbox
            // Even if the image is inside an <a>, we intercept to show the full photo
            if (img.closest('a')) {
                // If the user specifically wanted to navigate, they'd usually click the text/button
                // but since the image is a main eye-catcher, we prioritize full view here
                e.preventDefault();
                e.stopPropagation();
            }

            // Determine appropriate caption (from figcaption, H3, or alt text)
            const parent = img.closest('.photo-card, .card, .attraction-card, .craft-card');
            const caption = parent?.querySelector('figcaption, h3, .attraction-title, .card-title')?.textContent || img.alt || 'Gallery Image';
            
            openLightbox(img.src, img.alt, caption.trim());
        });
    });

    closeBtn.addEventListener('click', closeLightbox);
    
    // Close on overlay click
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) closeLightbox();
    });

    // Close on Escape Key (Accessibility)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('active')) {
            closeLightbox();
        }
    });
});

