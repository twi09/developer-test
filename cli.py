# import functions to compute the result 
from compute_solutions import compute_paths,compute_proba
import json
import sqlite3
import os
import numpy as np 
import sys

def load_graph_from_route(routes_table):
    """
    Function that transform the route_table into an adjacency matrix 
    """
    
    
    # List of planet names starts  
    planets_start = [x[0] for x in routes_table] 
    # List of planet names ends
    planets_ends = [x[1] for x in routes_table] 
    # Set of unique planets 
    set_unique_planets = set(planets_start + planets_ends)
    # Number of different planets 
    nb_planet = len(set_unique_planets)
    # Dico planet to index in the graph 
    dico_planet_to_index = dict(zip(set_unique_planets,[i for i in range(nb_planet)]))
    
    # Init an adjacency matrix 
    G = np.zeros((nb_planet,nb_planet)) + float("inf")
    
    # Each node can cyle on itself with a cost of 1 (refuel or wait)
    np.fill_diagonal(G, 1)
    
    # Fill the matrix by visiting each edge
    for edge in routes_table : 
        start_node_index,end_node_index,cost = dico_planet_to_index[edge[0]],dico_planet_to_index[edge[1]], edge[2]
        G[start_node_index,end_node_index] = cost
    
    return(G,dico_planet_to_index)
    


def give_me_the_odds(path_milenium,path_empire) : 
    
    """
    Function that takes the paths of .json files and returns the odds 
    """
    
    # Load .json for milenium info 
    with open(path_milenium) as f:
        data_milenium = json.load(f)
    # Load .json for empire info 
    with open(path_empire) as f:
        data_empire = json.load(f) 
        
    # Load the database with the routes  
    routes_path = os.path.dirname(path_milenium) + "/" + data_milenium["routes_db"]

    # Connect to the database 
    conn = sqlite3.connect(routes_path)
    # Create a cursor object
    c = conn.cursor()
    # Execute a SQL query to retrieve the ROUTES table 
    c.execute("SELECT * FROM ROUTES")
    # Fetch the results
    routes_table = c.fetchall()
    # Close the cursor and connection
    c.close()
    conn.close()


    # Define variables from .json files
    autonomy_default = data_milenium["autonomy"]
    countdown = data_empire["countdown"]
    node_to_start = data_milenium["departure"]
    node_to_end = data_milenium["arrival"]
    # load as a dictionary day:planet
    bounty_hunters = {data_empire["bounty_hunters"][i]["day"] : data_empire["bounty_hunters"][i]["planet"] for i in range(len(data_empire["bounty_hunters"])) }
    
    # Load the routes table as an adjacency matrix 
    G,dico_planet_to_index = load_graph_from_route(routes_table)
    
    # Compute valid solutions 
    Return_path = compute_paths(G,autonomy_default,countdown,node_to_start,node_to_end,bounty_hunters,dico_planet_to_index)
    
    print(compute_proba(Return_path))
    
#path_milenium = "examples/example2/millennium-falcon.json"
#path_empire = "examples/example2/empire.json" 


give_me_the_odds(sys.argv[1],sys.argv[2]) 
    
