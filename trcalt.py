from __future__ import with_statement
import os.path
import csv
import math
#import opensim 

class Traj:

    def __init__(self, StartPose, FinalPose, nFrames, frameRate, filename):
        self.mod1 = StartPose
        self.mod2 = FinalPose
        self.filename = filename
        # Change this to your ARMS model directory
        # UNIX: /home/usr/Documents/Opensim
        self.filepath = 'C:\\Users\\SyMon\\Documents\\OpenSim\\ARMS Copy\\ModelFiles\\' # Windows
        self.frameRate = frameRate
        self.nFrames = nFrames
        self.lines = [] 
        self.coordsPrime = None
        self.sPrime = None
        self.namesPrime = [] # to sanity check whether both sets would have the same markers...
        self.trajectories = {} 
          
    def prepareFileTemplate(self):
        nMarkers = len(self.trajectories.keys())
        nFrames = self.nFrames
        fName = self.filename
        names = self.trajectories.keys()
        self.lines.append( ['PathFileType', '4', '(X/Y/Z)', fName, '', '', '', ''] )
        self.lines.append(['DataRate', 'CameraRate', 'NumFrames', 'NumMarkers','Units', 'OrigDataRate', 'OrigDataStartFrame', 'OrigNumFrames'])
        self.lines.append(['60', '60', str(nFrames), str(nMarkers),'mm', '60', '1', str(nFrames)])
        header = ['Frame#', 'Time']
        dims = ['', '']
        
        for n in range(len(names)):
            header.extend([names[n], '', ''])
            dims.extend(['X'+str(n+1), 'Y'+str(n+1), 'Z'+str(n+1)])
            
        self.lines.append(header)
        self.lines.append(dims)
        self.lines.append(['', '', '', '', '', '', '', ''])
        
    def createTrajectories(self):
        # how many markers are there?
        m = len(self.mod1.coords)
        c = [i for i in range(m) if self.mod1.names[i]==self.mod2.names[i] ]
        if len(c)<len(self.mod1.names):
            print('Some markers not present in both models and will be excluded')
        if self.mod1.coords==self.mod2.coords:
            print('Start pose identical to end pose. Generating static data.')
            for i in c:
                p0 = mTOmm(self.mod1.coords[i])
                t = [p0 for f in range(self.nFrames)]
                self.trajectories[self.mod1.names[i]] = t
        else:
            for i in c:
                # convert to mm
                p0 = mTOmm(self.mod1.coords[i])
                p1 = mTOmm(self.mod2.coords[i])
                # generate trajectory
                t = lerp3(p0, p1, self.nFrames)
                self.trajectories[self.mod1.names[i]] = t
    
    def writeTrajectoriesToFile(self):
        # first we need a list of lists
        lines = []
        nFrames = self.nFrames # len(self.trajectories.keys())
        # first element of lines is always the frame
        frames  = range(nFrames)
        lines = [[] for f in frames]
        lines = [lines[f] + [str(f+1)] for f in frames]
        # second is always the timestamp, in seconds
        start_time=0
        incr = 1.0/float(self.frameRate)
        lines = [lines[i] + [str(i*incr)] for i in frames]
        # convert each trajectory to a string and append to each line 
        for n in self.trajectories.keys():
            t = self.trajectories[n]
            t_string = pTOstr(t)
            lines = [lines[i] + t_string[i] for i in range(len(t_string))]
        self.lines.extend(lines)
        
        fn = self.filepath + self.filename
        
        with open(fn,'wb') as ff:
            writer = csv.writer(ff,delimiter='\t')
            writer.writerows(self.lines)
            
        

class ModelPose:

    def __init__(self, osimModel):
        self.coords = [] # list of marker coordinates
        self.names = []  # list of marker names
        self.lines = []  # lines in final file
        self.data = []   # list of final coordinates
        self.mkr = osimModel.getMarkerSet()
        # 
        #self.coordsPrime = None
        #self.sPrime = None
        #self.namesPrime = [] # to sanity check whether both sets would have the same markers...

        #self.trajectories = {}
        # Get marker set from model
        
        # init system so we get a state (needed to get coords)
        self.sZero = osimModel.initSystem()
        for i in range(self.mkr.getSize()):
            foo = self.mkr.get(i)
            loc = foo.getLocationInGround(self.sZero)
            self.coords.append(vec2ls(loc))  
            # get starting coordinates as a float/ normal vector
            self.names.append(str(foo.getName()))
              
    def setTarget(self, osimModel): # this isn't being used at the moment
        mkr = osimModel.getMarkerSet()
        self.coordsPrime = []
        self.sPrime = osimModel.initSystem()
        for i in range(mkr.getSize()):
            foo = mkr.get(i)
            loc = foo.getLocationInGround(self.sPrime)
            self.coordsPrime.append(vec2ls(loc))  
            # get starting coordinates as a float/ normal vector
            self.namesPrime.append(str(foo.getName()))
                                         

def vec2ls(v):
#   # converts an opensim vector 3 v to a python collection (list)
    ls = [v.get(0), v.get(1), v.get(2)]     
    return ls

    
def dist(p0, p1):
    # Calculates distance between 2 points given as lists of 3 (euclid)
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
    # test whether points are the same:
    if p0==p1:
        p = [p0 for i in range(nPoints)]
    else:
        for i in range(nPoints):
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
    
def pTOstr(coords_list):
    coords_str = [ [str(p[0]), str(p[1]), str(p[2])] for p in coords_list ]
    return coords_str
   
#%%

#with open(f) as tsvfile:
#    tsvreader = csv.reader(tsvfile, delimiter="\t")
#    for l in tsvreader:
#        lines.append(l)
        

#with open(outF, 'wb') as ff:
#    writer = csv.writer(ff,delimiter='\t')
#    writer.writerows(lines)
    

    

 
