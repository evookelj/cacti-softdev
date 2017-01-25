var Graphing = (function (window) {
    "use strict";
    const arrow_head_side_len = 6;
    const arrow_head_angle = Math.PI * 0.2;
    const minutes_in_day = 60 * 24;

    const emoji_fire = "\uD83D\uDD25";
    const emoji_100 = "\uD83D\uDCAF";
    const emoji_poo = "\uD83D\uDCA9";

    const point_color = "#ff0000";
    const graph_color = "#003474";
    const bg_color = "#d0eeed";

    /////////////////////////////////////////////////////////////
    // UTIL: ////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////

    var fmtHour = function (hour) {
        hour = hour % 12;
        if (hour == 0) {
            return "12";
        }
        return String(hour);
    };
    // Format time (represented as minutes since midnight) for
    // display on the graph.
    var fmtTime = function (minutes) {
        var hours = Math.trunc(minutes / 60);
        var minsAfterHour = minutes % 60;
        if (hours == 0) {
            return "12:" + minsAfterHour + " AM";
        }
        if (hours < 12) {
            return hours + ":" + minsAfterHour + " AM";
        }
        return (hours - 12) + ":" + minsAfterHour + " PM";
    };

    /**
     * data format: array of...
     * {
     *     time: [integer (hours since midnight), integer (minutes after the hour)]
     *     weight: number from 0 to 1.0
     * }
     * sortDatapoints returns a map from times, represented as minutes since
     * midnight, to arrays of weights
     */
    var sortDatapoints = function (data) {
        var result = {}, i, timeInMinutes;
        for (i = 0; i < data.length; i += 1) {
            timeInMinutes = data[i].time[0] * 60 + data[i].time[1];
            // Set the position to an array if not already set
            result[timeInMinutes] = result[timeInMinutes] || [];
            // Put this weight in the position
            result[timeInMinutes].push(data[i].weight);
        }
        return result;
    };



    /////////////////////////////////////////////////////////////
    // DRAWING FUNCTIONS: ///////////////////////////////////////
    /////////////////////////////////////////////////////////////

    // Conventions:
    //  sketchThing(ctx, ...) sketches a path onto ctx (beginPath should be
    //    called beforehand, and stroke/fill must be called after)
    //  drawThing(ctx, ...) draws a thing to ctx, not requiring
    //    path-stroking/filling by the caller

    var sketchArrow = function (ctx, x, y, x1, y1) {
        ctx.moveTo(x, y);
        var theta = Math.atan2(y1 - y, x1 - x);
        console.log("theta", theta, "from", x, y, "to", x1, y1);
        // Draw arrow stem
        ctx.lineTo(x1, y1);
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

    var drawAxisLabels = function (ctx, x_left, y_top, w, h) {
        var cx = x_left + w / 2;
        var cy = y_top + h / 2;

        ctx.textAlign = "center";

        // X AXIS LABELS:

        ctx.save();

        // Draw tick marks for hours, and corresponding hour numbers:
        var hourTickSep = w / 24;
        var i, tickx;
        ctx.beginPath();
        for (i = 0; i < 24; i++) {
            tickx= x_left + i * hourTickSep;
            ctx.moveTo(tickx, y_top + h - 3);
            ctx.lineTo(tickx, y_top + h + 3);
            ctx.fillText(fmtHour(i), tickx, y_top + h + 15);
        }
        ctx.stroke();

        // Draw AM label under first half of graph, PM label under
        // second half, "Time of day" label under center:
        ctx.fillText("AM", cx - w / 4, y_top + h + 35);
        ctx.fillText("PM", cx + w / 4, y_top + h + 35);
        ctx.font = "15px sans-serif";
        ctx.fillText("Time of day   ", cx, y_top + h + 45);

        ctx.restore();

        // Y AXIS LABELS:
        // Tick marks:
        ctx.beginPath();
        ctx.moveTo(x_left - 4, y_top + h);
        ctx.lineTo(x_left + 4, y_top + h);
        ctx.moveTo(x_left - 4, y_top + 10);
        ctx.lineTo(x_left + 4, y_top + 10);
        ctx.stroke();

        // Max-weight and min-weight labels:
        ctx.save();
        ctx.font = "20px sans-serif";
        ctx.fillText(emoji_poo, x_left - 18, y_top + h);
        ctx.fillText(emoji_100, x_left - 18, y_top + 17);
        ctx.restore();

        // "Success" label:
        ctx.save();
        ctx.font = "15px sans-serif";
        ctx.translate(x_left, y_top);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText("Success", -h / 2, -8);
        ctx.restore();
    };

    var drawScatterplot = function (ctx, x_left, y_top, w, h, data) {
        ctx.fillStyle = bg_color;
        ctx.fillRect(x_left - 35, y_top - 10, w + 45, h + 65);
        ctx.fillStyle = graph_color;
        ctx.strokeStyle = graph_color;
        console.log(data);
        ctx.save();
        ctx.beginPath();
        sketchAxes(ctx, x_left, y_top, w, h);
        ctx.stroke();
        var t, j, px, py;
        ctx.beginPath();
        for (t = 0; t < minutes_in_day; t += 1) {
            if (Array.isArray(data[t])) {
                for (j = 0; j < data[t].length; j++) {
                    px = x_left + t / minutes_in_day * w;
                    // data[t][j] is the weight for this post, from 0.0 to 1.0
                    py = y_top + h - data[t][j] * h;
                    ctx.moveTo(px, py);
                    ctx.arc(px, py, 3, 0, 2 * Math.PI, false);
                }
            }
        }
        ctx.fillStyle = point_color;
        ctx.fill();
        ctx.restore();
        drawAxisLabels(ctx, x_left, y_top, w, h);
    };

    return Object.freeze({
        sortDatapoints: sortDatapoints,
        drawScatterplot: drawScatterplot,
        drawAxisLabels: drawAxisLabels
    });
}(this));
