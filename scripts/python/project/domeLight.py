'''
    domeLight.py

    Author: Teal Owyang
    Date:   2015-02-06

    Description: Interface for creating a dome light rig.
                 Rig Features:
                 - After the rig is created, the entire dome rig group can be translated, rotated, 
                   or scaled. 
                 - Each light can move around the half dome individually with the move tool. the
                   lights are constrained to move along the half sphere.
                 - All light attributes can be modified in the extra attributes of the group
                   even after the rig's been created. 
                 - All of the lights' aims are pointed at the light locator object. Move the
                   locator to move the lights' aim.
'''
from maya import cmds
from collections import OrderedDict
import re
import math


def process():
    '''
        Brings up the Dome Light Rig UI.
    '''

    dlWin = "domeLightWin"

    if cmds.window(dlWin, exists=True):
        cmds.deleteUI(dlWin)
    if cmds.windowPref(dlWin, exists=True):
        cmds.windowPref(dlWin, remove=True)

    winWidth = 425
    winHeight = 485

    cmds.window(dlWin, width=winWidth, height=winHeight, sizeable=False, menuBar=True, 
        title="Dome Light Rig")

    cmds.menu(label="Help")
    cmds.menuItem(label="About...", 
        command="from project import domeLight; domeLight.aboutWin()")

    cmds.frameLayout(borderVisible=1, borderStyle="etchedIn", labelVisible=0)
    mainForm = cmds.formLayout("mainForm")

    _buildControls( dlWin )
    _positionControls( dlWin, mainForm )

    cmds.window(dlWin, edit=True, width=winWidth, height=winHeight)

    cmds.showWindow(dlWin)


def _buildControls( dlWin ):
    # Build controls  
    ltTxt = cmds.text("ltTxt", label="Light Type:")

    ltRC = cmds.radioCollection("ltRC")
    spotRB = cmds.radioButton("spotRB", label="Spotlight", select=True,
        onCommand=("from maya import cmds;" + \
                   "cmds.floatSliderGrp('caFSG', edit=True, enable=True);" + \
                   "cmds.floatSliderGrp('paFSG', edit=True, enable=True);" + \
                   "cmds.floatSliderGrp('dropFSG', edit=True, enable=True)"))
    dirRB = cmds.radioButton("dirRB", label="Directional Light",
        onCommand=("from maya import cmds;" + \
                   "cmds.floatSliderGrp('caFSG', edit=True, enable=False);" + \
                   "cmds.floatSliderGrp('paFSG', edit=True, enable=False);" + \
                   "cmds.floatSliderGrp('dropFSG', edit=True, enable=False)"))

    cmds.intSliderGrp('numlISG', min=1, max=1000, fieldMaxValue=10000, value=240, field=True, 
        step=2, fs=2, cc=("from project import domeLight; domeLight._stepIntSlider()"), 
        label="Number of Lights")
    cmds.floatSliderGrp("drFSG", min=.001, max=10000, value=10, field=True, label="Dome Radius")

    cmds.colorSliderGrp("colorCSG", label="Color", rgb=[1, 1, 1])
    cmds.floatSliderGrp("intFSG", min=0, max=10, fieldMinValue=-10000, fieldMaxValue=10000,
        value=1, field=True, label="Intensity")
    cmds.checkBox("specCB", label="Emit Specular")
    cmds.floatSliderGrp("caFSG", min=0,  max=180, value=40, field=True, label="Cone Angle")
    cmds.floatSliderGrp("paFSG", min=-10, max=10, fieldMaxValue=180, fieldMinValue=-180, value=0, 
        field=True, label="Penumbra Angle")
    cmds.floatSliderGrp("dropFSG", min=0, max=255, fieldMaxValue=10000, value=0, field=True, 
        label="Dropoff")
    cmds.text("stTxt", label="Shadow Type:")

    cmds.radioCollection("shadowTypesRC")
    cmds.radioButton("noneRB", label="None", select=True, 
        onCommand=("from maya import cmds;" + \
                   "cmds.colorSliderGrp('scCSG', edit=True, enable=False); " + \
                   "cmds.intSliderGrp('drISG', edit=True, enable=False); " + \
                   "cmds.intSliderGrp('dfISG', edit=True, enable=False); " + \
                   "cmds.floatSliderGrp('dbFSG', edit=True, enable=False); " + \
                   "cmds.floatSliderGrp('lrFSG', edit=True, enable=False); " + \
                   "cmds.intSliderGrp('srISG', edit=True, enable=False)"))
    cmds.radioButton("dmRB", label="Depth Map", 
        onCommand=("from maya import cmds;" + \
                   "cmds.colorSliderGrp('scCSG', edit=True, enable=True); " + \
                   "cmds.intSliderGrp('drISG', edit=True, enable=True); " + \
                   "cmds.intSliderGrp('dfISG', edit=True, enable=True); " + \
                   "cmds.floatSliderGrp('dbFSG', edit=True, enable=True); " + \
                   "cmds.floatSliderGrp('lrFSG', edit=True, enable=False); " + \
                   "cmds.intSliderGrp('srISG', edit=True, enable=False)"))
    cmds.radioButton("rtRB", label="Ray Trace", 
        onCommand=("from maya import cmds;" + \
                   "cmds.colorSliderGrp('scCSG', edit=True, enable=True); " + \
                   "cmds.intSliderGrp('drISG', edit=True, enable=False); " + \
                   "cmds.intSliderGrp('dfISG', edit=True, enable=False); " + \
                   "cmds.floatSliderGrp('dbFSG', edit=True, enable=False); " + \
                   "cmds.floatSliderGrp('lrFSG', edit=True, enable=True); " + \
                   "cmds.intSliderGrp('srISG', edit=True, enable=True)"))
                                                 
    cmds.colorSliderGrp("scCSG", label="Shadow Color", enable=False, rgb=[0, 0, 0])
    cmds.intSliderGrp("drISG", min=16, max=8192, enable=False, value=512, field=True, 
        label="Dmap Resolution")
    cmds.intSliderGrp("dfISG", min=0, max=5, fieldMaxValue=10000, enable=False, value=1, 
        field=True, label="Dmap Filter Size")
    cmds.floatSliderGrp("dbFSG", min=0, max=1, fieldMaxValue=10000, pre=3, enable=False, 
        value=.001, field=True, label="Dmap Bias")
    cmds.floatSliderGrp("lrFSG", min=0, max=1, fieldMaxValue=10000, enable=False, field=True, 
        label="Light Radius")
    cmds.intSliderGrp("srISG", min=1, max=40, fieldMaxValue=10000, enable=False, value=1, 
        field=True, label="Shadow Rays")
    cmds.separator("sep", style="in")
    cmds.button("createBtn", label="Create Rig", 
        command=("from project import domeLight; domeLight._createRig(); \
                  from maya import cmds; cmds.deleteUI('" + dlWin + "')"))
    cmds.button("cancelBtn", label="Cancel", 
        command=("from maya import cmds;cmds.deleteUI('" + dlWin + "')"))


def _stepIntSlider():
    val = math.fmod(float(cmds.intSliderGrp('numlISG', query=True, value=True)), 
        cmds.intSliderGrp('numlISG', query=True, step=True))
    cmds.intSliderGrp('numlISG', edit=True, 
        value=(cmds.intSliderGrp('numlISG', query=True, value=True) - val))
    

def _positionControls( dlWin, mainForm ):
    # Position controls
    leftPos = -20
    rightPos = 20

    cmds.formLayout(mainForm, edit=True, attachForm=[('ltTxt', "left", 80), ('ltTxt', "top", 10)])
    cmds.formLayout(mainForm, edit=True, attachControl=['spotRB', "left", 15, 'ltTxt'], 
        attachForm=['spotRB', "top", 10])
    cmds.formLayout(mainForm, edit=True, attachControl=['dirRB', "left", 10, 'spotRB'], 
        attachForm=['dirRB', "top", 10])

    cmds.formLayout(mainForm, edit=True, attachForm=[('numlISG', "left", leftPos), 
        ('numlISG', "right", rightPos)], attachControl=['numlISG', "top", 10, 'ltTxt'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('drFSG', "left", leftPos), 
        ('drFSG', "right", rightPos)], attachControl=['drFSG', "top", 5, 'numlISG'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('colorCSG', "left", leftPos), 
        ('colorCSG', "right", rightPos)], attachControl=['colorCSG', "top", 10, 'drFSG'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('intFSG', "left", leftPos), 
        ('intFSG', "right", rightPos)], attachControl=['intFSG', "top", 5, 'colorCSG'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('specCB', "left", 103), 
        ('specCB', "right", rightPos)], attachControl=['specCB', "top", 5, 'intFSG'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('caFSG', "left", leftPos), 
        ('caFSG', "right", rightPos)], attachControl=['caFSG', "top", 5, 'specCB'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('paFSG', "left", leftPos), 
        ('paFSG', "right", rightPos)], attachControl=['paFSG', "top", 5, 'caFSG'])
    cmds.formLayout(mainForm, edit=True, attachForm=[('dropFSG', "left", leftPos), 
        ('dropFSG', "right", rightPos)], attachControl=['dropFSG', "top", 5, 'paFSG'])

    cmds.formLayout(mainForm, edit=True, attachForm=['stTxt', "left", 55], 
        attachControl=['stTxt', "top", 10, 'dropFSG'])
    cmds.formLayout(mainForm, edit=True, 
        attachControl=[('noneRB', "left", 15, 'stTxt'), ('noneRB', "top", 10, 'dropFSG')])
    cmds.formLayout(mainForm, edit=True, 
        attachControl=[('dmRB', "left", 10, 'noneRB'), ('dmRB', "top", 10, 'dropFSG')])
    cmds.formLayout(mainForm, edit=True, 
        attachControl=[('rtRB', "left", 10, 'dmRB'), ('rtRB', "top", 10, 'dropFSG')])

    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('scCSG', "left", leftPos), ('scCSG', "right", rightPos)], 
        attachControl=['scCSG', "top", 10, 'stTxt'])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('drISG', "left", leftPos), ('drISG', "right", rightPos)], 
        attachControl=['drISG', "top", 5, 'scCSG'])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('dfISG', "left", leftPos), ('dfISG', "right", rightPos)], 
        attachControl=['dfISG', "top", 5, 'drISG'])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('dbFSG', "left", leftPos), ('dbFSG', "right", rightPos)], 
        attachControl=['dbFSG', "top", 5, 'dfISG'])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('lrFSG', "left", leftPos), ('lrFSG', "right", rightPos)], 
        attachControl=['lrFSG', "top", 5, 'dbFSG'])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('srISG', "left", leftPos), ('srISG', "right", rightPos)], 
        attachControl=['srISG', "top", 5, 'lrFSG'])

    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('sep', "left", 0), ('sep', "right", 0), ('sep', "bottom", 25)])
    cmds.formLayout(mainForm, edit=True, 
        attachForm=[('createBtn', "left", 0), ('createBtn', "bottom", 0)], 
        attachControl=['createBtn', "top", 0, 'sep'], 
        attachPosition=['createBtn', "right", 0, 50])
    cmds.formLayout(mainForm, edit=True, 
        attachControl=[('cancelBtn', "left", 0, 'createBtn'), ('cancelBtn', "top", 0, 'sep')], 
        attachForm=[('cancelBtn', "right", 0), ('cancelBtn', "bottom", 0)])


def _createAttributes( domeRig ):
    # Create and set group attributes
    rgb = cmds.colorSliderGrp( 'colorCSG', query=True, rgbValue=True )
    _createColorAttribute( domeRig, 'color', rgb )

    i = cmds.floatSliderGrp( 'intFSG', query=True, value=True )
    cmds.addAttr( domeRig, longName='intensity', attributeType='float', defaultValue=i, 
        softMinValue=0, softMaxValue=10, minValue=-10000, maxValue=10000 )

    spec = cmds.checkBox( 'specCB', query=True, value=True )
    cmds.addAttr( domeRig, longName='emitSpecular', attributeType='bool', defaultValue=spec )

    # Only create these attributes for spotlights
    if cmds.radioButton('spotRB', query=True, select=True):
        ca = cmds.floatSliderGrp( 'caFSG', query=True, value=True )
        cmds.addAttr( domeRig, longName='coneAngle', attributeType='float', defaultValue=ca, 
            minValue=0, maxValue=180 )
        
        pa = cmds.floatSliderGrp( 'paFSG', query=True, value=True )
        cmds.addAttr( domeRig, longName='penumbraAngle', attributeType='float', defaultValue=pa, 
            softMinValue=-10, softMaxValue=10, minValue=-180, maxValue=180 )

        drop = cmds.floatSliderGrp( 'dropFSG', query=True, value=True )
        cmds.addAttr( domeRig, longName='dropoff', attributeType='float', defaultValue=drop, 
            softMinValue=0, softMaxValue=255, maxValue=10000 )

    cmds.addAttr( domeRig, longName='shadows', attributeType='enum', 
        enumName='None:Depth Map:Ray Trace' )

    rgb = cmds.colorSliderGrp( 'scCSG', query=True, rgbValue=True )
    _createColorAttribute( domeRig, 'shadowColor', rgb )

    cmds.addAttr( domeRig, longName='useDepthMapShadows', attributeType='bool', hidden=True)
    cmds.addAttr( domeRig, longName='useRayTraceShadows', attributeType='bool', hidden=True)

    dr = cmds.intSliderGrp( 'drISG', query=True, value=True )
    cmds.addAttr( domeRig, longName='dmapResolution', attributeType='short', defaultValue=dr, 
        minValue=16, maxValue=8192 )

    df = cmds.intSliderGrp( 'dfISG', query=True, value=True )
    cmds.addAttr( domeRig, longName='dmapFilterSize', attributeType='short', defaultValue=df, 
        softMinValue=0, softMaxValue=5, maxValue=10000 )

    db = cmds.floatSliderGrp( 'dbFSG', query=True, value=True )
    cmds.addAttr( domeRig, longName='dmapBias', attributeType='float', defaultValue=db, 
        softMinValue=.001, softMaxValue=1, maxValue=10000 )

    lr = cmds.floatSliderGrp( 'lrFSG', query=True, value=True )
    cmds.addAttr( domeRig, longName='lightRadius', attributeType='float', defaultValue=lr, 
        softMinValue=0, softMaxValue=1, maxValue=10000 )
    
    sr = cmds.intSliderGrp( 'srISG', query=True, value=True )
    cmds.addAttr( domeRig, longName='shadowRays', attributeType='short', defaultValue=sr, 
        softMinValue=1, softMaxValue=40, maxValue=10000 )
    
    # Setup enum value mapping
    cmds.setDrivenKeyframe( (domeRig + '.useDepthMapShadows'), 
        currentDriver=(domeRig + '.shadows') )
    cmds.setDrivenKeyframe( (domeRig + '.useDepthMapShadows'), 
        currentDriver=(domeRig + '.shadows'), driverValue=1, value=1 )
    cmds.setDrivenKeyframe( (domeRig + '.useDepthMapShadows'), 
        currentDriver=(domeRig + '.shadows'), driverValue=2 )

    cmds.setDrivenKeyframe( (domeRig + '.useRayTraceShadows'), 
        currentDriver=(domeRig + '.shadows') )
    cmds.setDrivenKeyframe( (domeRig + '.useRayTraceShadows'), 
        currentDriver=(domeRig + '.shadows'), driverValue=1 )
    cmds.setDrivenKeyframe( (domeRig + '.useRayTraceShadows'),
        currentDriver=(domeRig + '.shadows'), driverValue=2, value=1 )


def _createColorAttribute( domeRig, name, rgb ):
    cmds.addAttr( domeRig, longName=name, attributeType='float3', usedAsColor=True )
    cmds.addAttr( domeRig, longName=('red' + name), attributeType='float', 
        defaultValue=rgb[0], parent=name )
    cmds.addAttr( domeRig, longName=('green' + name), attributeType='float', 
        defaultValue=rgb[1], parent=name )
    cmds.addAttr( domeRig, longName=('blue' + name), attributeType='float', 
        defaultValue=rgb[2], parent=name )    


def _getLightInfo( num ):
    combos = []

    # Collect all possible combinations of light information for the given number of lights
    best = [0,{}]

    for i in range(1,num+1):
        for j in range(1,num+1):
            if i * j == num:
                diff = i - .25*j
                if len(best[1]) == 0 or math.fabs(diff) <= best[0]:
                    best[0] = math.fabs(diff)
                    best[1] = {'lightsPerArc':i, 'arcs':j}

    return best[1]

def _createRig():
    # Grab light creation values
    isSpot = cmds.radioButton('spotRB', query=True, select=True)
    radius = cmds.floatSliderGrp("drFSG", query=True, value=True)
    num = cmds.intSliderGrp("numlISG", query=True, value=True)    

    # Round down to next even number if odd
    if num > 1:
        num = int(num - math.fmod(num,2))

    l = _getLightInfo( num )

    # Create group
    domeRig = cmds.group(em=True, name='domeRig#')

    # Create and set group attributes
    _createAttributes( domeRig )
    cmds.setAttr( (domeRig + '.displayHandle'), True )
    cmds.setAttr( (domeRig + '.selectHandleY'), radius)

    # Create Lights
    lights = _createLights( domeRig, isSpot, l['lightsPerArc'], l['arcs'], radius )
    
    # Add lights to their own group
    lightgrp = cmds.group(lights, parent=domeRig, name='lights')

    # Make light group locked unkeyable
    attrs = cmds.listAttr(lightgrp, keyable=True)
    for attr in attrs:
        cmds.setAttr( (lightgrp + '.' + attr), keyable=False, lock=True )

    # Create Invisible Half Sphere
    lightConstraint = cmds.polySphere( name=(domeRig + '_lightConstraint'), radius=radius )
    cmds.setAttr((lightConstraint[0] + '.visibility'), False)
    cmds.select((lightConstraint[0] + '.f[0:179]'), (lightConstraint[0] + '.f[360:379]'), replace=True)
    cmds.delete()

    chld = cmds.listRelatives( lightConstraint[0], children=True )
    cmds.setAttr((chld[0] + '.visibility'), False)

    # Add sphere to group
    cmds.parent( lightConstraint[0], domeRig )

    # Create Locator
    lightLocator = cmds.spaceLocator(name=(domeRig + '_lightLocator'))

    # Add locator to group
    cmds.parent( lightLocator, domeRig )

    # Set up each light
    _setupLights( domeRig, isSpot, lights, num, lightConstraint, lightLocator )


def _createLights( domeRig, isSpot, numLights, numArcs, radius ):
    lights = []
    
    # Calculate light angle in arc
    if numLights < 5:
        a = 90.0 / (numLights + 1)
        start = 1
        end = numLights + 1
    else:
        a = 90.0 / (numLights - 1)
        start = 0
        end = numLights

    # Create and position lights in a single arc
    for t in range(start,end):
        if numLights < 5: n = t
        else: n = t + 1
        
        # Create Light
        domeLightName = (domeRig + '_light' + str(n))

        if isSpot: domeLight = cmds.spotLight( name=domeLightName )
        else:      domeLight = cmds.directionalLight( name=domeLightName )

        # Calculate position
        tx = radius * math.cos(math.radians(a*t))
        ty = radius * math.sin(math.radians(a*t))

        # Set position
        cmds.setAttr((domeLightName + '.translateX'), tx)
        cmds.setAttr((domeLightName + '.translateY'), ty)

        lights.append(domeLight)

    a = 360.0 / numArcs

    # Add lights to group
    cmds.group( lights, useAsGroup=domeRig )

    lightArcs = OrderedDict()

    for i in range(1,numArcs):
        # Duplicate Light Arc
        arcLights = cmds.duplicate( domeRig, renameChildren=True )

        # Set rig pivot to origin
        _centerPivot( arcLights[0] )

        # Rotate the group
        cmds.setAttr((arcLights[0] + '.rotateY'), a*i)

        # Remove the group from the duplicated arc
        grp = arcLights.pop(0)

        # Add lights to light arc dictionary
        lightArcs.update({grp:arcLights})

    for grp in lightArcs:
        for l in lightArcs[grp]:
            # Parent all the lights into the original group
            cmds.parent( l, domeRig )
            chld = cmds.listRelatives(l, children=True)
            lights.append( chld[0] )

        # Delete duplicated group
        cmds.delete(grp)

    # Set rig pivot to origin
    _centerPivot( domeRig )

    return lights


def _centerPivot( obj ):
    pivotControls = ('PivotX', 'PivotY', 'PivotZ')
    
    for p in pivotControls:
        cmds.setAttr( (obj + '.rotate' + p), 0 )
        cmds.setAttr( (obj + '.scale' + p), 0 )


def _setupLights( domeRig, isSpot, lights, numLights, lightConstraint, lightLocator ):
    lightAttr = ( 'color', 'emitSpecular', 'coneAngle', 'penumbraAngle',
                  'dropoff', 'shadowColor', 'dmapResolution', 'dmapFilterSize',
                  'dmapBias', 'lightRadius', 'shadowRays', 'useDepthMapShadows',
                  'useRayTraceShadows' )

    # Create intensity MD to divide each light's intensity to sum the user's intensity
    intMD = cmds.shadingNode( 'multiplyDivide', asUtility=True, name=(domeRig + '_mdIntensity') )
    cmds.setAttr( (intMD + ".operation"), 2 )
    cmds.setAttr( (intMD + ".input2X"), numLights )
    cmds.connectAttr( (domeRig + '.intensity'), (intMD + '.input1X') )

    # Set up for individual lights in the rig
    for l in lights:
        # Connect intensity MD to each light's intensity
        cmds.connectAttr( (intMD + '.outputX'), (l + '.intensity') )

        # Constrain all lights to sphere
        lp = cmds.listRelatives(l, parent=True)
        cmds.geometryConstraint( lightConstraint, lp )

        # Set all lights to point at locator
        cmds.aimConstraint( lightLocator, lp[0], offset=[0,-90,0] )

        # Connect group's extra attributes to each light's attributes
        for attr in lightAttr:
            if isSpot or ( not isSpot and attr not in ['coneAngle', 'penumbraAngle', 'dropoff']):
                cmds.connectAttr( (domeRig + '.' + attr), (l + '.' + attr) )

    # Connect sphere and light rig keyable attributes
    attrs = cmds.listAttr(lightConstraint[0], keyable=True)
    for attr in attrs:
        cmds.setAttr( (lightConstraint[0] + '.' + attr), keyable=False, lock=True )


def aboutWin():
    aboutWindow = "AboutWin"

    if cmds.window(aboutWindow, exists=True):
        cmds.deleteUI(aboutWindow)

    cmds.window(aboutWindow, resizeToFitChildren=True, sizeable=False, title="About Dome Light Rig")

    cmds.frameLayout(borderVisible=True, borderStyle="etchedIn", labelVisible=False)
    cmds.columnLayout()
    cmds.text(label="Created by: Teal Owyang", align="left")
    cmds.text(label="")
    cmds.text(label="This is a Dome Light Rig utility that generates a lighting", align="left")
    cmds.text(label="setup to simulate dome lighting.", align="left")
    cmds.text(label="")
    cmds.text(label="Credit to Mike Harris for initial UI code.")
    cmds.text(label="")
    cmds.text(label="If you have any comments or suggestions you can contact me at:", align="left")
    cmds.text(label="tmowyang@gmail.com", align="left")

    cmds.showWindow(aboutWindow)