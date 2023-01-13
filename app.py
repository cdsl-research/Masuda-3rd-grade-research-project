from flask import Flask,render_template
import functions


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('top.html')

@app.route('/make_graph')
def make_graph():
    functions.data("./static/csv/data2.csv")
    return render_template('show.html')

if __name__ == "__main__":
    app.run(port=8080, debug=True)
