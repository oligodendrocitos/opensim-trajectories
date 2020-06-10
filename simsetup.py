import os
import sys

"""
A Setup for custom motion generation execution
"""


# Add path to the directory containing our scripts in the ARMS module
sys.path.append('C:\Users\SyMon\Documents\OpenSim\ARMS Copy\Scripts')

import trcalt as tm


m1=getCurrentModel()
print('current opened model assigned to m1.')
SP = tm.ModelPose(m1)
print('Start pose SP created from m1.')
staticData = tm.Traj(SP, SP, 150, 60,'staticpose-new-script.trc')
staticData.createTrajectories()
staticData.prepareFileTemplate()
staticData.writeTrajectoriesToFile()
print('Static data for model scaling generated.')

print('Adjust model position in editor and set it to default.')
print('Get the osim model of the final pose: m2 = getCurrentModel()')
print('Create final pose: Your_pose_name = tm.ModelPose(m2)')
print('Create and write trajectories to file:')
print('tj = tm.Traj(StartPose, Finalpose, NumFrames, Framerate,''filename.trc'')')
print('For example: tj = tm.Traj(SP, Your_pose_name, 150, 60,''filename.trc'')')
print('tj.createTrajectories()')
print('tj.prepareFileTemplate()')
print('tj.writeTrajectoriesToFile()')

#tj.prepareFileTemplate()
#tj.writeTrajectoriesToFile()

#p0=[1,1,1]
#p1=[-2,0,0]