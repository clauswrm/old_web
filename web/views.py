from flask import render_template, request, Response, jsonify

from web import app
from web.digit_predictor import DigitPredictor, convert_canvas_image_to_array

model = DigitPredictor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<user>')
def user_page(user):
    return render_template('user.html', user=user)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    image_data = request.get_data()
    try:
        image = convert_canvas_image_to_array(image_data)
        prediction = model.predict(image)
        return jsonify(prediction)
    except RuntimeError:
        return Response('Server could not predict input', status=500)


@app.errorhandler(404)
def page_not_found(e):
    return '404 not found', 404
