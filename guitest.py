import os
import sys
#import os.path
#import traceback
#import javax.swing
#import java.io as io   
#from javax.swing import JFrame

"""

Gui window to wait for an event


Adapted from 
https://wiki.python.org/jython/SwingExamples#JButton_and_Button_events
"""


import javax.swing as sw
from javax.swing import *
from java.awt import BorderLayout

# This assumes scripts path has been amended to the
# directory containing these scripts (Edit>Preferences in the GUI)
# sys.path.append(os.getcwd())


class Example:
  def setText(self,event):
      self.label.text = 'Button clicked.'
      self.clickedbool = True
      self.frame.dispatchEvent(new WindowEvent(frame, WindowEvent.WINDOW_CLOSING));
  

  def __init__(self):
    frame = sw.JFrame("Jython Example JButton")
    frame.setSize(150, 100)
    frame.setLayout(BorderLayout())
    self.label = sw.JLabel('Click Proceed when final pose has been set')
    frame.add(self.label, BorderLayout.NORTH)
    button = sw.JButton('Proceed',actionPerformed=self.setText)
    frame.add(button, BorderLayout.SOUTH)
    self.clickedbool = False
    #frame.setDefaultCloseOperation(sw.WindowConstants.EXIT_ON_CLOSE)
    frame.setVisible(True)

if __name__ == '__main__':
        w=Example()
        
        #if w.clickedbool:
        #    var= 5*6
        #    str(var)
        