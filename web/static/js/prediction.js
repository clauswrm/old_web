const canvas = document.getElementById('draw');
const context = canvas.getContext('2d');
const url = 'https://clausmartinsen.no/predict';
let painting = false;

// Start drawing
canvas.addEventListener('mousedown', function (e) {
    painting = true;
    draw(e);
});

// Draw...
canvas.addEventListener('mousemove', function (e) {
    if (painting) {
        draw(e);
    }
});

// Stop drawing and make model predict
canvas.addEventListener('mouseup', function (e) {
    painting = false;
    predict()
});

function draw(event) {
    const mousePos = getRelativeMousePos(event);
    const radius = 5;

    context.strokeStyle = '#000000';
    context.moveTo(mousePos.x, mousePos.y);
    context.beginPath();
    context.arc(mousePos.x, mousePos.y, radius, 0, 2 * Math.PI);
    context.fill();
    context.stroke();
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
    }).catch(reason => {
        console.error(reason);
        showPrediction('Error predicting number')
    }).then(response => {
        return response.text();
    }).then(number => {
        showPrediction(number);
    });
}

function showPrediction(prediction) {
    const predictionText = document.getElementById('prediction');
    predictionText.innerHTML = "Prediction: " + prediction;
}

function clearDrawing() {
    context.beginPath();
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.stroke();
}
