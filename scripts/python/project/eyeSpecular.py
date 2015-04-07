'''
    eyeSpecular.py

    Author: Teal Owyang
    Date:   2015-02-24

    Description: A light rig with a single light and a locator. The locator is where the specular 
                 highlight is on the eye. When the user moves the locator along the eye, the 
                 specular highlight moves with it by the light moving to the necessary position.
'''

from maya import cmds

def process():
    eye = cmds.polySphere()
    light = cmds.spotLight()
    locator = cmds.spaceLocator()
    
    cmds.geometryConstraint( eye, locator )