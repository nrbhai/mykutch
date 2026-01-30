/**
 * Simple client-side i18n script
 * - Detects language from localStorage or navigator
 * - Fetches properties file (JSON)
 * - Updates DOM elements with data-i18n attribute
 */

const supportedLanguages = ['en', 'hi', 'de', 'fr', 'es', 'ru'];
const defaultLanguage = 'en';

function getInitialLanguage() {
    const savedLang = localStorage.getItem('site-lang');
    if (savedLang && supportedLanguages.includes(savedLang)) {
        return savedLang;
    }
    const userLang = navigator.language.slice(0, 2);
    return supportedLanguages.includes(userLang) ? userLang : defaultLanguage;
}

async function loadLanguage(lang) {
    // Check for local file protocol usage which blocks fetch
    if (window.location.protocol === 'file:') {
        alert("Note: Multilingual support (JSON loading) requires a local web server (like Live Server) due to browser security restrictions on 'file://' paths. Content may not appear otherwise.");
    }

    // Determine correct path to lang directory
    // If we are deep in /destinations/, we need ../lang/
    // If we are at root /site/, we need ./lang/
    const isRoot = !window.location.pathname.includes('/destinations/') && !window.location.pathname.includes('/crafts/'); // Simple specific check for now
    const pathPrefix = isRoot ? 'lang/' : '../lang/';

    try {
        const response = await fetch(`${pathPrefix}${lang}.json`);
        if (!response.ok) {
            throw new Error(`Could not load ${lang}.json`);
        }
        return await response.json();
    } catch (e) {
        console.error('Error loading language:', e);
        // Fallback to English if load fails
        if (lang !== 'en') {
            console.log('Falling back to English');
            return loadLanguage('en');
        }
        return null;
    }
}

function applyTranslations(translations) {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const keys = key.split('.');
        let value = translations;
        
        // Traverse nested keys if any (e.g. bhuj.hero_title)
        for (const k of keys) {
            if (value && value[k] !== undefined) {
                value = value[k];
            } else {
                value = null;
                break;
            }
        }

        if (value) {
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = value;
            } else if (element.tagName === 'IMG') {
                element.alt = value;
            } else if (element.tagName === 'META') {
                element.setAttribute('content', value);
            } else {
                element.innerHTML = value; // Use innerHTML to allow basic tags like <strong>
            }
        } else {
            console.warn(`Missing translation for key: ${key}`);
        }
    });

    // Update specific attributes if needed (like meta tags)
    // This requires specific data-i18n directives or structure
}

async function initOneTime() {
    const currentLang = getInitialLanguage();
    // Set HTML lang attribute
    document.documentElement.lang = currentLang;
    
    // Create UI for switching (Simple selector injected for testing/usage)
    if (!document.getElementById('lang-switcher')) {
        const switcher = document.createElement('div');
        switcher.id = 'lang-switcher';
        switcher.style.position = 'fixed';
        switcher.style.bottom = '20px';
        switcher.style.right = '20px';
        switcher.style.zIndex = '9999';
        switcher.style.background = 'rgba(0,0,0,0.8)';
        switcher.style.padding = '10px';
        switcher.style.borderRadius = '5px';
        
        // Build option list
        let selectHtml = `<select id="lang-select" style="background:#333; color:white; border:1px solid #555; padding:5px;">`;
        supportedLanguages.forEach(l => {
            selectHtml += `<option value="${l}" ${l === currentLang ? 'selected' : ''}>${l.toUpperCase()}</option>`;
        });
        selectHtml += `</select>`;
        
        switcher.innerHTML = selectHtml;
        document.body.appendChild(switcher);

        document.getElementById('lang-select').addEventListener('change', (e) => {
            const newLang = e.target.value;
            localStorage.setItem('site-lang', newLang);
            window.location.reload(); 
        });
    }

    const translations = await loadLanguage(currentLang);
    if (translations) {
        applyTranslations(translations);
    }
}

// Run when DOM is ready
document.addEventListener('DOMContentLoaded', initOneTime);
