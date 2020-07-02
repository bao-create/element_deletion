from pyNastran.bdf.bdf import BDF
import numpy as np

num_layers = 10
layer_thickness = .01





model = BDF()
model.read_bdf("very_small_cube200_200_10.bdf", xref=False) #read in the BDF file, no cross referencing
cen_matrix = np.array([]) # init a empty array to hold centroids 

for eid in model.elements: #iterate through elements
    ele = model.elements[eid]
    nodes = ele.nodes #extract the nodes from each element
    coord_matrix = np.array([])
    for node in nodes: # for each element, 
        n = model.nodes[node]
        coord = n.xyz #look up the node
        coord_matrix = np.stack((coord_matrix,coord), axis =1) #add its coordinates to a matrix of coordinates for that element
    centr = np.mean(coord_matrix, axis=1)/4 #find the centroid of the element
    cen_matrix = np.stack((cen_matrix,centr),axis=1) #append to master centroid list

good_y_vals = np.arange(layer_thickness,num_layers * layer_thickness,layer_thickness) #find all of the values of the layer interfaces

