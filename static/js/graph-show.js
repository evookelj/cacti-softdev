(function () {
    "use strict";
    var canvas = document.getElementById("graph-canvas");
    var ctx = canvas.getContext('2d');

    // Increases line sharpness
    ctx.translate(0.5, 0.5);

    var graphContainer = document.getElementById("graph");
    var graphData = [];
    try {
        graphData = JSON.parse(graphContainer.getAttribute("data-tweets"));
    } catch (e) {
        console.error(e);
        console.error("PARSING data-tweets FAILED");
    }

    Graphing.drawScatterplot(ctx, 30, 10, 400, 200, Graphing.sortDatapoints(graphData));
}());
