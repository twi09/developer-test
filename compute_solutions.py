'''
This script contains the function needed to compute the probability of sucess
''' 

import numpy as np 

# Compute the probability from the total number of time meet bounty hunters 
compute_probability = lambda nb_total_meet : sum(((9**(k-1))/ 10**(k)) for k in range(1,nb_total_meet+1)) if nb_total_meet!=0 else 0



# Remove paths that contains endor in the path in progress
def remove_valid(paths,Return_path,node_to_end) :
    # Visit all the possible paths and remove valid solutions from path in progress
    copy_paths = paths.copy()
    for i in range(len(copy_paths)):
        if (node_to_end in copy_paths[i][0]) :
            paths.remove(copy_paths[i])
            Return_path.append(copy_paths[i])
        

# Compute valid solutions from a current path 
def compute_new_paths(current_path,neight_nodes,costs_nh,autonomy_default,countdown,bounty_hunters) :     
    # Store the valid paths 
    new_path = []
    # test all the possibe neighbors
    for i in range(len(neight_nodes)) :
        # if enough autonomy an before countdown, travel and autonomy = autonomy - nb_day_to_travel
        if current_path[1][0] >=  costs_nh[i]  and current_path[1][1] + costs_nh[i] <= countdown : 
            autonomy = current_path[1][0] - costs_nh[i] 
            # number of days = number of days + time to travel 
            nb_of_days = current_path[1][1]+costs_nh[i]
            # if nb_of_days correponds to a number of day where bounty hunters are in a given planet 
            if nb_of_days in bounty_hunters.keys() : 
                # Iterate number of time meet bounty hunters (+1 if meet else 0)
                nb_bounty_meet = current_path[1][2]+ int(bounty_hunters[int(nb_of_days)] == neight_nodes[i])
            else : 
                # nothing to meet ! 
                nb_bounty_meet = current_path[1][2] 
            # if travel on the same planet (=wait on the planet)
            if neight_nodes[i] == current_path[0][-1] :
                # Then back to default autonomy 
                autonomy = autonomy_default
            new_path.append([current_path[0] + [ neight_nodes[i] ], [autonomy,nb_of_days,nb_bounty_meet]])
            
        
            
    # if empty autonomy and before countdown then need to refuel
    if current_path[1][0]==0 and current_path[1][1] +  1 <= countdown : 
        # number of days = number of days + time to refuel (=1)
        nb_of_days = current_path[1][1]+ 1
        # autonomy is reset to default 
        autonomy = autonomy_default 
        # if nb_of_days correponds to a number of day where bounty hunters are in a given planet 
        if nb_of_days in bounty_hunters.keys() : 
            # Iterate number of time meet bounty hunters (+1 if meet else 0)
            nb_bounty_meet = current_path[1][2]+ int(bounty_hunters[int(nb_of_days)] == current_path[0][-1])
        else : 
            # nothing to meet ! 
            nb_bounty_meet = current_path[1][2] 
        # Append only the refuel solution (stay on the same planet = repeat the last node of the path)
        new_path.append([current_path[0] + [ current_path[0][-1] ], [autonomy,nb_of_days,nb_bounty_meet]])

    return(new_path)




def compute_paths(G,autonomy_default,countdown,node_to_start,node_to_end,bounty_hunters,dico_planet_to_index) : 
    '''
    Function that compute valid paths 
    
    Parameters: 
    --------------------
    G : A graph defined as a np array, ex : G = np.array([[1,6,6,inf],[inf,1,1,4],[inf,inf,1,1],[inf,inf,inf,inf]])
    autonomy_default : The autonomy of the Millennium Falcon 
    countdown : deadline to boom
    node_to_start : The planet where the Millennium Falcon is initialy 
    node_to_end : The planet to go (end of the path)
    bounty_hunters : dictionary of day:planet where the bounty_hunters are, ex : bounty_hunters = {6:"Hoth",7:"Hoth",8:"Hoth"}
    dico_planet_to_index : dictionary that map the planet to the corresponding index in the graph, ex : dico_planet_to_index = {"Tatouine":0,"Dagobah":1,"Hoth":2,"Endor":3}
    '''
    
    # Dictionary that map index to planet 
    dico_index_to_planet = {v: k for k, v in dico_planet_to_index.items()}
    # nb_of day as init
    nb_of_days_init = 0 
    # count number of time meet bounty_hunters init
    nb_bounty_meet_init = 0 
    
    # List with current paths, a path is defined as follow: [[nodes1,nodes2,...],[autonomy,nb_of_days,nb_bounty_meet]], init with the first node
    Paths_in_progress=[[[node_to_start],[autonomy_default,nb_of_days_init,nb_bounty_meet_init]]]
    # List that contains the valid solutions 
    Return_path = []
    
    
    while Paths_in_progress!=[]  : 
        # Take the path of Paths_in_progress
        current_path =  Paths_in_progress.pop(0)
        # Take the last node of the path 
        last_node = current_path[0][-1]
        
        
        # Costs to add a node that is in the neighborhood of last_node (+remove float_inf cost nodes)
        costs_nh = G[dico_planet_to_index[last_node]]
        
        # Select index of non-inf nodes 
        index_non_inf = np.where(costs_nh!=float("inf"))[0]
        # List of neighborhood nodes (non float_inf cost nodes)
        neight_nodes = [dico_index_to_planet[i] for i in index_non_inf]
        
        # Filter non-inf costs 
        costs_nh = costs_nh[index_non_inf]
        
        # New paths obtained from current_path that are before countdown 
        new_paths = compute_new_paths(current_path,neight_nodes,costs_nh,autonomy_default,countdown,bounty_hunters)
        
        # Add new paths to progess paths list
        Paths_in_progress +=new_paths
        
        # Remove valid solutions in progress paths list
        remove_valid(Paths_in_progress,Return_path,node_to_end)
     
    return(Return_path)


def compute_proba(Return_path) : 
    '''
    Function that compute the probability from valid paths
    '''
    # If not solutions 
    if Return_path==[] : 
        return(0)
    else : 
        # Take path with minimum number of time meet bounty hunters 
        nb_min_meet = min(Return_path,key=lambda x:x[1][2])[1][2]
        return((1-compute_probability(nb_min_meet))*100)
