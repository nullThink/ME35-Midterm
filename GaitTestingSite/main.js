const canvas = document.getElementById("gaitCanvas");
const ctx = canvas.getContext('2d');
const ASPECT_RATIO = 0.5; //((canvas.width)) / 2000;

class Leg {
    constructor(l, startX, startY, color) {
        this.legLength = (l * 100) * ASPECT_RATIO;
        this.angleFromHoriz = (1) * Math.PI;
        this.currX = startX;
        this.currY = startY;
        this.legColor = color;
    }
    setAngle(angle) {
        this.angleFromHoriz = angle * (Math.PI / 180);
    }
    getEndPoint() {
        return {
            'x': (this.legLength * Math.cos(Math.PI - this.angleFromHoriz) - this.currX),
            'y': (this.legLength * Math.sin(Math.PI - this.angleFromHoriz) - this.currY)
        };
    }

    setCurrPoint(xValue, yValue) {
        this.currX = xValue;
        this.currY = yValue;
    }

    drawLeg(ctx) {
        ctx.beginPath();
        ctx.strokeStyle = this.legColor;
        ctx.lineWidth = '2';

        ctx.translate(this.currX, this.currY);
        ctx.rotate(this.angleFromHoriz);
        ctx.translate(-this.currX, -this.currY);

        ctx.moveTo(this.currX, this.currY);
        ctx.lineTo(this.currX + this.legLength, this.currY);
        ctx.stroke();

        ctx.closePath();

        this.drawEndPoint(ctx);
    }

    drawEndPoint(ctx) {
        ctx.beginPath();
        ctx.strokeStyle = 'red';

        ctx.arc(this.getEndPoint().x, this.getEndPoint().y, 10, 0, 0)
        ctx.fill();
        ctx.closePath();
    }

    getAngle() {
        return this.angleFromHoriz;
    }
}

// Hip leg is about 7 cm long, knee leg is about 13 cm.
let hipLeg = new Leg(7, canvas.width / 2, 0, 'green');
let kneeLeg = new Leg(13, canvas.width / 2, 0, "blue");
hipLeg.setAngle(70);
kneeLeg.setAngle(20);

window.onload = ((e) => {
    draw(ctx);
});

function resetCanvas(ctx) { ctx.clearRect(0, 0, canvas.width, canvas.height) }

function draw(ctx) {
    kneeLeg.drawLeg(ctx);
    hipLeg.drawLeg(ctx);
    // ctx.beginPath()
    // ctx.fillRect(10, 10, 10, 10)
    // ctx.closePath()

    // ctx.beginPath();
    // ctx.strokeStyle = 'black';
    // ctx.lineWidth = '2';
    // ctx.moveTo(canvas.width / 2, canvas.height / 2);
    // ctx.lineTo(canvas.width, canvas.height);
    // ctx.stroke();
    // ctx.closePath();
} // ctx.closePath();