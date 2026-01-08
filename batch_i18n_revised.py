
import json
import os
import re

# Base paths
BASE_DIR = r"c:\website_project\mykutch\site"
LANG_DIR = os.path.join(BASE_DIR, "lang")
DEST_DIR = os.path.join(BASE_DIR, "destinations")

# Content configuration for internationalization
PAGES_CONFIG = {
    "kadia_dhrow": {
        "file": "kadia-dhrow.html",
        "content": {
            "hero_title": {
                "en": "Kadia Dhro — The Grand Canyon of India",
                "hi": "The Grand Canyon of India"
            },
            # lead_text already manually fixed in HTML, so we don't need to try matching its old content again necessarily,
            # but keeping it in JSON config ensures the keys are preserved in hi.json/en.json if we re-run.
            # However, the script tries to replace HTML content. If content is already replaced (has data-i18n), regex won't match.
            # That's fine.
            "lead_text": {
                "en": "Kadia Dhro \(or Kadiya Dhrow\) is Kutch's most spectacular hidden gem.*natural wonders\.", 
                "en_full": "Kadia Dhro (or Kadiya Dhrow) is Kutch's most spectacular hidden gem, often called the 'Grand Canyon of India'. This geological marvel features stunning multi-colored rock formations carved by wind and water over centuries. The riverbed displays vibrant bands of red, yellow, and orange sandstone, creating a surreal landscape that looks like a painting come to life. Once an obscure spot, it is now a must-visit for nature lovers.",
                "hi": "कड़िया ध्रो (या कड़िया ध्रोव) कच्छ का सबसे शानदार छिपा हुआ रत्न है, जिसे अक्सर 'भारत का ग्रैंड कैनियन' कहा जाता है। इस भूवैज्ञानिक चमत्कार में सदियों से हवा और पानी द्वारा तराशी गई शानदार बहुरंगी चट्टानें हैं। नदी के तल में लाल, पीले और नारंगी बलुआ पत्थर के जीवंत बैंड दिखाई देते हैं, जो एक अतिरेक परिदृश्य (surreal landscape) बनाते हैं जो एक पेंटिंग के जीवन में आने जैसा दिखता है।"
            },
            "who_title": { "en": "Who Should Visit", "hi": "Who Should Visit" },
            "who_photographers": {
                "en": "<strong>Photographers</strong>: For the dramatic colors and rock textures",
                "hi": "<strong>Photographers</strong>: नाटकीय रंगों और रॉक टेक्सचर के लिए (सूर्योदय/सूर्यास्त पर सबसे अच्छी रोशनी)।"
            },
            "who_hikers": {
                "en": "<strong>Hikers & Explorers</strong>: Requires a bit of walking",
                "hi": "<strong>Hikers & Explorers</strong>: असमान पथरीले इलाके में थोड़ा चलने की आवश्यकता है।"
            },
            "landmark_title": { "en": "Landmarks & Heritage", "hi": "Landmarks & Heritage" },
            "canyon_hike_title": { "en": "Canyon Hike", "hi": "Canyon Hike" },
            "canyon_hike_desc": { "en": "\(1-2 Hours\) Walk down into the riverbed.*", "hi": "(1-2 घंटे) नीचे से विशाल रॉक स्तंभों को देखने के लिए नदी के तल में चलें (यदि सूखा हो)।" },
            "photo_title": { "en": "Photography", "hi": "Photography" },
            "photo_desc": {
                "en": "Climb the small cliffs for a panoramic top-down shot.*",
                "hi": "रंगीन बैंड के मनोरम टॉप-डाउन शॉट के लिए छोटी चट्टानों पर चढ़ें।"
            },
            "croc_title": { "en": "Crocodile Spotting", "hi": "Crocodile Spotting" },
            "croc_desc": {
                "en": "Be careful! Freshwater crocodiles live.*",
                "hi": "सावधान रहें! नदी के गहरे पानी के कुंडों में मीठे पानी के मगरमच्छ रहते हैं।"
            },
            "sunset_title": { "en": "Sunset View", "hi": "Sunset View" },
            "sunset_desc": { "en": "The rocks glow golden-red during the evening.*", "hi": "शाम के सुनहरे समय (golden hour) के दौरान चट्टानें सुनहरी-लाल चमकती हैं।" },
             "tips_title": { "en": "Curated Local Advice", "hi": "Curated Local Advice" },
             "tip_facilities_title": { "en": "No Facilities", "hi": "No Facilities" },
             "tip_facilities_desc": { "en": "There are ZERO shops, toilets, or water stalls.*", "hi": "यहाँ कोई दुकानें, शौचालय या पानी के स्टॉल नहीं हैं। अपनी ज़रूरत का सब कुछ साथ ले जाएँ।" },
             "when_title": { "en": "When to Visit", "hi": "When to Visit" },
             "when_desc": { 
                 "en": "<strong>November to February:</strong> Best weather for hiking.*", 
                 "hi": "<strong>November to February:</strong> लंबी पैदल यात्रा के लिए सबसे अच्छा मौसम। <br><br><strong>Monsoon (July-Sept):</strong> परिदृश्य हरा-भरा होता है और नदी बहती है, जो मंत्रमुग्ध कर देने वाली लगती है, लेकिन एप्रोच रोड बहुत कीचड़युक्त और कठिन हो जाती है।" 
             },
             "itinerary_title": { "en": "Suggested Itinerary", "hi": "Suggested Itinerary" },
             "day_7am": { "en": "00 AM: Depart from Bhuj with packed breakfast.", "hi": "00 AM: पैक्ड नाश्ते के साथ भुज से प्रस्थान करें।" },
             "day_8am": { "en": "00 AM: Reach Kadia Dhro. Park safely.", "hi": "00 AM: कड़िया ध्रो पहुँचें। सुरक्षित पार्क करें।" },
             "day_815am": { "en": "15 AM - 10:30 AM: Hike, explore, and photography.", "hi": "15 AM - 10:30 AM: हाइक, एक्सप्लोर और फोटोग्राफी।" },
             "day_11am": { "en": "00 AM: Visit nearby Rakhal Van.*", "hi": "00 AM: यदि समय मिले तो पास के रखाल वन (आरक्षित वन) जाएँ।" },
             "day_1230pm": { "en": "30 PM: Return to Bhuj for lunch.", "hi": "30 PM: दोपहर के भोजन के लिए भुज वापस लौटना।" }
        }
    },
     "mandvi": {
        "file": "mandvi.html",
        "content": {
            "hero_title": { "en": "Mandvi — Where the Desert Meets the Sea", "hi": "Mandvi — Where the Desert Meets the Sea" },
            "lead_text": {
                "en": "Mandvi is the only premier beach destination in Kutch.*White Rann\.",
                "en_full": "Mandvi is the only premier beach destination in Kutch, offering a perfect relaxed break from the arid desert landscape. Once a major port for the spice trade, it is now a popular day-trip and weekend getaway from Bhuj (1 hour away). Known for its pristine beaches, the royal Vijay Vilas Palace, and a 400-year-old shipbuilding tradition, Mandvi is where history meets the Arabian Sea. A typical visit lasts 1 to 2 days, making it ideal for unwinding after exploring the White Rann.",
                "hi": "मांडवी कच्छ का एकमात्र प्रमुख बीच डेस्टिनेशन है, जो शुष्क रेगिस्तानी परिदृश्य से एक आदर्श आरामदायक ब्रेक प्रदान करता है। कभी मसाला व्यापार के लिए एक प्रमुख बंदरगाह, अब यह भुज (1 घंटे दूर) से एक लोकप्रिय डे-ट्रिप और वीकेंड गेटअवे है। अपने साफ समुद्र तटों, शाही विजय विलास पैलेस और 400 साल पुरानी जहाज निर्माण परंपरा के लिए जाना जाने वाला, मांडवी वह जगह है जहाँ इतिहास अरब सागर से मिलता है। एक सामान्य यात्रा 1 से 2 दिनों तक चलती है, जो इसे व्हाइट रण की खोज के बाद आराम करने के लिए आदर्श बनाती है।"
            },
            "landmark_title": { "en": "Landmarks & Heritage", "hi": "Landmarks & Heritage" },
            "palace_title": { "en": "Vijay Vilas Palace", "hi": "Vijay Vilas Palace" },
            "palace_desc": { "en": "\(1-2 Hours\) Visit in the afternoon.*", "hi": "(1-2 घंटे) शाही भव्यता देखने के लिए दोपहर (3 PM - 5 PM) में जाएँ। 'हम दिल दे चुके सनम' की शूटिंग के लिए प्रसिद्ध। प्रवेश: ₹50. फोन कैमरे की अनुमति है।" },
            "beach_title": { "en": "Mandvi Wind Farm Beach", "hi": "Mandvi Wind Farm Beach" },
            "beach_desc": { "en": "\(Evening\) The best sunset point.*", "hi": "(शाम) सबसे अच्छा सनसेट पॉइंट। ऊंट की सवारी, घुड़सवारी और स्ट्रीट फूड का आनंद लें। सप्ताहांत (weekends) पर भीड़ होती है, इसलिए शांति के लिए थोड़ा आगे जाएँ।" },
            "ship_title": { "en": "Shipbuilding Yard", "hi": "Shipbuilding Yard" },
            "ship_desc": { "en": "\(30-45 Mins\) Visit in the morning.*", "hi": "(30-45 मिनट) सुबह जाएँ। कारीगरों को रुक्मावती नदी के किनारे हाथ से विशाल लकड़ी के जहाज बनाते हुए देखें। पुल से देखने के लिए नि:शुल्क।" },
            "72_title": { "en": "72 Jinalaya", "hi": "72 Jinalaya" },
            "72_desc": { "en": "\(45 Mins\) A stunning Jain temple complex.*", "hi": "(45 मिनट) शहर से 10 किमी दूर एक शानदार जैन मंदिर परिसर। मुंद्रा जाने/आने के रास्ते में जाना सबसे अच्छा है। शांतिपूर्ण और फोटोजेनिक वास्तुकला।" },
            "memorial_title": { "en": "Shyamji Krishna Varma Memorial", "hi": "Shyamji Krishna Varma Memorial" },
            "memorial_desc": { "en": "\(1 Hour\) Interactive museum dedicated to the freedom fighter.*", "hi": "(1 घंटा) स्वतंत्रता सेनानी को समर्पित इंटरैक्टिव संग्रहालय। इतिहास प्रेमियों के लिए बहुत अच्छा है। गुरुवार को बंद रहता है।" },
            "tips_title": { "en": "Curated Local Advice", "hi": "Curated Local Advice" },
            "tip_timing_title": {"en": "Timing", "hi": "Timing"},
            "tip_timing_desc": {"en": "Don't visit the beach at noon.*", "hi": "दोपहर (12-3 PM) में बीच पर न जाएँ; बहुत गर्मी होती है। सुबह और शाम सबसे अच्छे हैं।"},
             "when_title": { "en": "When to Visit", "hi": "When to Visit" },
             "when_desc": { "en": "<strong>October to March \(Winter\):</strong> Best time.*", 
             "hi": "<strong>October to March (Winter):</strong> सबसे अच्छा समय। दिन सुहावने (20-30°C) होते हैं और शामें ठंडी होती हैं। बीच गतिविधियों के लिए उत्तम।<br><br><strong>April to June (Summer):</strong> गर्म और उमस भरा। दिन का तापमान 35-40°C तक पहुँच जाता है। शाम की सैर के लिए अच्छा है लेकिन दिन में घूमने से बचें।<br><br><strong>July to September (Monsoon):</strong> मांडवी हरे-भरे परिवेश और नाटकीय बादलों के साथ सुंदर दिखता है, लेकिन समुद्र के खराब होने के कारण तैरना प्रतिबंधित है।" 
             }
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
                clean_text = v["en"].replace("\\(", "(").replace("\\)", ")").replace(".*", "").replace("\\.", ".")
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

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    update_json(os.path.join(LANG_DIR, "en.json"), f"destinations.{page_key}", config["content"], "en")
    update_json(os.path.join(LANG_DIR, "hi.json"), f"destinations.{page_key}", config["content"], "hi")

    new_content = content
    # ... (Regex replacement logic omitted here for brevity as it was already run, but okay to re-include to be safe)
    # Actually, let's keep it simple and just do the injection, or re-run regex if keys are missing in HTML
    
    for key, val_map in config["content"].items():
        en_pattern = val_map.get("en", "")
        if not en_pattern: continue
        pattern_escaped = en_pattern if "\\" in en_pattern else re.escape(en_pattern)
        full_regex = f"(<[^>]+)(>)\\s*({pattern_escaped})\\s*(</[^>]+>)"
        i18n_key = f"destinations.{page_key}.{key}"
        replacement = f'\\1 data-i18n="{i18n_key}"\\2\\3\\4'
        new_content = re.sub(full_regex, replacement, new_content, count=1)
        full_regex_dot = f"(<[^>]+)(>)\\s*({pattern_escaped})\\s*(</[^>]+>)"
        new_content = re.sub(full_regex_dot, replacement, new_content, count=1, flags=re.DOTALL)

    # Inject i18n.js script if missing
    if 'src="../js/i18n.js"' not in new_content:
        # Try to insert before script.js
        if 'src="../js/script.js"' in new_content:
            new_content = new_content.replace('<script src="../js/script.js"></script>', '<script src="../js/i18n.js"></script>\n    <script src="../js/script.js"></script>')
            print("Injected i18n.js script tag")
        else:
            # Insert before body end
            new_content = new_content.replace('</body>', '<script src="../js/i18n.js"></script>\n</body>')
            print("Injected i18n.js script tag before body end")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated HTML file {file_path}")

if __name__ == "__main__":
    process_file("kadia_dhrow")
    process_file("mandvi")
