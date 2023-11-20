import numpy as np
import sys
import os

# ============================================
# Shell:
L  = 1.0              # Length of the squared side of the shell
n  = int(sys.argv[1]) # Number of boundary elements in one of the sides of the shell.
                      # Assuming input is int AND PAIR
N  = (n + 1)*(n + 1)  # Total number of nodes in the shell
nE = 2 * n * n        # Total number of elements in the shell
nB = n                # Total number of boundary elements in the shell

dx = float(L/n)       # Distance between nodes (in the shell)
L  = dx * n           # Reshape lenght of the shell

# ============================================
# Beam:
Lb = 1.0              # Legth of the beam             
m  = int(sys.argv[2]) # Number of boundary elements in the beam. Assuming input is int
                      # Number of extra nodes for the beam is equal to m. Note that one
                      # of the nodes already exists
nBb = 0               # Number of boundary elements added due to the beam
dxm = float(Lb / m)   # Distance between nodes (in the shell)
Lb  = dxm * m         # Reshape lenght of the domain


meshdir = 'newmesh' 
os.system('rm -rf ' + meshdir)
os.mkdir(meshdir)

# ===========================================================================================
# Write the header file and write info there:
headerFile = open(meshdir + '/mesh.header', 'w')

headerFile.write(str(N + m) + ' ' + str(nE + m) + ' ' + str(nB + nBb) + '\n')
if nBb != 0:
    headerFile.write('3\n')
    headerFile.write('101 ' + str(nBb) + '\n')
else:
    headerFile.write('2\n')
headerFile.write('202 ' + str(nB + m) + '\n')
headerFile.write('303 ' + str(nE) + '\n')


# ===========================================================================================
# Now write the nodes in the mesh.node file:
nodesFile = open(meshdir + '/mesh.nodes', 'w')

# Write the first four nodes:
nodesFile.write('1 1 0 0 0\n')
nodesFile.write('2 1 ' + str(L) + ' 0 0\n')
nodesFile.write('3 1 ' + str(L) + ' ' + str(L) + ' 0\n')
nodesFile.write('4 1 0 ' + str(L) + ' 0\n')

# Set counter of nodes for shell nodes:
node_id = 4
         
for ii in np.arange(1, n, 1):
    node_id += 1  # Update counter
    x = ii * dx # Calculate x coordinate
    nodesFile.write(str(node_id) + ' 1 ' + str(x) + ' 0 0\n' )

for jj in np.arange(1, n, 1):
    for ii in np.arange(0, n+1, 1):
        node_id += 1
        x = ii * dx
        y = jj * dx
        nodesFile.write(str(node_id) + ' 1 ' + str(x) + ' ' + str(y) + ' 0\n' )

for ii in np.arange(1, n, 1):
    node_id += 1  # Update counter
    x = ii * dx # Calculate x coordinate
    nodesFile.write(str(node_id) + ' 1 ' + str(x) + ' ' + str(L) + ' 0\n' )

# Now write the beam nodes:
node_id += 1  # Update counter
nodesFile.write(str(node_id) + ' 1 ' + str(L) + ' ' + str(L/2.) + ' ' + str(Lb) + '\n')

for ii in np.arange(1, m, 1):
    node_id += 1 # Update counter
    z = ii * dxm # Coordinate z  
    nodesFile.write(str(node_id) + ' 1 ' + str(L) + ' ' + str(L/2.) + ' ' + str(z) + '\n')

# Close the node file:
nodesFile.close()


# ===========================================================================================
# Now write the elements:
elementsFile = open(meshdir + '/mesh.elements', 'w')

# Write first 2 elements:
elementsFile.write('1 1 303 1 5 ' + str(4 + n) + ' \n')
elementsFile.write('2 1 303 5 ' + str(4 + n + 1) + ' ' + str(4 + n) + ' \n')

# set count of elements
element_id = 2

# Write the elements in the shell between the two first lines of nodes:
# ---------------------------------------------------------------------
for ii in np.arange(2, n, 1):
    
    # Set the ids of the nodes in the corresponding cell
    n1 = 4 + ii -1 # 4 nodes are the corners of the plate. Next node is 5, then 6,...
    n2 = n1 + 1 #4 + ii
    n3 = n2 + n #4 + n + ii
    n4 = n3 - 1 #4 + n + ii - 1

    # Write elements:
    element_id += 1
    elementsFile.write(str(element_id) + ' 1 303 ' + str(n1) + ' ' + str(n2) + ' ' + str(n4) + '\n')
    element_id += 1
    elementsFile.write(str(element_id) + ' 1 303 ' + str(n2) + ' ' + str(n3) + ' ' + str(n4) + '\n')

# Write last 2 elements in the line:
element_id += 1
elementsFile.write(str(element_id) + ' 1 303 ' + str(4 + n - 1) + ' 2 ' + str(4 + 2*n - 1) + ' \n')
element_id += 1
elementsFile.write(str(element_id) + ' 1 303 2 ' + str(4 + 2*n) + ' ' + str(4 + 2*n - 1) + ' \n')


# Write the next lines until last one (still shell)
# ---------------------------------------------------------------------
for jj in np.arange(0, n-2, 1):
    for ii in np.arange(0, n, 1):
        n1 = 4 + n + jj*(n + 1) + ii
        n2 = n1 + 1 
        n3 = n2 + n + 1
        n4 = n3 - 1

        element_id += 1
        elementsFile.write(str(element_id) + ' 1 303 ' +
                           str(n1) + ' ' +
                           str(n2) + ' ' +
                           str(n4) + ' \n')
        element_id += 1
        elementsFile.write(str(element_id) + ' 1 303 ' +
                           str(n2) + ' ' +
                           str(n3) + ' ' +
                           str(n4) + ' \n')

# Last line is special (still shell):
# ---------------------------------------------------------------------
# Within this line, the first case is also special:
n1 = 4 + n + (n - 2)*(n + 1)
n2 = n1 + 1 
n3 = n2 + n
n4 = 4

element_id += 1
elementsFile.write(str(element_id) + ' 1 303 ' +
                   str(n1) + ' ' +
                   str(n2) + ' ' +
                   str(n4) + ' \n')
element_id += 1
elementsFile.write(str(element_id) + ' 1 303 ' +
                   str(n2) + ' ' +
                   str(n3) + ' ' +
                   str(n4) + ' \n')

# Now the cases within the first and the last ones:
for ii in np.arange(1, n-1, 1):
    n1 = 4 + n + (n - 2)*(n + 1) + ii
    n2 = n1 + 1 
    n3 = n2 + n
    n4 = n3 - 1

    element_id += 1
    elementsFile.write(str(element_id) + ' 1 303 ' +
                       str(n1) + ' ' +
                       str(n2) + ' ' +
                       str(n4) + ' \n')
    element_id += 1
    elementsFile.write(str(element_id) + ' 1 303 ' +
                       str(n2) + ' ' +
                       str(n3) + ' ' +
                       str(n4) + ' \n')

# And the last two elements:
n1 = 4 + n + (n - 2)*(n + 1) + n - 1
n2 = n1 + 1 
n3 = 3
n4 = n2 + n - 1

element_id += 1
elementsFile.write(str(element_id) + ' 1 303 ' +
                   str(n1) + ' ' +
                   str(n2) + ' ' +
                   str(n4) + ' \n')
element_id += 1
elementsFile.write(str(element_id) + ' 1 303 ' +
                   str(n2) + ' ' +
                   str(n3) + ' ' +
                   str(n4) + ' \n')

# Now write elements in the beam
# ------------------------------------------------------------

# First element:
element_id += 1
connection_node = 4 + (n-1) + (n+1) * int(n/2) 
first_beam_node = N + 2
last_beam_node  = N + 1
elementsFile.write(str(element_id) + ' 2 202 ' +
                       str(connection_node) + ' ' +
                       str(first_beam_node) + ' \n')

# Rest of elements except last one:
for ii in range(m-2):    
    element_id += 1
    elementsFile.write(str(element_id) + ' 2 202 ' +
                       str(first_beam_node + ii) + ' ' +
                       str(first_beam_node + ii + 1) + ' \n')

# Last element:
element_id += 1
elementsFile.write(str(element_id) + ' 2 202 ' +
                       str(N + m) + ' ' +
                       str(last_beam_node) + ' \n')

# Close the file:
elementsFile.close()


# ===========================================================================================
# Write the boundary elements:
# Now write the elements:
boundaryFile = open(meshdir + '/mesh.boundary', 'w')

boundary_id = 1
for ii in range(n):
    
    boundary_el = ii + 1
    parent_el = 2*n * (n - ii) - 2*(n - 1) - 1
    
    if ii == 0:
        node_0 = 4
        node_1 = (n + 1)*(n + 1) - ((n - 2) + n + 1)
    elif ii == n - 1:
        node_0 = (n + 1)*(n + 1) - ((n - 2) + (n + 1) * ii)
        node_1 = 1
    else:
        node_0 = (n + 1)*(n + 1) - ((n - 2) + (n + 1) * ii)
        node_1 = node_0 - (n + 1)
        
    boundaryFile.write(str(boundary_el) + ' ' +
                       str(boundary_id) + ' ' +
                       str(parent_el) +
                       ' 0 202 ' +
                       str(node_0) + ' ' + str(node_1) + '\n')

boundaryFile.close()
