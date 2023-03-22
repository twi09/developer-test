# import functions to compute the result 
from compute_solutions import compute_paths,compute_proba,give_me_the_odds_from_files
import json
import sqlite3
import os
import numpy as np 
import sys

def give_me_the_odds(path_milenium,path_empire) : 
    """
    Function that takes the paths of .json files and returns the odds 
    
    Parameters
    ------
    path_milenium : path of the milenium-falcon.json file
    path_empire : path of the empire.json file 
    """
    
    # Load .json for milenium info 
    with open(path_milenium) as f:
        data_milenium = json.load(f)
    # Load .json for empire info 
    with open(path_empire) as f:
        data_empire = json.load(f) 
    
    # Load the database with the routes  
    routes_path = os.path.dirname(path_milenium) + "/" + data_milenium["routes_db"]

    print(give_me_the_odds_from_files(data_milenium,data_empire,routes_path))
    
#path_milenium = "examples/example2/millennium-falcon.json"
#path_empire = "examples/example2/empire.json" 


give_me_the_odds(sys.argv[1],sys.argv[2]) 
    
