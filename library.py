# pylint:disable=no-member
import os
from itertools import combinations
import apex
import pandas as pd

def truss_sketch(model, points: list):
    part = model.createPart()
    sketch = part.createSketchOnGlobalPlane(name='Sketch 1', plane=apex.construct.GlobalPlane.XY, alignSketchViewWithViewport=False)
    
    for i_point, j_point in combinations(points, 2):
        point_list = [apex.construct.Point2D(i_point[0], i_point[1]), apex.construct.Point2D(j_point[0], j_point[1])]
        sketch.createPolyline(name='', points=point_list)

    return sketch.completeSketch(fillSketches=False)

def find_constraint_nodes(nodes) -> list:    
    node_xy = pd.DataFrame({'x': [node.coordinates.x for node in nodes], 'y': [node.coordinates.y for node in nodes]})
    constraints = node_xy[((node_xy['x']==round(node_xy['x'].min(), 2)) & (node_xy['y']==round(node_xy['y'].min(), 2))) | ((node_xy['x']==round(node_xy['x'].max(), 2)) & (node_xy['y']==round(node_xy['y'].min(), 2)))]

    constraint_nodes = []
    for idx in constraints.index:
        constraint_nodes.append(apex.mesh.NodeCollection())
        constraint_nodes[-1].append(nodes[idx])    

    return constraint_nodes

def find_load_nodes(nodes) -> list:  
    node_xy = pd.DataFrame({'x': [node.coordinates.x for node in nodes], 'y': [node.coordinates.y for node in nodes]})
    lodes = node_xy[((node_xy['x']==node_xy['x'].max()) & (node_xy['y']==node_xy['y'].max()))]

    load_nodes = []
    for idx in lodes.index:
        load_nodes.append(apex.mesh.NodeCollection())
        load_nodes[-1].append(nodes[idx])    

    return load_nodes
    
def get_unused_name(name, path):
    """Finds a nonexistant filename by adding/incrementing a suffix
    
    Parameters
    ----------
    name : str
        Desired base model name.
    path : str
        Directory in which model will be saved.
    
    Returns
    -------
    str
        Unused model name.

    """
    if os.path.exists(os.path.join(path, name)) is False:
        new_name = name
    
    else:
        found = False
        suffix = 1
        while found is False:
            name_inc = f'{name}_{suffix}'
            if os.path.exists(os.path.join(path, name_inc)) is False:
                new_name = name_inc
                found = True
            else:
                suffix += 1
    
    return new_name
