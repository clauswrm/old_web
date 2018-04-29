var canvas = document.getElementById('draw');
var context = canvas.getContext('2d');
var url = 'http://127.0.0.1:5000/predict';
var painting = false;

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
    var mousePos = getRelativeMousePos(event);
    var radius = 5;

    context.strokeStyle = '#000000';
    context.moveTo(mousePos.x, mousePos.y);
    context.beginPath();
    context.arc(mousePos.x, mousePos.y, radius, 0, 2 * Math.PI);
    context.fill();
    context.stroke();
}

function getRelativeMousePos(e) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

function predict() {
    var img = canvas.toDataURL();
    fetch(url, {
        method: 'POST',
        headers: {
            'content-type': 'text/plain'
        },
        body: img
    }).catch(function (reason) {
        console.error(reason);
        showPrediction('Error predicting number')
    }).then(function (response) {
        return response.text();
    }).then(function (number) {
        showPrediction(number)
    });
}


function showPrediction(prediction) {
    var predictionText = document.getElementById('prediction');
    predictionText.innerHTML = "Prediction: " + prediction;
}


function clearDrawing() {
    context.beginPath();
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.stroke();
}

