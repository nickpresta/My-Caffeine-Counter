function drawPlus(elm, size, color) {
    var canvas = elm;

    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");

        ctx.fillStyle = color;
        ctx.strokeStyle = color;

        ctx.fillRect(size / 3, 0, size / 3, size);
        ctx.fillRect(0, size / 3, size, size / 3);
    } else {
        alert("Your browser must support the Canvas element");
    }
}

function drawText(elm, text, color, font, baseline, align) {
    var canvas = elm;

    canvas.setAttribute("value", text);
    canvas.setAttribute("width", canvas.getAttribute("value").length * 70);

    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");

        ctx.width = 100;
        ctx.height = 100;
        ctx.fillStyle = color;
        ctx.font = font;
        ctx.textBaseline = baseline;
        ctx.textAlign = align;

        ctx.fillText(text, 0, 0);
    } else {
        alert("Your browser must support the Canvas element");
    }
}

jQuery.fn.center = function() {
    this.css("position","absolute");
    this.css("top", ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px");
    this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
    return this;
}

jQuery.fn.clearCanvas = function() {
    this[0].width = this.width();
}

function updateCount(elm, cType) {
    var data = { n: elm[0].getAttribute("value"), type: cType }
    $.get("/update/", data, function (data) {
            elm.fadeOut("slow", function() {
                elm.clearCanvas();
                var temp = new Array();
                temp = data.split(",");
                num = temp[0];
                choice = temp[1];
                $('body').data('choice', choice);
                drawText(elm[0], num, "black", "7em Arial", "top", "start");
                elm.fadeIn("slow");
                $("#counter").center();
                });
            });
}
