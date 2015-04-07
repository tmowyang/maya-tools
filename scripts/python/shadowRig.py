'''
    shadowRig.py

    Author: Teal Owyang
    Date:   2014-12-03

    Description: Create a "shadow only" light rig that will allow the user to
                 generate a lighting setup that will only produce a shadow
                 without affecting the amount of light being added into the
                 scene.
'''
from maya import cmds
import re

def shadowRig():
    controls = [ "translateX", "translateY", "translateZ", \
                 "rotateX", "rotateY", "rotateZ", \
                 "scaleX", "scaleY", "scaleZ", "v" ]

    negLightAttr = [ "decayRate", "emitSpecular", "useDepthMapShadows", \
                     "dmapResolution", "dmapFilterSize", "color", \
                     "shadowColor", "useRayTraceShadows", "lightRadius", \
                     "shadowRays"]

    # Create group
    shadowSpot = cmds.group(em=True, name='shadowSpot#')

    # Grab index
    index = None
    if re.search('[0-9]+$', shadowSpot):
        index = re.search('[0-9]+$', shadowSpot).group()[0]

    # Save spotlight names
    shadowLightName = ('shadowLight' + index)
    shadowNegLightName = ('shadowNegLight' + index)

    # Create spotlights
    shadowLight = cmds.spotLight( name=shadowLightName )
    shadowNegLight = cmds.spotLight( name=shadowNegLightName )

    # Add spotlights to group
    cmds.group( shadowLightName, shadowNegLightName, useAsGroup=shadowSpot )

    # Create constraints
    cmds.pointConstraint( shadowLightName, shadowNegLightName )
    cmds.orientConstraint( shadowLightName, shadowNegLightName )

    # Connect shape attributes
    cmds.connectAttr( (shadowLight + '.coneAngle'), (shadowNegLight + '.coneAngle'), force=True )
    cmds.connectAttr( (shadowLight + '.dropoff'), (shadowNegLight + '.dropoff'), force=True )
    cmds.connectAttr( (shadowLight + '.penumbraAngle'), (shadowNegLight + '.penumbraAngle'), force=True )

    # Create utility node
    shadowSpotIntensity = cmds.shadingNode( 'multiplyDivide', asUtility=True, name=(shadowSpot + 'mdIntensity') )
    cmds.connectAttr( (shadowLight + '.intensity'), (shadowSpotIntensity + '.input1X') )
    cmds.setAttr ( (shadowSpotIntensity + '.input2X'), -1 )
    cmds.connectAttr ( (shadowSpotIntensity + '.outputX'), (shadowNegLight + '.intensity') )

    # Zero out shadow light attributes
    cmds.setAttr ( (shadowNegLightName + ".useDepthMapShadows"), 0 )
    cmds.setAttr ( (shadowNegLightName + ".useRayTraceShadows"), 0 )

    # Lock attributes
    for attr in negLightAttr:
        cmds.setAttr ( (shadowNegLightName + "." + attr), lock=True, keyable=False )

    # Lock and hide spotlight controls
    for control in controls:
        cmds.setAttr ( (shadowSpot + "." + control), lock=True, keyable=False )
        cmds.setAttr ( (shadowNegLightName + "." + control), lock=True, keyable=False )
        
    # Activate displayHandle
    cmds.setAttr ( (shadowLightName + ".displayHandle"), 1 )