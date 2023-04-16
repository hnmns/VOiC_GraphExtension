# from voic import db
# need a dictionary to map EDGEs to (VType1,VType2)
ev_dict = {"IsParentOf":("Parent","Child"), "IsResidentOf":("Child","State"), "HasExclusiveContinuing":("State","Child"),
	   "HasHomeState":("State","Child"), "LivedIn":("Child","State"), "LastStateGreaterThan12":("Child","State")}


def to_GSS_format(g, f_path): # Take a doc graph 'g' and convert it to GSS-readable CSV version.
    vevs = g.split(',')
    # vevs = g
    # print(vevs)
    # Just compile a big, "\n"-escaped string and dump it all in at the end.
    with open(f_path, mode="w") as file: # Dump the new graph into the file that we use when calling GSS
        insertion = ""
        insertion_vtypes = ""
        # constants = [] # verts in ""
        # Need to fix/edit target graphs or the search so that constants are accounted for...
        for vev in vevs:
            temp = vev.split('-')
            graph_line = "{}>{},{}\n".format(temp[0].replace("\"",""),temp[2].replace("\"",""),temp[1])
            edge = temp[1] # At index 1, we have the edge.
            vert_types=[]
            try:
                vert_types = ev_dict[edge] # Get the vertex types that we expect with that edge.
                insertion_vtype1, insertion_vtype2 = ["",""] # Init empty
                if (temp[0][0]!="\"" or temp[0][-1]!="\""): # Check if not constant
                    insertion_vtype1 = "{},,{}\n".format(temp[0],vert_types[0])
                if (temp[2][0]!="\"" or temp[2][-1]!="\""):
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
	out = subprocess.check_output(["./glasgow-subgraph-solver/glasgow_subgraph_solver", pattern_path, target_path])
	out = out.decode() # From bytecode to string?
	# print(temp)
	# outs = out.split()
	s = 'status = '
	status_idx = out.find(s)
	tf_dict = {'true':True, 'false':False, 't':True, 'f':False}
	is_match = tf_dict[out[status_idx+len(s)]]
	return is_match

# Extra/improvements
### How to prevent misreading a vertex that happens to be called 'status = '???????
### use `mapping` output from GSS to show what parts of your search graph were matched by the returned target?