from __future__ import with_statement
import os.path
import csv
#import opensim 
  

#f = path to template file
#outF = path to save output 

def vec2ls(v):
#	# converts an opensim vector 3 v to a python collection
	ls = [v.get(0), v.get(1), v.get(2)] 	
	return ls
	
# vars  
coords = []
names = []
lines = []

# Get current model
osimModel = getCurrentModel()
# marker set
mkr = osimModel.getMarkerSet()


# init system so we get a state (needed to get coords)
sZero = osimModel.initSystem()

for i in range(mkr.getSize()):
	foo = mkr.get(i)
	loc = foo.getLocationInGround(sZero)
	coords.append(vec2ls(loc))	
	# get starting coordinates as a float/ normal vector
	names.append(str(foo.getName()))
	

#%%

with open(f) as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for l in tsvreader:
        lines.append(l)
        

#%%        
numFrames = int(lines[-1][0]) 
numMarkers = len(names)
lines[0][3] = outF # correct the file path 
lines[2][3] = str(numMarkers)
header = lines[3][:2]
dim = lines[4][:2]

for n in range(len(names)):
    header.extend([names[n], '', ''])
    dim.extend(['X'+str(n+1), 'Y'+str(n+1), 'Z'+str(n+1)])
    
lines[3] = header
lines[4] = dim


#%%
currentNumFrames = 151
#len(lines)-6
data = []

for c in coords:
    data.extend([str(c[0]*1000), str(c[1]*1000), str(c[2]*1000)])
    
    
#%%
for i in range(currentNumFrames):
    ln = lines[6+i][:2]
    ln.extend(data)
    lines[6+i] = ln
    

#%% 

with open(outF, 'wb') as ff:
    writer = csv.writer(ff,delimiter='\t')
    writer.writerows(lines)
	

	

 
