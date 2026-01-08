const fs = require('fs');
const path = require('path');

const files = ['en.json', 'de.json', 'fr.json', 'es.json', 'ru.json'];
const basePath = path.join(__dirname, 'site/lang');

files.forEach(file => {
    const filePath = path.join(basePath, file);
    try {
        if (fs.existsSync(filePath)) {
            let content = fs.readFileSync(filePath, 'utf8');
            // Look for the end of the footer object (indicated by 'dev_credit') followed by the start of 'home' object
            // This is safer than just looking for `} "home"` in case there are other similar patterns, though likely unique here.
            // We know the problematic area is between "footer" and "home".
            
            const idx = content.indexOf('"mandvi": {');
            if (idx !== -1) {
                const preceding = content.substring(Math.max(0, idx - 20), idx);
                console.log(`Preceding "mandvi" in ${file}: ${JSON.stringify(preceding)}`);
                
                // Check if there is a comma in the preceding non-whitespace characters
                let ptr = idx - 1;
                while (ptr >= 0 && /\s/.test(content[ptr])) {
                    ptr--;
                }
                
                if (content[ptr] === '}') {
                    console.log(`Found closing brace at pos ${ptr} without comma. Fixing...`);
                    const newContent = content.slice(0, ptr + 1) + ',' + content.slice(ptr + 1);
                    fs.writeFileSync(filePath, newContent);
                    console.log(`Fixed ${file}`);
                } else if (content[ptr] === ',') {
                    console.log(`${file} already has a comma.`);
                } else {
                    console.log(`Unexpected char '${content[ptr]}' before "mandvi" in ${file}`);
                }
            } else {
                console.log(`"mandvi" key not found in ${file}`);
            }
        } else {
            console.log(`File not found: ${filePath}`);
        }
    } catch (err) {
        console.error(`Error processing ${file}:`, err);
    }
});
