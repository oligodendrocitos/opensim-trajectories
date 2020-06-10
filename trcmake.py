from __future__ import with_statement
import os.path
import csv
import math
#import opensim 


class StartPose:

    def __init__(self, osimModel):
        self.coords = [] # list of marker coordinates
        self.names = []  # list of marker names
        self.lines = []  # lines in final file
        self.data = []   # list of final coordinates
		self.mkr = osimModel.getMarkerSet()
		# 
        self.coordsPrime = None
        self.sPrime = None
		self.namesPrime = [] # to sanity check whether both sets would have the same markers...

        self.trajectories = {}
        # Get marker set from model
        
        # init system so we get a state (needed to get coords)
        self.sZero = osimModel.initSystem()
        for i in range(self.mkr.getSize()):
            foo = self.mkr.get(i)
            loc = foo.getLocationInGround(self.sZero)
            self.coords.append(vec2ls(loc))  
            # get starting coordinates as a float/ normal vector
            self.names.append(str(foo.getName()))
              
    def setTarget(self, osimModel):
        mkr = osimModel.getMarkerSet()
        self.coordsPrime = []
        self.sPrime = osimModel.initSystem()
        for i in range(mkr.getSize()):
            foo = mkr.get(i)
            loc = foo.getLocationInGround(self.sPrime)
            self.coordsPrime.append(vec2ls(loc))  
            # get starting coordinates as a float/ normal vector
            self.namesPrime.append(str(foo.getName()))
        
    def createStaticData(self, nFrames):
        """ 
        Static data consists of existing coordinates converted to millimeters
        """
        data_line = []
        for c in self.coords:
            data_line.extend([str(c[0]*1000), str(c[1]*1000), str(c[2]*1000)])
        
        self.data = [data_line for i in range(nFrames)]
        
    def createTrajectories(self, nFrames):
        # how many markers are there?
        m = len(self.coords)
        c = [i for i in range(m) if self.names[i]==self.namesPrime[i] ]
        if len(c)<len(self.names):
            print('Some markers not present in both models and will be excluded')

        for i in c:
            # convert to mm
            p0 = mTOmm(self.coords[i])
            p1 = mTOmm(self.coordsPrime[i])
            # generate trajectory
            t = lerp3(p0, p1, nFrames)
            self.trajectories[self.names[i]] = t
                  
    def prepareFileTemplate(self, filename, nFrames, nMarkers):
        """
        Prepare the header and layout of the target .trc file
        filename : target filename
        nFrames : number of frames desired
        nMarkers : number of markers in model
        """
        nMarkers = len(self.trajectories.keys())
        names = self.trajectories.keys()
        self.lines[0] = ['PathFileType', '4', '(X/Y/Z)', filename, '', '', '', '']
        self.lines[1] = ['DataRate', 'CameraRate', 'NumFrames', 'NumMarkers',                        
                        'Units', 'OrigDataRate', 'OrigDataStartFrame', 'OrigNumFrames']
        self.lines[2] = ['60', '60', str(nFrames), str(nMarkers), 
                        'mm', '60', '1', str(nFrames)]
        header = ['Frame#', 'Time']
        dims = ['', '']
        
        for n in range(len(names)):
            header.extend([names[n], '', ''])
            dim.extend(['X'+str(n+1), 'Y'+str(n+1), 'Z'+str(n+1)])
            
        self.lines[3] = header
        self.lines[4] = dims
        self.lines[5] =  ['', '', '', '', '', '', '', '']
        self.lines[6] = ['1', '0']
    
    def writeTrajectoriesToFile(self):
        # first we need a list of lists
        lines = []
		nFrames = len(self.trajectories
        # first element of lines is always the frame
        frames  = range(1,nFrames+1)
        lines = [[] for f in frames]
		lines = [lines[f] + str(f) for i in frames]
        start_time=0
        lines = [lines[i] + str(i*) for i in frames]
                        
                        
class DataG:
    def __init__(self):
        data = []
        foo = []
        bar = None
        



f = "C:\\Users\\SyMon\\Documents\\OpenSim\\ARMS Copy\\MoBL-ARMS OpenSim tutorial_33\\ModelFiles\\data.trc"
outF = "C:\\Users\\SyMon\\Documents\\OpenSim\\ARMS Copy\\MoBL-ARMS OpenSim tutorial_33\\ModelFiles\\staticpose.trc"

def vec2ls(v):
#   # converts an opensim vector 3 v to a python collection
    ls = [v.get(0), v.get(1), v.get(2)]     
    return ls

    
def dist(p0, p1):
    # Calculates distance between 2 points given as lists of 3
    x = (p1[0]-p0[0])**2
    y = (p1[1]-p0[1])**2
    z = (p1[2]-p0[2])**2
    d = math.sqrt(x + y + z)
    return d
    
   
def lerp3(p0, p1, nPoints):
    # returns a list of coordinates between p0 and p1
    # find vector between the given end points
    v = [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]
    # find the abs. magnitude of this vector
    # calculate dist. between end points points
    mag = dist(p0,p1)
    # 
    u = []

    # increment for each new point is total distance divided by desired no. of frames
    incr = mag/nPoints ##(nPoints-1)
    # 
    p = []
    for i in range(nPoints+1 ):
        d = i*incr
        tmp = d/mag
        b = [ tmp*v[0], tmp*v[1], tmp*v[2] ]
        p.append([ p0[0]+b[0], p0[1]+b[1], p0[2]+b[2] ])
    
    return p

    
def mTOmm(p):
    conv = [i*1000 for i in p]
    return conv

    
def mmTOm(p):
    conv = [i/1000 for i in p]
    return p
    
   
#%%

#with open(f) as tsvfile:
#    tsvreader = csv.reader(tsvfile, delimiter="\t")
#    for l in tsvreader:
#        lines.append(l)
        

#%%        
#numFrames = int(lines[-1][0]) 
#numMarkers = len(names)


#%%
#currentNumFrames = 151
#len(lines)-6
#data = []
    
    
#%%
#for i in range(currentNumFrames):
#    ln = lines[6+i][:2]
#    ln.extend(data)
#    lines[6+i] = ln
    

#%% 

#with open(outF, 'wb') as ff:
#    writer = csv.writer(ff,delimiter='\t')
#    writer.writerows(lines)
    


# convert to mm

# read in a trc file (to get headers)

# frame vector

# time vector
# sampling frequency

# repeat for Scaling procedure
# lerp for motion

# header line:
# foo.name() + "t t t " + bar.name() 

# cat vectors into a matrix
# writelines

# save as .trc
    

 
