"""
Le but de ce sujet est de simuler la propagation d'un feu de forêt en fonction du vent.
Le terrain est décrit par une carte carrée, représentée par une grille de cases.
Certaines de ces cases ne contiennent aucune matière combustible et sont donc des obstacles pour le feu.
et la case jaune représente le départ de feu.
Le feu se déplace dans les quatre directions (haut, bas, gauche, droite),
d'une case par tour, jusqu'à rencontrer des obstacles.

L'objectif est d'écrire un programme qui indique à quelle tour chaque case de la forêt suivante va brûler 
"""

import random as rd
import tkinter as tk

grid_size = 50  # Taille de la grille 
square_size =  5 # Taille de chaque carré
fire_day=0
adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
open_list=[]

def generate_red_gradient(start_color, end_color, steps):
    start_r = int(start_color[1:3], 16)
    start_g = int(start_color[3:5], 16)
    start_b = int(start_color[5:7], 16)
    
    end_r = int(end_color[1:3], 16)
    end_g = int(end_color[3:5], 16)
    end_b = int(end_color[5:7], 16)
   
    gradient = []
    
    for step in range(steps):
        r = start_r + (end_r - start_r) * step // (steps - 1)
        g = start_g + (end_g - start_g) * step // (steps - 1)
        b = start_b + (end_b - start_b) * step // (steps - 1)
        
        gradient.append(f"#{r:02x}{g:02x}{b:02x}")
    return gradient

def create_color_grid(canvas, grid_size, square_size,maze,colors_fire):
    #grille à partir du maze
    for row in range(grid_size):
        for col in range(grid_size):
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            color=colors_fire[maze[row][col]]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

def create_maze(longth, length):
    lst=[]
    for i in range(longth):
        lst2=[]
        nb=-2
        for j in range(length):
            nb=-2 if rd.random()>.7 else -1
            lst2.append(nb)
        lst.append(lst2)
    return lst

#find Possible solutions in open list
def find_sol(open_list,fire_d):
    new_list=[]
    for node in open_list:	
        for new_pos in adjacent_squares:
            # Get node position
            node_pos = (node[0] + new_pos[0],node[1] + new_pos[1])

            # Make sure within range
            if node_pos[0] > (len(maze) - 1) or node_pos[0] < 0 or node_pos[1] > (len(maze[len(maze) - 1]) - 1) or node_pos[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_pos[0]][node_pos[1]] != -2 and maze[node_pos[0]][node_pos[1]]==-1:
                maze[node_pos[0]][node_pos[1]]=fire_d
                new_list.append(node_pos)
    return(new_list)

def find_fire_source(x,y):
        lst=[]
        for i in range(x):
            for j in range(y):
              if maze[i][j]==-1:
                lst.append(tuple(list((i,j))))    
        return(lst)
        
def on_click(event, canvas):
    global open_list,fire_day,grid_size,maze
    while open_list:
        fire_day+=1
        open_list=find_sol(open_list,fire_day)
        print('day',fire_day)
    colors_fire=create_color_fire(fire_day+1)    
    create_color_grid(canvas, grid_size, square_size,maze,colors_fire)
    canvas.pack()

def create_color_fire(max):
    colors_list = generate_red_gradient("#CAFF70", "#FF6800", max)
    colors_fire=dict(zip([i for i in range(1,max)],colors_list))
    colors_fire[-2]='grey'
    colors_fire[-1]='green'
    colors_fire[0]='red'
    return colors_fire

maze=create_maze(grid_size,grid_size)
fire=find_fire_source(grid_size,grid_size)
fire_source=[8,10]
maze[fire_source[0]][fire_source[1]]=fire_day    
colors_fire=create_color_fire(100)
open_list=[fire_source]

root = tk.Tk()
root.title("Feu de forêt !")

# Création du canvas pour dessiner
canvas = tk.Canvas(root, width=grid_size * square_size, height=grid_size * square_size)
canvas.pack()
canvas.bind("<Button-1>", lambda event: on_click(event, canvas))
    

# Création de la grille de feu
create_color_grid(canvas, grid_size, square_size,maze,colors_fire)

# Lancement de la boucle principale de Tkinter
root.mainloop()
    
    
 
