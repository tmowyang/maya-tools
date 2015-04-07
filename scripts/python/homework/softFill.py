'''
    softFill.py

    Author: Teal Owyang
    Date:   2015-01-20

    Description: A "soft fill" light rig that will allow the user to generate a lighting setup that
    			 will produce soft fill lighting in the scene.
'''
from maya import cmds
import re

def softFill():
    controls = ( 'tx', 'ty', 'tz',
                 'rx', 'ry', 'rz',
                 'sx', 'sy', 'sz', 'v' )
    
    lightAttr = ( 'color', 'dmapBias', 'dmapFilterSize', 
                  'dmapResolution', 'emitSpecular', 'shadowColor',
                  'shadowRays', 'useDepthMapShadows', 'useRayTraceShadows')
    
    lights = []
    
    # Create group
    softFill = cmds.group(em=True, name='softFill#')
    
    # Create and set group attributes
    cmds.addAttr( softFill, longName='color', attributeType='float3', usedAsColor=True )
    cmds.addAttr( softFill, longName='red', attributeType='float', defaultValue=1, parent='color' )
    cmds.addAttr( softFill, longName='green', attributeType='float', defaultValue=1, parent='color' )
    cmds.addAttr( softFill, longName='blue', attributeType='float', defaultValue=1, parent='color' )

    cmds.addAttr( softFill, longName='intensity', attributeType='float', defaultValue=1, softMinValue=0, softMaxValue=10 )
    cmds.addAttr( softFill, longName='lightAngle', attributeType='float', defaultValue=5, minValue=0, maxValue=90 )
    cmds.addAttr( softFill, longName='emitSpecular', attributeType='bool' )

    cmds.addAttr( softFill, longName='shadowColor', attributeType='float3', usedAsColor=True )
    cmds.addAttr( softFill, longName='redShadow', attributeType='float', parent='shadowColor' )
    cmds.addAttr( softFill, longName='greenShadow', attributeType='float', parent='shadowColor' )
    cmds.addAttr( softFill, longName='blueShadow', attributeType='float', parent='shadowColor' )

    cmds.addAttr( softFill, longName='shadows', attributeType='enum', enumName='None:Depth Map:Ray Trace' )
    cmds.addAttr( softFill, longName='dmapResolution', attributeType='short', defaultValue=512, minValue=16, maxValue=8192 )
    cmds.addAttr( softFill, longName='dmapFilterSize', attributeType='short', defaultValue=.001, softMinValue=0, softMaxValue=5 )
    cmds.addAttr( softFill, longName='dmapBias', attributeType='float', defaultValue=.001, softMinValue=.001, softMaxValue=1 )
    cmds.addAttr( softFill, longName='shadowRays', attributeType='short', defaultValue=1, softMinValue=1, softMaxValue=40 )

    cmds.addAttr( softFill, longName='useDepthMapShadows', attributeType='bool', hidden=True)
    cmds.addAttr( softFill, longName='useRayTraceShadows', attributeType='bool', hidden=True)
    
    cmds.setAttr( (softFill + '.displayHandle'), 1 )
    
    # Setup enum value mapping
    cmds.setDrivenKeyframe( (softFill + '.useDepthMapShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline' )
    cmds.setDrivenKeyframe( (softFill + '.useDepthMapShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline',
                             driverValue=1, value=1 )
    cmds.setDrivenKeyframe( (softFill + '.useDepthMapShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline',
                             driverValue=2 )

    cmds.setDrivenKeyframe( (softFill + '.useRayTraceShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline' )
    cmds.setDrivenKeyframe( (softFill + '.useRayTraceShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline',
                             driverValue=1 )
    cmds.setDrivenKeyframe( (softFill + '.useRayTraceShadows'), currentDriver=(softFill + '.shadows'), 
                             inTangentType='spline', outTangentType='spline',
                             driverValue=2, value=1 )

    # Create and connect utility nodes
    # MD Intensity
    softFillIntensity = cmds.shadingNode( 'multiplyDivide', asUtility=True, name=(softFill + '_mdIntensity') )
    cmds.setAttr( (softFillIntensity + ".operation"), 2 )
    cmds.setAttr( (softFillIntensity + ".input1X"), 1 )
    cmds.setAttr( (softFillIntensity + ".input2X"), 5 )
    cmds.connectAttr( (softFill + '.intensity'), (softFillIntensity + '.input1X') )
    
    # MD Light Angle
    softFillLightAngle = cmds.shadingNode( 'multiplyDivide', asUtility=True, name=(softFill + '_mdLightAngle') )
    cmds.setAttr ( (softFillLightAngle + '.input1X'), 5 )
    cmds.setAttr ( (softFillLightAngle + '.input1Y'), 5 )
    cmds.setAttr ( (softFillLightAngle + '.input2Y'), -1 )
    cmds.connectAttr( (softFill + '.lightAngle'), (softFillLightAngle + '.input1X') )
    cmds.connectAttr( (softFill + '.lightAngle'), (softFillLightAngle + '.input1Y') )
    
    # Save directional light names
    softFillName = softFill + '_light'
    
    # Create directional lights
    for i in range(1,6):
        light = cmds.directionalLight( name=(softFillName + str(i)) )
        lights.append(light)
    
    # Add directional lights to group
    cmds.group( lights, useAsGroup=softFill )
    
    # Connect light angle utility node to lights' rotations
    cmds.connectAttr( (softFillLightAngle + '.outputX'), (softFillName + '2.rotateX') )
    cmds.connectAttr( (softFillLightAngle + '.outputY'), (softFillName + '3.rotateX') )
    cmds.connectAttr( (softFillLightAngle + '.outputY'), (softFillName + '4.rotateY') )
    cmds.connectAttr( (softFillLightAngle + '.outputX'), (softFillName + '5.rotateY') )
    
    # Connect utility node output to light intensity
    for i in range(0,5):
        cmds.connectAttr( (softFillIntensity + '.outputX'), (lights[i] + '.intensity') )
        for control in controls:
            if control != 'rx' and control != 'ry':
                cmds.setAttr( (softFillName + str(i+1) + '.' + control), lock=True )
        
        # Connect light attributes
        for attr in lightAttr:
            cmds.connectAttr( (softFill + '.' + attr), (lights[i] + '.' + attr) )