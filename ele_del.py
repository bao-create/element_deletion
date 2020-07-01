from pyNastran.bdf.bdf import BDF
import numpy as np

num_layers = 10
layer_thickness = .01





model = BDF()
model.read_bdf("very_small_cube200_200_10.bdf", xref=False)
cen_matrix = np.array([])

for eid in model.elements:
    ele = model.elements[eid]
    nodes = ele.nodes
    coord_matrix = np.array([])
    for node in nodes:
        n = model.nodes[node]
        coord = n.xyz
        coord_matrix = np.stack((coord_matrix,coord), axis =1)
    centr = np.mean(coord_matrix, axis=1)/4
    cen_matrix = np.stack((cen_matrix,centr),axis=1)

good_y_vals = 
