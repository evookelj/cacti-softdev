(function () {
    "use strict";
    var canvas = document.getElementById("graph-canvas");
    var ctx = canvas.getContext('2d');

    // Increases line sharpness
    ctx.translate(0.5, 0.5);

    // graphContainer is the <div> containing the <canvas>. It
    // has attribute data-tweets which contains the JSON data
    // for the tweets to be displayed in the <canvas>.
    var graphContainer = document.getElementById("graph");
    var graphDataJSON = graphContainer.getAttribute("data-tweets");
    var graphData = [];
    try {
        graphData = JSON.parse(graphDataJSON);
        console.log("graphData:", graphData);
        console.log("graphDataJSON:", graphDataJSON);
    } catch (e) {
        // If parsing the JSON failed, something is very wrong. Most likely
        // a problem with how the server is putting the data into the template
        console.error(e);
        console.error("PARSING data-tweets FAILED");
    }

    // Draw a scatterplot of the data in graphData, at (x=30, y=10) on the
    // canvas, and give the graph dimensions 400x200
    Graphing.makeGraph(ctx, graphData, 30, 10, 400, 200);
}());
