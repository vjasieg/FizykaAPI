import flask
import matplotlib.pyplot as plt

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    plt.plot([1, 2, 3, 4])
    plt.ylabel('some numbers')
    plt.show()
    return "gitara siema"

app.run()