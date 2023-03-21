import numpy as np 

'''
This script aim to understand the problem on a toy graph
'''

inf = float("inf")

# Example of graph 
G = np.array([[1,6,6,inf],[inf,1,1,4],[inf,inf,1,1],[inf,inf,inf,1]])

# Autonomy of  Millennium Falcon
autonomy = 6
# Deadline annihilation
countdown = 7 

# List of tuples (planet,day)
Bounty_hunters = [("Hoth",6),("Hoth",7),("Hoth",8)]

# Dictionary that map planets to index in G 
dico_planet_to_index = {"Tatouine":0,"Dagobah":1,"Hoth":2,"Endor":3}

# Dictionary that map index to planet 
dico_index_to_planet = {v: k for k, v in dico_planet_to_index.items()}

'''
Write a script that enumerate all the paths from Tatoine to Endor and filter based on a condition
'''

# Remove paths based in Paths_in_progress on a condition 
# To test: Condition = endor visited or cycle of size 3 
def test_remove(paths,Return_path,Trash) :
    # Visit all the possible paths and remove pathes that not match condition 
    copy_paths = paths.copy()
    for e in copy_paths:
        # Number of duplicate values in a path
        unique,counts = np.unique(e,return_counts=True)
        if ("Endor" in e) :
            paths.remove(e)
            Return_path.append(e)
        
        elif 3 in counts :
            paths.remove(e)
            Trash.append(e)



# List with current paths, init with the first node
Paths_in_progress=[["Tatouine"]]
# List that contains the valid solutions 
Return_path = []
# List of invalid paths
Trash = []

# Test on a small number of iter 
for i in range(18) :
    # Take the path of Paths_in_progress
    current_path =  Paths_in_progress.pop(0)
    # Take the last node of the path 
    last_node = current_path[-1]
    
    # Costs to add a node that is in the neighborhood of last_node
    costs_nh = G[dico_planet_to_index[last_node]]
    
    # List of neighborhood nodes (non float_inf cost nodes)
    neight_nodes = [dico_index_to_planet[i] for i in np.where(costs_nh!=float("inf"))[0]]
    
    # New paths obtained by adding neighborhood nodes
    new_paths = [current_path + [neight_nodes[i]] for i in range(len(neight_nodes))]
    
    # Remove invalid nodes and valid nodes in new_paths
    test_remove(new_paths,Return_path,Trash)
 
    
    # Add remaining path
    Paths_in_progress +=new_paths
    

