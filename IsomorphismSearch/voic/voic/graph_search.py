# from voic import db
# need a dictionary to map EDGEs to (VType1,VType2)

# ev_dict = {"IsParentOf":("Parent","Child"), "IsResidentOf":("Child","State"), "HasExclusiveContinuing":("State","Child"),
# 	   "HasHomeState":("State","Child"), "LivedIn":("Child","State"), "LastStateGreaterThan12":("Child","State")}
ev_dict = {"IsParentOf":("Parent","Child"), "IsClaimantOf":("Parent","Child"), "IsRespondentOf":("Parent","Child"), "IsResidentOf":("Child","State"), "HasExclusiveContinuing":("Parent","Child"), "HasExclusiveContinuingJ":("State","Child"),
	   "HasHomeState":("Parent","Child"), "HasHomeStateJ":("State","Child"), "RetainsJurisdictionOver":("Parent","Child"), "LivesIn":("Child","State"), "LivedIn":("Child","State"), "IsFrom":("Parent","State"),
        "DeferredTo":("State","State"), "Declined":("State","Jurisdiction"), "HasStrongConnection":("Parent","Child"), "Has":("State","Misc")}


def to_GSS_format(g, f_path): # Take a doc graph 'g' and convert it to GSS-readable CSV version.
    
    vevs = g.split(',')
	
    # Just compile a big, "\n"-escaped string and dump it all in at the end.
    with open(f_path, mode="w") as file: # Dump the new graph into the file that we use when calling GSS, whether pattern.txt or target.txt
        
        if (len(g)==0): ### Account for empty document graphs
            file.write("Place>Holder,Is")
            return

        insertion = ""
        insertion_vtypes = ""
        for vev in vevs:
            temp = vev.split('-')
            edge = temp[1] # At index 1, we have the edge.
            graph_line = "{}>{},{}\n".format(temp[0].replace("\"",""),temp[2].replace("\"",""),edge)
            # print(edge)
            vert_types=[]
            try:
                vert_types = ev_dict[edge] # Get the vertex types that we expect with that edge.
                insertion_vtype1, insertion_vtype2 = ["",""] # Init empty
                insertion_vtype1 = "{},,{}\n".format(temp[0],vert_types[0])
                insertion_vtype2 = "{},,{}\n".format(temp[2],vert_types[1])
                insertion_vtypes += insertion_vtype1 + insertion_vtype2
            except:
                pass

            insertion+=graph_line
            
        # Have duplicate types if many edges connected to one node. Remove those redundancies, or does it matter?
        insertion_vtypes = "\n".join(list(set(insertion_vtypes.split("\n")))[1:]) # Sorts alphabetically, incidentally.
        
        # insertion = insertion.replace("\n\n","\n")
        # insertion_vtypes = insertion_vtypes.replace("\n\n", "\n") # FIX THE EXTRA NEWLINE IN (pattern) GRAPHS
        insertion_total = (insertion+insertion_vtypes).replace("\n\n","\n")
        # # print(insertion)
        # # print(insertion_vtypes)
        # file.write(insertion+insertion_vtypes)
        file.write(insertion_total)
        
    return
# ex = 'virginia-HasExclusiveContinuing-fiaa,john-IsParentOf-fiaa'
# to_GSS_format(ex, "pattern.txt")


import os
import subprocess

def subgraph_search(pattern_path="pattern.txt", target_path="target.txt"):
    
	### New procedure to check for constant-to-constant mapping ###
	out = subprocess.check_output(["./glasgow-subgraph-solver/glasgow_subgraph_solver", pattern_path, target_path])
	out = out.decode() # From bytecode to string?
	# print(temp)
	# outs = out.split()
	print(out)
	s = 'status = '
	status_idx = out.find(s)
	tf_dict = {'true':True, 'false':False, 't':True, 'f':False}
	is_match = tf_dict[out[status_idx+len(s)]]
	return is_match

# Extra/improvements
### How to prevent misreading a vertex that happens to be called 'status = '???????
### use `mapping` output from GSS to show what parts of your search graph were matched by the returned target?