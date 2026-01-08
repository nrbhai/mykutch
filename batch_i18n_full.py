
import json
import os
import re

# Base paths
BASE_DIR = r"c:\website_project\mykutch\site"
LANG_DIR = os.path.join(BASE_DIR, "lang")
DEST_DIR = os.path.join(BASE_DIR, "destinations")

# Standardized Footer Helper
STANDARD_FOOTER = """<footer class="footer-main" style="margin-top: 2rem; background: linear-gradient(135deg, #F8FAFC, #E0F2FE, #BAE6FD); color: var(--color-heading); padding: 2.5rem 0; border-top: 1px solid rgba(0,0,0,0.05);">
        <div class="container">
            <div style="max-width: 900px; margin: 0 auto; text-align: center;">
                <img src="../assets/images/logo.png" alt="MyKutch Logo" style="height: 130px; margin-bottom: 1rem; opacity: 0.9;">
                <h3 style="color: var(--color-heading); font-family: var(--font-heading); margin-bottom: 0.5rem; font-size: 1.1rem; letter-spacing: 0.05em;" data-i18n="footer.about_title"></h3>
                <p style="opacity: 0.8; line-height: 1.4; margin-bottom: 1rem; font-size: 0.9rem; max-width: 600px; margin-left: auto; margin-right: auto;" data-i18n="footer.about_text"></p>
                <div style="display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                    <div style="font-size: 0.85rem;">
                        <span style="opacity: 0.7; margin-right: 0.3rem;" data-i18n="footer.contact_label"></span>
                        <a href="tel:9825034580" style="color: var(--color-primary); text-decoration: none; font-weight: 600;">+91 98250 34580</a>
                    </div>
                    <div style="font-size: 0.85rem;">
                        <span style="opacity: 0.7; margin-right: 0.3rem;" data-i18n="footer.email_label"></span>
                        <a href="mailto:info@mykutch.org" style="color: var(--color-primary); text-decoration: none; font-weight: 600;">info@mykutch.org</a>
                    </div>
                </div>
                <div style="border-top: 1px solid rgba(0,0,0,0.05); padding-top: 1rem; font-size: 0.8rem; font-weight: 500; opacity: 0.6;">
                    <p data-i18n="footer.dev_credit"></p>
                </div>
            </div>
        </div>
    </footer>"""

# Content configuration for internationalization
PAGES_CONFIG = {
    "kadia_dhrow": {
        "file": "kadia-dhrow.html",
        "content": {
            "hero_title": { "en": "Kadia Dhro — The Grand Canyon of India", "hi": "Kadia Dhro — The Grand Canyon of India" },
            "lead_text": {
                "en": "Kadia Dhro \(or Kadiya Dhrow\) is Kutch's most spectacular hidden gem.*nature lovers\.", 
                "en_full": "Kadia Dhro (or Kadiya Dhrow) is Kutch's most spectacular hidden gem, often called the 'Grand Canyon of India'. This geological marvel features stunning multi-colored rock formations carved by wind and water over centuries. The riverbed displays vibrant bands of red, yellow, and orange sandstone, creating a surreal landscape that looks like a painting come to life. Once an obscure spot, it is now a must-visit for nature lovers.",
                "hi": "कड़िया ध्रो (या कड़िया ध्रोव) कच्छ का सबसे शानदार छिपा हुआ रत्न है, जिसे अक्सर 'भारत का ग्रैंड कैनियन' कहा जाता है। इस भूवैज्ञानिक चमत्कार में सदियों से हवा और पानी द्वारा तराशी गई शानदार बहुरंगी चट्टानें हैं। नदी के तल में लाल, पीले और नारंगी बलुआ पत्थर के जीवंत बैंड दिखाई देते हैं, जो एक अतिरेक परिदृश्य (surreal landscape) बनाते हैं जो एक पेंटिंग के जीवन में आने जैसा दिखता है।"
            },
            "who_title": { "en": "Who Should Visit", "hi": "Who Should Visit" },
            "who_photographers": { "en": "<strong>Photographers</strong>: For the dramatic colors and rock textures .*Sunrise/Sunset\)\.", "hi": "<strong>Photographers</strong>: नाटकीय रंगों और रॉक टेक्सचर के लिए (सूर्योदय/सूर्यास्त पर सबसे अच्छी रोशनी)।" },
            "who_hikers": { "en": "<strong>Hikers & Explorers</strong>: Requires a bit of walking on uneven rocky terrain\.", "hi": "<strong>Hikers & Explorers</strong>: असमान पथरीले इलाके में थोड़ा चलने की आवश्यकता है।" },
            "who_geology": { "en": "<strong>Geology Enthusiasts</strong>: To study the unique Jurassic-era sedimentary rock.*", "hi": "<strong>Geology Enthusiasts</strong>: अद्वितीय जुरासिक-युग की तलछटी चट्टान परतों (sedimentary rock layers) का अध्ययन करने के लिए।" },
            "who_note": { "en": "<strong>Note</strong>: NOT suitable for elderly or those with mobility issues.*", "hi": "<strong>Note</strong>: ऊबड़-खाबड़ इलाका होने के कारण बुजुर्गों या चलने-फिरने में असमर्थ लोगों के लिए उपयुक्त नहीं है।" },
            
            "how_to_reach_title": { "en": "How to Reach", "hi": "How to Reach" },
            "reach_bhuj": { "en": "<strong>From Bhuj</strong>: Approx 45km\. Best reached by private taxi or rental bike\.", "hi": "<strong>From Bhuj</strong>: लगभग 45 किमी। निजी टैक्सी या किराए की बाइक से सबसे अच्छा पहुँचा जा सकता है।" },
            "reach_road": { "en": "<strong>Road Condition</strong>: The last few kilometers are off-road\. Drive carefully\.", "hi": "<strong>Road Condition</strong>: आखिरी कुछ किलोमीटर ऑफ-रोड हैं। सावधानी से गाड़ी चलाएं।" },

            "landmark_title": { "en": "Landmarks & Heritage", "hi": "Landmarks & Heritage" },
            "landmark_subtitle": { "en": "The defining monuments", "hi": "परिभाषित स्मारक" },
            "canyon_hike_title": { "en": "Canyon Hike", "hi": "Canyon Hike" },
            "canyon_hike_desc": { "en": "\(1-2 Hours\) Walk down into the riverbed.*", "hi": "(1-2 घंटे) नीचे से विशाल रॉक स्तंभों को देखने के लिए नदी के तल में चलें (यदि सूखा हो)।" },
            "photo_title": { "en": "Photography", "hi": "Photography" },
            "photo_desc": { "en": "Climb the small cliffs for a panoramic top-down shot.*", "hi": "रंगीन बैंड के मनोरम टॉप-डाउन शॉट के लिए छोटी चट्टानों पर चढ़ें।" },
            "croc_title": { "en": "Crocodile Spotting", "hi": "Crocodile Spotting" },
            "croc_desc": { "en": "Be careful! Freshwater crocodiles live.*", "hi": "सावधान रहें! नदी के गहरे पानी के कुंडों में मीठे पानी के मगरमच्छ रहते हैं।" },
            "sunset_title": { "en": "Sunset View", "hi": "Sunset View" },
            "sunset_desc": { "en": "The rocks glow golden-red during the evening.*", "hi": "शाम के सुनहरे समय (golden hour) के दौरान चट्टानें सुनहरी-लाल चमकती हैं।" },
            
            "tips_title": { "en": "Curated Local Advice", "hi": "Curated Local Advice" },
            "tip_facilities_title": { "en": "No Facilities", "hi": "No Facilities" },
            "tip_facilities_desc": { "en": "There are ZERO shops, toilets, or water stalls.*", "hi": "यहाँ कोई दुकानें, शौचालय या पानी के स्टॉल नहीं हैं। अपनी ज़रूरत का सब कुछ साथ ले जाएँ।" },
            
            "shopping_title": {"en": "Shopping & Bazaars", "hi": "Shopping & Bazaars"},
            "shopping_check": { "en": "Check local guides for shopping\.", "hi": "खरीदारी-विवरण (shopping info) जल्द ही अपडेट किया जाएगा।" },
            "eats_title": {"en": "Local Eats", "hi": "Local Eats"},
            "eats_check": { "en": "Check local guides for food\.", "hi": "भोजन-विवरण (food info) जल्द ही अपडेट किया जाएगा।" },

            "when_title": { "en": "When to Visit", "hi": "When to Visit" },
            "when_desc": { "en": "<strong>November to February:</strong> Best weather for hiking.*", "hi": "<strong>November to February:</strong> लंबी पैदल यात्रा के लिए सबसे अच्छा मौसम। <br><br><strong>Monsoon (July-Sept):</strong> परिदृश्य हरा-भरा होता है और नदी बहती है, लेकिन एप्रोच रोड बहुत कीचड़युक्त हो जाती है।" },
            
            "itinerary_title": { "en": "Suggested Itinerary", "hi": "Suggested Itinerary" },
            "day_7am": { "en": "00 AM: Depart from Bhuj with packed breakfast\.", "hi": "00 AM: पैक्ड नाश्ते के साथ भुज से प्रस्थान करें।" },
            "day_8am": { "en": "00 AM: Reach Kadia Dhro\. Park safely\.", "hi": "00 AM: कड़िया ध्रो पहुँचें। सुरक्षित पार्क करें।" },
            "day_815am": { "en": "15 AM - 10:30 AM: Hike, explore, and photography\.", "hi": "15 AM - 10:30 AM: हाइक, एक्सप्लोर और फोटोग्राफी।" },
            "day_11am": { "en": "00 AM: Visit nearby Rakhal Van.*", "hi": "00 AM: यदि समय मिले तो पास के रखाल वन (आरक्षित वन) जाएँ।" },
            "day_1230pm": { "en": "30 PM: Return to Bhuj for lunch\.", "hi": "30 PM: दोपहर के भोजन के लिए भुज वापस लौटना।" },
            "nearby_title": { "en": "Nearby Places to Visit", "hi": "Nearby Places to Visit" },
            "nearby_bhuj_desc": { "en": "\(45km\) The base city\.", "hi": "(45km) मुख्य शहर (The base city)।" },
            "nearby_rann_desc": { "en": "\(80km\) Can be done on the same day.*", "hi": "(80km) यदि आप बहुत जल्दी शुरुआत करें तो उसी दिन किया जा सकता है।" }
        }
    },
    "mandvi": {
        "file": "mandvi.html",
        "content": {
            # Only adding missing items or core items here, previously covered but verifying
            "hero_title": { "en": "Mandvi — Where the Desert Meets the Sea", "hi": "Mandvi — Where the Desert Meets the Sea" },
             "lead_text": {
                "en": "Mandvi is the only premier beach destination in Kutch.*White Rann\.",
                "en_full": "Mandvi is the only premier beach destination in Kutch, offering a perfect relaxed break from the arid desert landscape. Once a major port for the spice trade, it is now a popular day-trip and weekend getaway from Bhuj (1 hour away). Known for its pristine beaches, the royal Vijay Vilas Palace, and a 400-year-old shipbuilding tradition, Mandvi is where history meets the Arabian Sea. A typical visit lasts 1 to 2 days, making it ideal for unwinding after exploring the White Rann.",
                "hi": "मांडवी कच्छ का एकमात्र प्रमुख बीच डेस्टिनेशन है, जो शुष्क रेगिस्तानी परिदृश्य से एक आदर्श आरामदायक ब्रेक प्रदान करता है। कभी मसाला व्यापार के लिए एक प्रमुख बंदरगाह, अब यह भुज (1 घंटे दूर) से एक लोकप्रिय डे-ट्रिप और वीकेंड गेटअवे है। अपने साफ समुद्र तटों, शाही विजय विलास पैलेस और 400 साल पुरानी जहाज निर्माण परंपरा के लिए जाना जाने वाला, मांडवी वह जगह है जहाँ इतिहास अरब सागर से मिलता है। एक सामान्य यात्रा 1 से 2 दिनों तक चलती है, जो इसे व्हाइट रण की खोज के बाद आराम करने के लिए आदर्श बनाती है।"
            },
            "landmark_title": { "en": "Landmarks & Heritage", "hi": "Landmarks & Heritage" },
            "shopping_title": {"en": "Shopping & Bazaars", "hi": "Shopping & Bazaars"},
             # NOTE: Mandvi has actual shopping list? Check HTML. Assuming plain list if present.
             "eats_title": {"en": "Local Eats", "hi": "Local Eats"}, 
             "when_title": { "en": "When to Visit", "hi": "When to Visit" },
             "itinerary_title": { "en": "Suggested Itinerary", "hi": "Suggested Itinerary" },
             "tip_timing_title": {"en": "Timing", "hi": "Timing"},
             "tip_timing_desc": {"en": "Don't visit the beach at noon.*", "hi": "दोपहर (12-3 PM) में बीच पर न जाएँ; बहुत गर्मी होती है। सुबह और शाम सबसे अच्छे हैं।"}
        }
    }
}

def update_json(lang_file, key_prefix, data, lang_code):
    with open(lang_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    keys = key_prefix.split('.')
    current = json_data
    for k in keys:
        if k not in current:
            current[k] = {}
        current = current[k]
    for k, v in data.items():
        if lang_code == 'en':
            if isinstance(v, dict) and "en_full" in v:
                current[k] = v["en_full"]
            elif isinstance(v, dict) and "en" in v:
                clean_text = v["en"].strip().replace("\\(", "(").replace("\\)", ")").replace(".*", "").replace("\\.", ".")
                # Remove regex chars
                current[k] = clean_text
        elif lang_code == 'hi':
             if isinstance(v, dict) and "hi" in v:
                current[k] = v["hi"]
    with open(lang_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"Updated {lang_file} for {key_prefix}")

def process_file(page_key):
    config = PAGES_CONFIG[page_key]
    file_path = os.path.join(DEST_DIR, config["file"])
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Update JSONs
    update_json(os.path.join(LANG_DIR, "en.json"), f"destinations.{page_key}", config["content"], "en")
    update_json(os.path.join(LANG_DIR, "hi.json"), f"destinations.{page_key}", config["content"], "hi")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    
    # Process translations
    for key, val_map in config["content"].items():
        en_pattern = val_map.get("en", "")
        if not en_pattern: continue
        
        # Regex logic:
        # If the pattern contains regex specifics like .* or \( or \), we assume it is already a ready-to-use regex.
        # Otherwise, we escape it to treat it as literal text.
        if ".*" in en_pattern or "\\(" in en_pattern or "\\[" in en_pattern:
             pattern_escaped = en_pattern
        else:
             pattern_escaped = re.escape(en_pattern)
        
        # We need to robustly match content that might span lines or have extra whitespace
        # (<[^>]+>) captures the opening tag.
        # \s* matches potential whitespace after tag closes
        # ({pattern_escaped}) captures the content we want to match
        # \s* matches potential whitespace before closing tag
        # (</[^>]+>) captures closing tag
        
        full_regex = f"(<[^>]+)(>)\\s*({pattern_escaped})\\s*(</[^>]+>)"
        
        i18n_key = f"destinations.{page_key}.{key}"
        
        def replacement(match):
            tag_open = match.group(1)
            tag_close_bracket = match.group(2)
            inner_text = match.group(3)
            tag_close = match.group(4)
            
            # Clean up existing data-i18n if present
            tag_open_clean = re.sub(r'\s*data-i18n="[^"]*"', '', tag_open)
            
            # Reconstruct with single data-i18n
            return f'{tag_open_clean} data-i18n="{i18n_key}"{tag_close_bracket}{inner_text}{tag_close}'

        # Apply strictly with DOTALL to catch newlines
        new_content = re.sub(full_regex, replacement, new_content, count=1, flags=re.DOTALL)

    # 2. Cleanup Multiple attributes if any crept in (Quick fix)
    # This regex looks for (data-i18n="...") ... (data-i18n="...") 
    # and removes subsequent ones? Hard to do reliably with regex. 
    # The replacement logic above cleans standard cases.

    # 3. Footer Replacement
    # Find existing footer
    footer_regex = r'<footer class="footer-main".*?</footer>'
    if re.search(footer_regex, new_content, re.DOTALL):
        new_content = re.sub(footer_regex, STANDARD_FOOTER, new_content, flags=re.DOTALL)
        print("Replaced Footer")

    # 4. Inject i18n.js
    if 'src="../js/i18n.js"' not in new_content:
        if 'src="../js/script.js"' in new_content:
            new_content = new_content.replace('<script src="../js/script.js"></script>', '<script src="../js/i18n.js"></script>\n    <script src="../js/script.js"></script>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated HTML file {file_path}")

if __name__ == "__main__":
    process_file("kadia_dhrow")
    process_file("mandvi")
