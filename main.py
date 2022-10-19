
import csv, sys
from rdflib import Graph
from tabulate import tabulate


class Sparql:
    def __init__(self, data_path, query_path) -> None:
        self.data_path = data_path
        self.query_path = query_path
        self.make_graph()
        self.load_query()
    
    def make_graph(self) -> None:
        self.graph = Graph()
        self.graph.parse(self.data_path, format="ttl")

    def load_query(self) -> None:
        with open(self.query_path, mode="r") as query_file:
            self.query = query_file.read()

    def execute(self, csvfile=None) -> None:
        qres = self.graph.query(self.query)

        if not csvfile:
            header = list(map(lambda x: str(x), qres.vars))
            results = []
            for row in qres:
                results.append(list(map(lambda x: str(x), row)))
            print(tabulate(results, header, tablefmt="fancy_grid"))
        else:
            with open(csvfile, mode='w') as csv_file:
                header = list(map(lambda x: str(x), qres.vars))
                writer = csv.DictWriter(csv_file, fieldnames=header)
                writer.writeheader()
                for row in qres:
                    d = {}
                    tmp = list(map(lambda x: str(x), row))
                    for elem, name in zip(tmp, header):
                        d[name] = elem
                    writer.writerow(d)

        
if __name__ == "__main__":
    arguments = sys.argv
    
    s = Sparql(arguments[1], arguments[2])
    if len(arguments) == 4:
        s.execute(arguments[3])
    else:
        s.execute()
