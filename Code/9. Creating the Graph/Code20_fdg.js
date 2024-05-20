// This code is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
// To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.

//new distance calc and trying to get the window to fit
fetch('finalprocessedallbinders200graphdata50percent.json')
    .then(response => response.json())
    .then(data => {
        const { nodes, links } = data;
        console.log(window.innerWidth, window.innerHeight);
        //console.log("nodes loaded:", nodes)
        //console.log("Links loaded:", links)
        
        
        var simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(d => calculateDistance(d)))
            .force("charge", d3.forceManyBody().strength(-2))
            .force("center", d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2));

        // Schedule the transformation to occur after 30 seconds
        setTimeout(() => {
            // Stop the simulation
            simulation.stop();

            // Apply the linear transformation
            applyLinearTransformation(nodes, window.innerWidth, window.innerHeight);

            updatePositions();

            // Log the transformed coordinates and/or update the SVG elements
            nodes.forEach(d => {
                console.log(`Transformed Node ${d.id}: x=${d.x}, y=${d.y}`);
                // Update SVG elements if necessary
            });

        }, 80000); // 80 seconds

        function calculateDistance(link) {
            // equation for edge distance
            let x = Math.max(link.value, 1e-200);
            x = Math.log10(x);
            // scale based on window size
            return x/Math.max(window.innerWidth, window.innerHeight);
        }

        function applyLinearTransformation(nodes, width, height) {
            // Find min and max x, y coordinates
            let minX = d3.min(nodes, d => d.x);
            let maxX = d3.max(nodes, d => d.x);
            let minY = d3.min(nodes, d => d.y);
            let maxY = d3.max(nodes, d => d.y);
        
            // Calculate scale and translation factors
            let a = (width - 30) / (maxX - minX);
            let b = 15 - minX * (width - 30) / (maxX - minX);
            let c = (height-30) / (maxY - minY);
            let d = 15 -minY * (height-30) / (maxY - minY);
        
            // Apply transformation to each node
            nodes.forEach(node => {
                node.x = a * node.x + b;
                node.y = c * node.y + d;
            });
        }

        function updatePositions() {
            // Update node positions
            node.attr("cx", d => d.x)
                .attr("cy", d => d.y);
        
            // Update link positions
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        
            // Optionally update label positions as well
            labels.attr("x", d => d.x)
                  .attr("y", d => d.y);
        }
        

        var svg = d3.select("body").append("svg")
            .attr("width", window.innerWidth)
            .attr("height", window.innerHeight);

        var link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke-width", 2)
            //.attr("stroke", d => linkColor(d.subject));
            .attr("stroke", "black")
            .attr("opacity", d => linkOpacity(d.subject));

        function linkColor(subjectNumber) {
            if (subjectNumber === 1) {
                return "black";
            } else if (subjectNumber === 2) {
                return "gray";
            } else {
                return "blue";
            }
        }

        function linkOpacity(subjectNumber) {
            if (subjectNumber === 1) {
                return 0.5;
            } else if (subjectNumber === 2) {
                return 0.3;
            } else {
                return 0.15;
            }
        }

        function nodeColor(id) {
            if (id[0] === 'm' || id[0] === '!') {
                return "#f6c19c";
            } else if(id.startsWith('b&')){
                return "red"
            }else {
                //return "#b7ef7b";
                return "#1e90ff";
            }
        }

        function nodeOpacity(id) {
            if (id[0] === 'm' || id[0] === '!') {
                return 0.5; // g3p sequences have semi-opaque nodes
            } else {
                return 1.0; // reference sequences and potential binding sequences have solid nodes
            }
        }
        
        //can modify such that repeated g3p sequencees have slightly larger sizes 
        function nodeRadSize(id) {
            if (id[0] == 'm' || id[0] == 'b') {
                return 5; //0.5 of 10
            } else if (id[0] === '!'){ 
                let startIndex = id.indexOf("!") + 1;
                let endIndex = id.indexOf("m");
                let numberStr = id.substring(startIndex, endIndex);
                let number = parseInt(numberStr);
                return 5 + Math.log(number)/10;
            }else{
                return 10;
            }
        }

        var node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", d => nodeRadSize(d.id))
            .attr("fill", d => nodeColor(d.id))
            .attr("opacity", function(d) { return nodeOpacity(d.id); }); 

        function nodeLabel(id) {
            if (id[0] === 'm' || id[0] == '!' || id[0] == 'b') {
                return false;
            } else {
                return true;
            }
        }

        var labels = svg.selectAll(".label")
            .data(nodes.filter(node => nodeLabel(node.id)))
            //.data(nodes)
            .enter().append("text")
            .attr("class", "label")
            .text(d => d.id);

        // Update SVG dimensions on window resize
        window.addEventListener("resize", function() {
            svg.attr("width", window.innerWidth)
            .attr("height", window.innerHeight);
            // You may also want to update the force center or other aspects of the simulation here
        });

        // Modify tick function to constrain node positions within SVG
        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("cx", d => Math.max(0, Math.min(window.innerWidth, d.x)))
                .attr("cy", d => Math.max(0, Math.min(window.innerHeight, d.y)));
            // Update link positions and labels similarly

            labels.attr("x", d => d.x)
                  .attr("y", d => d.y);
        });
    }); 
