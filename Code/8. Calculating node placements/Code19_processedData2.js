// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

const fs = require('fs');

const processData = (filename) => {
    fs.readFile(filename, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading the file:', err);
            return;
        }

        const nodes = new Set(); // Populate this with your nodes
        const links = []; // Populate this with your links
        let currentQuery = null;
        let queryCount = 0; // Counter for processed queries
        let subjectCount = 1; 
        const lines = data.split('\n');

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            
            if (line.startsWith('Query:')) {
                /*if (queryCount == 50) {
                    break; // Exit the loop after 10 queries
                }*/
                currentQuery = line.split(' ')[1];
                nodes.add(currentQuery);
                queryCount++; // Increment the query counter
                subjectCount = 1; // Reset counter for subjects
            } else if (line.startsWith('Subject:') && currentQuery) {
                const parts = line.split(/\s+/);
                const subjectId = parts[1];
                //const eValue = parseFloat(parts[3]);
                
                //evalue normalization
                eValue = parseFloat(parts[3]);
                //mineval = 69.0004 //from processeddata3-med for 18, but make it positive
                //mineval = 120.71 //from processeddata3-med for 43, but make it positive
                mineval = 145.403 //from processeddata3-med for 200, but make it positive
                
                let normeValue = eValue + mineval;

                nodes.add(subjectId);
                links.push({ source: currentQuery, target: subjectId, value: normeValue, subject: subjectCount });
                subjectCount++;
            }
        }

        // Convert nodes Set to an array of objects
        const nodesArray = Array.from(nodes).map(id => ({ id }));

        // Write the processed data to a JSON file
        const output = { nodes: nodesArray, links };
        fs.writeFile('/Users/chenlab/Desktop/blastcodetesting/fdgtest/finalprocessedallbinders200graphdata50percent.json', JSON.stringify(output, null, 2), err => {
            if (err) {
                console.error('Error writing processed data:', err);
                return;
            }
            console.log('Data processed and saved.');
        });
    });
};

processData('/Users/chenlab/Desktop/blastcodetesting/fdgtest/finalprocessedmcallbinders200graphdata50percent.txt');
