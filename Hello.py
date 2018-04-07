from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Her kommer clausmartinsen.no, med Flask backend.'


if __name__ == '__main__':
    app.run(debug=True)
