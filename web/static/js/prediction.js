const canvas = document.getElementById('draw');
const context = canvas.getContext('2d');
const url = 'https://clausmartinsen.no/predict';

let painting = false;
let previousMousePos = null;

// Start drawing
canvas.addEventListener('mousedown', function (e) {
    painting = true;
    previousMousePos = getRelativeMousePos(e);
});

canvas.addEventListener('touchstart', function (e) {
    e.preventDefault(); // Prevent screen scroll
    painting = true;
    let touch = e.touches[0];
    previousMousePos = getRelativeMousePos(touch);
});

// Continue drawing
canvas.addEventListener('mousemove', function (e) {
    if (painting) {
        draw(e);
    }
});

canvas.addEventListener('touchmove', function (e) {
    e.preventDefault(); // Prevent screen scroll
    if (painting) {
        let touch = e.touches[0];
        draw(touch);
    }
});

// Stop drawing and make model predict
canvas.addEventListener('mouseup', function (e) {
    painting = false;
    previousMousePos = null;
    predict();
});

canvas.addEventListener('touchend', function (e) {
    e.preventDefault(); // Prevent screen scroll
    painting = false;
    previousMousePos = null;
    predict();
});

function draw(event) {
    const mousePos = getRelativeMousePos(event);
    context.strokeStyle = '#000000';
    context.lineJoin = 'round';
    context.lineWidth = 10;

    // Draw a line from previous pos to current pos
    context.beginPath();
    context.moveTo(previousMousePos.x, previousMousePos.y);
    context.lineTo(mousePos.x, mousePos.y);
    context.closePath();
    context.stroke();

    // Update previous mouse pos
    previousMousePos = mousePos;
}

function getRelativeMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

function predict() {
    const img = canvas.toDataURL();
    fetch(url, {
        method: 'POST',
        headers: {
            'content-type': 'text/plain'
        },
        body: img
    }).then(response => {
        return response.text();
    }).then(number => {
        showPrediction(number);
    }).catch(reason => {
        console.error(reason);
        showPrediction('ERROR');
    });
}

function showPrediction(prediction) {
    const predictionText = document.getElementById('prediction');
    predictionText.innerHTML = 'Prediction: ' + prediction;
}

function clearDrawing() {
    // Clear whole canvas
    context.beginPath();
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.closePath();
    context.stroke();
}
