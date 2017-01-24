var Graphing = (function (window) {
    "use strict";
    const arrow_head_side_len = 6;
    const arrow_head_angle = Math.PI * 0.2;
    const minutes_in_day = 60 * 24;

    /**
     * data format: array of...
     * {
     *     time: int (minutes since midnight,
     *     weight: number from 0 to 1.0
     * }
     * sortDatapoints returns a map from times to arrays of weights
     */
    var sortDatapoints = function (data) {
        var result = {}, i;
        for (i = 0; i < data.length; i += 1) {
            let t = data[i].time;
            // Set the position to an array if not already set
            result[t] = result[t] || [];
            // Put this weight in the position
            result[t].push(data[i].weight);
        }
        return result;
    };

    var sketchArrow = function (ctx, x, y, x1, y1) {
        ctx.moveTo(x, y);
        var theta = Math.atan2(y1 - y, x1 - x);
        console.log("theta", theta);
        // Draw arrow stem
        ctx.lineTo(x1, y1);
        console.log(
                x1 - Math.cos(theta - arrow_head_angle) * arrow_head_side_len,
                y1 - Math.sin(theta - arrow_head_angle) * arrow_head_side_len
                );
        ctx.lineTo(
                x1 - Math.cos(theta - arrow_head_angle) * arrow_head_side_len,
                y1 - Math.sin(theta - arrow_head_angle) * arrow_head_side_len
        );
        ctx.moveTo(x1, y1);
        ctx.lineTo(
                x1 - Math.cos(theta + arrow_head_angle) * arrow_head_side_len,
                y1 - Math.sin(theta + arrow_head_angle) * arrow_head_side_len
        );
        // Move back to head of arrow
        ctx.moveTo(x1, y1);
    };

    var sketchAxes = function (ctx, x_left, y_top, w, h) {
        var x_right = x_left + w;
        var y_bot = y_top + h;
        sketchArrow(ctx, x_left, y_bot, x_left, y_top);
        sketchArrow(ctx, x_left, y_bot, x_right, y_bot);
    };

    var drawScatterplot = function (ctx, x, y, w, h, data) {
        ctx.save();
        ctx.beginPath();
        sketchAxes(ctx, x, y, w, h);
        ctx.stroke();
        var t, j, px, py;
        ctx.beginPath();
        for (t = 0; t < minutes_in_day; t += 1) {
            if (Array.isArray(data[t])) {
                for (j = 0; j < data[t].length; j++) {
                    px = x + t / minutes_in_day * w;
                    // data[t][j] is the weight for this post, from 0.0 to 1.0
                    py = y - data[t][j] * h;
                    ctx.moveTo(px, py);
                    ctx.arc(px, py, 3, 0, 2 * Math.PI, false);
                }
            }
        }
        ctx.fill();
        ctx.restore();
    };
    var canvas = document.getElementById("graph");
    var ctx = canvas.getContext('2d');
    ctx.beginPath();
    sketchArrow(ctx, 40, 40, 70, 70);
    ctx.stroke();
    drawHistogram(ctx, 10, 10, 100, 100);

    return Object.freeze({
        sortDatapoints: sortDatapoints,
        drawScatterplot: drawScatterplot
    });
}(this));
