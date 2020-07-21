from numpy.lib.function_base import append
from pyNastran.bdf.bdf import BDF
import numpy as np
from pyNastran.bdf.mesh_utils import bdf_renumber

num_layers = 10
layer_thickness = .09
build_axis = 2 #1,2,3 -> x,y,z
tol = .001 #tolerance of element existing on the layer transition
porosity = .005



model = BDF()
model.read_bdf("very_small_cube200_200_10.bdf", xref=False) #read in the BDF file, no cross referencing
cen_matrix = np.empty([len(model.elements),4]) # init a empty array to hold centroids 
i = 0
for eid in model.elements: #iterate through elements
    
    ele = model.elements[eid]
    nodes = ele.nodes #extract the nodes from each element
    coord_matrix = np.empty([len(nodes),3])
    j = 0
    for node in nodes: # for each element, 
        n = model.nodes[node]
        coord = n.xyz #look up the node
        coord_matrix[j,:] = coord #add its coordinates to a matrix of coordinates for that element
        j += 1

    centr = np.mean(coord_matrix, axis=0) #find the centroid of the element

    centr_eid = np.append(centr,eid) #adds the eid as a 4th column
    cen_matrix[i,:] = centr_eid #append to master centroid list
    i += 1 

layer_vals = np.arange(layer_thickness,num_layers * layer_thickness,layer_thickness) #find all of the position values of the layer interfaces
layer_elements = []


for cen in cen_matrix: 
    good_ele_flag = False
    dim = 0
    for ax in cen:
       dim += 1
       if dim == build_axis:
           current_centroid_check = np.where(np.logical_and(layer_vals<=(ax*(1+tol)),layer_vals > (ax*(1-tol)))) #checks if current build axis value, in the current 
           #centroid is in the tolerance of the layer tranisiton. outputs tuple type
           if current_centroid_check[0].size != 0: #checks to see if the value was in the range specifed by layer_vals
               good_ele_flag = True
       elif dim == 4 and good_ele_flag:
            layer_elements.append(ax)

           
number_to_delete = round(len(model.elements)*porosity) #calculates the number of elements to delete based on the porosity, assumes all holes in layer transition

eles_to_delete = np.random.choice(layer_elements,number_to_delete,replace=False) #samples uniformly without replacement
print(len(model.elements))
for i in eles_to_delete:
    del model.elements[int(i)] #deletes requires elements 
print(len(model.elements))

model.write_bdf("very_small_cube_pores.bdf") #writes the bdf without the elements 
bdf_renumber("very_small_cube_pores.bdf","very_small_cube_pores_seq.bdf")