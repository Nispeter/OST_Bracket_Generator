import random
import tkinter as tk




class Node:
    def __init__ (self,game):
        self.game = game
        self.l = None
        self.r = None

def generate_bracket(games):
    if not games:
        return None
    
    nodes = [Node(game) for game in games]

    while len(nodes) > 1:
        next_round = []
        for i in range (0, len(nodes),2):
            game1 = nodes[i]
            game2 = nodes[i+1]

            #opt = input(f"{game1.game} vs {game2.game}")
            opt = random.randint(0,1)
            parent = Node(nodes[i+opt].game)
            parent.l = game1
            parent.r = game2

            next_round.append(parent)
        
        nodes = next_round

    return nodes[0]

def print_tree(node,level):
    if (node):

        print_tree(node.l, level+1)
        print("            " * level + node.game)
        print_tree(node.r, level+1)  


with open("output.txt", "r") as file:
    games= file.readlines()

#games = ['a','b','c','d','e','f','g','h']
root = generate_bracket(games)
print_tree(root,0)
