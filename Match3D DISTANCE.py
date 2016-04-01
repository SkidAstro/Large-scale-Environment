import random
import sys
import math
import os.path
import shutil
from datetime import datetime
import networkx as nx

D = math.acos(-1.0) / 180 # acos(-1) = Pi
C = 299792.458
maxL = 1 #Mpc/h

def dist(a, b): ##tuples (x,y) of coordinate 2D
        return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def add_galaxy(filename):
          """Creates a spanning tree of a group of galaxy position data"""
          G=nx.Graph()
          galaxy = open(filename) # File with galaxy data
          # Create nodes in G where each node is a galaxy w/ all associated information
          for line in galaxy:
                  words = line.split()
                  ID = words[0]
                  RA = words[1]
                  Dec = words[2]
                  zRS = words[3]
                  distance = words[4]
                  G.add_node(int(ID), RA = float(RA), Dec = float(Dec), zRS = float(zRS),
                             x = (C*float(zRS)/100*math.cos(D*float(Dec))*math.cos(D*float(RA))),
                             y = (C*float(zRS)/100*math.cos(D*float(Dec))*math.sin(D*float(RA))),
                             z = (C*float(zRS)/100*math.sin(D*float(Dec))), distance = float(distance))
                  
          galaxy.close
          return G

def add_HIgal(filename):
          """Creates a spanning tree of a group of galaxy position data"""
          G=nx.Graph()
          galaxy = open(filename) # File with galaxy data
          # Create nodes in G where each node is a galaxy w/ all associated information
          i = 0
          for line in galaxy:
                  words = line.split()
                  RA = words[0]
                  Dec = words[1]
                  zRS = words[2]
                  logHImassorlim = words[3]
                  massratorlim = words[4]
                  HIDeforlim = words[5]
                  detectionstatus = words[6]
                  density_normalized = words[7]
                  G.add_node(i, RA = float(RA), Dec = float(Dec), zRS = float(zRS),
                             x = (C*float(zRS)/100*math.cos(D*float(Dec))*math.cos(D*float(RA))),
                             y = (C*float(zRS)/100*math.cos(D*float(Dec))*math.sin(D*float(RA))),
                             z = (C*float(zRS)/100*math.sin(D*float(Dec))),
                             logHImassorlim = str(logHImassorlim),
                             massratorlim  = str(massratorlim),
                             HIDeforlim = str(HIDeforlim),
                             detectionstatus = str(detectionstatus),
                             density_normalized = str(density_normalized))
                  i+=1
          print i
          galaxy.close
          return G

def output_text(graph, filename):
        
##        dir_path = os.path.join('output', folder_name, 'galaxy')  # will return 'output/folder_name'
##        if not os.path.isdir(dir_path):
##                os.makedirs(dir_path) # create directory [current_path]/output/folder_name
##        file = open(os.path.join(dir_path, filename + ".txt"), "w")
        file = open(os.path.join(filename + ".txt"), "w")
        i=0 # make counter to avoid end of file empty line
        countMax = graph.number_of_nodes()
        file.write("# ")
        file.write("RA  ")
        file.write("Dec  ")
        file.write("zRS ")
        file.write("distance  ")
        file.write("logHImassorlim  ")
        file.write("massratorlim  ")
        file.write("HIDeforlim  ")
        file.write("detectionstatus  ")
        file.write("density_normalized  \n")
        
        for node in graph:
                file.write(str(graph.node[node]['RA']) + "  ")
                file.write(str(graph.node[node]['Dec']) + "  ")
                file.write(str(graph.node[node]['zRS']) + "  ")
                file.write(str(graph.node[node]['distance']) + "  ")
                file.write(str(graph.node[node]['logHImassorlim']) + "  ")
                file.write(str(graph.node[node]['massratorlim']) + "  ")
                file.write(str(graph.node[node]['HIDeforlim']) + "  ")
                file.write(str(graph.node[node]['detectionstatus']) + "  ")
                file.write(str(graph.node[node]['density_normalized']) + "  ")
                
                i+=1
                if i!= countMax: #check end of file
                        file.write("\n")
        file.close()
        
startTime = datetime.now() # Start timing the script

HIgal = add_HIgal("HIdataText.txt")
gal = add_galaxy("galaxy_full_distance.txt")
finale = nx.Graph()

i = 0
for node1 in HIgal.nodes():
      min = maxL
      status = True
      minDist = 0      
      for node2 in gal.nodes():
##            print dist((HIgal.node[node1]['x'],HIgal.node[node1]['y'],HIgal.node[node1]['z']),
##                    (gal.node[node2]['x'],gal.node[node2]['y'],gal.node[node2]['z']))
            if dist((HIgal.node[node1]['x'],HIgal.node[node1]['y'],HIgal.node[node1]['z']),
                    (gal.node[node2]['x'],gal.node[node2]['y'],gal.node[node2]['z'])) <= min:
                  status = False
                  min = dist((HIgal.node[node1]['x'],HIgal.node[node1]['y'],HIgal.node[node1]['z']),
                    (gal.node[node2]['x'],gal.node[node2]['y'],gal.node[node2]['z']))
                  minDist = gal.node[node2]['distance']
      if(status==False):
            finale.add_node(i, RA = HIgal.node[node1]['RA'], Dec = HIgal.node[node1]['Dec'], zRS = HIgal.node[node1]['zRS'],
                            distance = minDist,
                            logHImassorlim = HIgal.node[node1]['logHImassorlim'],
                            massratorlim  = HIgal.node[node1]['massratorlim'],
                            HIDeforlim = HIgal.node[node1]['HIDeforlim'],
                            detectionstatus = HIgal.node[node1]['detectionstatus'],
                            density_normalized = HIgal.node[node1]['density_normalized'])
            i+=1
      
print i

output_text(finale, "match")

print "\n[Complete]" + "\nThe script took " + str(datetime.now() - startTime) + " to run\n" # Report amt. of time the script took to run
                             

                  

