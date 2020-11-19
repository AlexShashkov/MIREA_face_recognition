import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class TreeBuilder:
    def __init__(self, collisions):
        self.collisions = collisions
        
    def build(self):
        tree = self.buildTree(self.collisions)
        return self.buildGraph(tree)

    def buildGraph(self, tree):
        plt.clf()
        df = pd.DataFrame({ 'from':tree[0], 'to':tree[1]})
        # Build your graph
        G=nx.from_pandas_edgelist(df, 'from', 'to')
        nx.draw(G, with_labels=True, node_size=3000, node_color="skyblue", pos=nx.spring_layout(G), )
        plt.title("Контактировали между собой")

        return plt


    def buildTree(self, registered_collisions):
        result = []
        checked = []
        for index in range(len(registered_collisions)):
            pro = []
            for item in registered_collisions[index].collided_with:
                if item != None and item != index:
                    if f"{index}-{item}" not in checked and f"{item}-{index}" not in checked:
                        checked.append(f"{index}-{item}")
                        pro.append(f"{item}")
            result.append([f"{index}", pro])

        frm = []
        to = []
        for item in result:
            for i in range(len(item[1])):
                frm.append(item[0])
                to.append(item[1][i])

        return (frm, to)

    def breadthFirstSearch(self, tree, index, distance=0, exclude = []):
        dist = distance
        path = []
        exc = exclude
        result = None
        dist += 1
        if index in tree:
            return [dist, path]
        for item in tree:
            if tree.index(item) != len(tree)-1 and item not in exc and item != None:
                exc.append(item)
                result = self.breadthFirstSearch(self.collisions[item].collided_with, index, dist, exc)
                if result != None:
                    return result

        return None

    def findConnected(self, tree, result = [], cont=True):
        result = result
        for item in tree:
            if item not in result and item != None:
                result.append(item)
                if cont:
                    result = self.breadthFirstSearch(self.collisions[item].collided_with, result, False)

        return result