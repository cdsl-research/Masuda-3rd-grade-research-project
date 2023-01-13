import pandas as pd
import matplotlib.pyplot as plt
def make_graph(file):
    input_csv = pd.read_csv(f"./{file}")
    first_column_data = input_csv[input_csv.keys()[0]]
    second_column_data = input_csv[input_csv.keys()[1]]

    plt.xlabel(input_csv.keys()[0])
    plt.ylabel(input_csv.keys()[1])

    plt.plot(first_column_data, second_column_data, linestyle='solid', marker='o')
    plt.savefig("./static/images/graph.png")
    plt.show()
