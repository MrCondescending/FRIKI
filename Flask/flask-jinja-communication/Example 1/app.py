from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.x = 10

@app.route('/', methods=['GET', 'POST'])
def index():
    name = 'John'
    return render_template('index.html', name=name, p = {'a':1, 'b':2}, app = app)

if __name__ == '__main__':
    app.run(debug=True)
