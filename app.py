from flask import Flask,render_template
import graph

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('exe.html')

@app.route('/make_graph')
def make_graph():
    graph.make_graph("/static/csv/data.csv")
    print(134)
    return render_template('show.html')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
