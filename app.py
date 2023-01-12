from flask import Flask,render_template
import graph
from module import self_create

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('top.html')

@app.route('/make_graph')
def make_graph():
    graph.make_graph("/static/csv/data.csv")
    return render_template('show.html')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
