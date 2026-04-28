const fs = require('fs');
const path = require('path');

const indexFile = 'index.html';
const tabFile = 'analysis_tab.html';

try {
    const indexContent = fs.readFileSync(indexFile, 'utf8');
    const tabContent = fs.readFileSync(tabFile, 'utf8');

    // Possible markers for the end of the Home section
    const startMarkers = [
        '</div> <!-- End home-view -->',
        '<!-- End home-view -->',
        '</div><!-- End home-view -->'
    ];

    // Possible markers for the end of the Analysis view
    const endMarkers = [
        '<!-- End analysis-view -->',
        '<!-- End analysis-view-->'
    ];

    let startIndex = -1;
    let startMarkerFound = '';
    for (const marker of startMarkers) {
        startIndex = indexContent.indexOf(marker);
        if (startIndex !== -1) {
            startMarkerFound = marker;
            break;
        }
    }

    let endMarkerIndex = -1;
    let endMarkerFound = '';
    for (const marker of endMarkers) {
        endMarkerIndex = indexContent.indexOf(marker);
        if (endMarkerIndex !== -1) {
            endMarkerFound = marker;
            break;
        }
    }

    if (startIndex === -1) {
        console.error("Error: Could not find any home-view end markers.");
        process.exit(1);
    }
    if (endMarkerIndex === -1) {
        console.error("Error: Could not find any analysis-view end markers.");
        process.exit(1);
    }

    const finalStartIndex = startIndex + startMarkerFound.length;
    const finalEndIndex = endMarkerIndex;

    const originalPre = indexContent.slice(0, finalStartIndex);
    const originalPost = indexContent.slice(finalEndIndex);
    
    const finalHTML = originalPre + "\n\n" + tabContent + "\n\n    " + originalPost;
    
    fs.writeFileSync(indexFile, finalHTML);
    console.log("SUCCESS: Synced index.html with analysis_tab.html");
} catch (err) {
    console.error("Unexpected Error:", err.message);
    process.exit(1);
}
