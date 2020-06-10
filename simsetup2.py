import os
import sys

# Default jython console doesn't allow waiting for user input
# until an alternative is found, two scripts need to be run consecutively...


m2=getCurrentModel()
FP = tm.ModelPose(m2)
tj = tm.Traj(SP, FP, 150, 60,'new-motion-test.trc')
tj.createTrajectories()
tj.prepareFileTemplate()
tj.writeTrajectoriesToFile()


#tj.prepareFileTemplate()
#tj.writeTrajectoriesToFile()

#p0=[1,1,1]
#p1=[-2,0,0]