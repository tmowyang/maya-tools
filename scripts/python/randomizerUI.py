'''
    randomizerUI.py

    Author: Teal Owyang
    Date:   2015-01-12

    Description: Takes any number of selected objects and scatter them
                 throughout the Maya scene randomizing their position,
                 rotation, and scale.
'''
from maya import cmds
import re
import random
import string

def randomizerUI():

    controls = ( 'tx', 'ty', 'tz',
                 'rx', 'ry', 'rz',
                 'sx', 'sy', 'sz' )

    window = 'randomizerUI'
    if cmds.window( window, exists=True ):
        cmds.deleteUI( window )
    if cmds.windowPref( window, exists=True ):
        cmds.windowPref( window, remove=True )

    width = 300
    height = 290

    cmds.window( window, widthHeight=(width, height), sizeable=False, menuBar=True, title='Scatterand' )

    cmds.frameLayout( borderVisible=True, borderStyle='etchedIn', labelVisible=False )
    mainForm = cmds.formLayout()

    cmds.radioCollection( 'spaceRC' )
    cmds.radioButton( 'localSpaceRB', label='Local Space', select=True )
    cmds.radioButton( 'worldSpaceRB', label='World Space' )

    minFloat = cmds.text( label='Min' )
    maxFloat = cmds.text( label='Max' )

    tTxt = cmds.text( label='Translate:' )
    rTxt = cmds.text( label='Rotate:' )
    sTxt = cmds.text( label='Scale:' )

    for control in controls:
        # Create float fields
        cmds.floatField( (control + 'MinFloat'), width=75, precision=3, enable=0 )
        cmds.floatField( (control + 'MaxFloat'), width=75, precision=3, enable=0 )

        # Set rotate range
        if re.search('^r', control):
            cmds.floatField( (control + 'MinFloat'), edit=True, minValue=0, maxValue=360 )
            cmds.floatField( (control + 'MaxFloat'), edit=True, minValue=0, maxValue=360, value=360 )

        # Set scale range
        if re.search('^s', control):
            cmds.floatField( (control + 'MinFloat'), edit=True, minValue=.001, value=1 )
            cmds.floatField( (control + 'MaxFloat'), edit=True, minValue=.001, value=1 )

        label = string.capitalize(control[-1:])

        cmds.checkBox( (control + 'CB'), label=label, changeCommand=('toggleCheckBox("' + control + '")') )

    sep = cmds.separator( style='in' )

    okBtn = cmds.button( label='OK', width=150, command='randomizer()' )
    cancelBtn = cmds.button( label='Cancel', width=150, command=('cmds.deleteUI( "' + window + '")') )

    # Local and World Space
    cmds.formLayout( mainForm, edit=True, attachForm=[('localSpaceRB', "left", 60), ('localSpaceRB', "top", 10)] )
    cmds.formLayout( mainForm, edit=True, attachControl=[('worldSpaceRB', "left", 25, 'localSpaceRB')], attachForm=[('worldSpaceRB', "top", 10)] )

    # Min and Max labels
    cmds.formLayout( mainForm, edit=True, attachForm=[(minFloat, "left", 165)], attachControl=[(minFloat, "top", 10, 'worldSpaceRB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[(maxFloat, "left", 235)], attachControl=[(maxFloat, "top", 10, 'worldSpaceRB')] )
    
    # Translate    
    cmds.formLayout( mainForm, edit=True, attachForm=[(tTxt, "left", 25)], attachControl=[(tTxt, "top", 1, minFloat)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('txCB', "left", 100)], attachControl=[('txCB', "top", 1, minFloat)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('txMinFloat', "left", 135)], attachControl=[('txMinFloat', "top", 1, minFloat)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('txMaxFloat', "left", 210)], attachControl=[('txMaxFloat', "top", 1, minFloat)] )

    cmds.formLayout( mainForm, edit=True, attachForm=[('tyCB', "left", 100)], attachControl=[('tyCB', "top", 7, tTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('tyMinFloat', "left", 135)], attachControl=[('tyMinFloat', "top", 7, tTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('tyMaxFloat', "left", 210)], attachControl=[('tyMaxFloat', "top", 7, tTxt)] )

    cmds.formLayout( mainForm, edit=True, attachForm=[('tzCB', "left", 100)], attachControl=[('tzCB', "top", 3, 'tyCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('tzMinFloat', "left", 135)], attachControl=[('tzMinFloat', "top", 3, 'tyCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('tzMaxFloat', "left", 210)], attachControl=[('tzMaxFloat', "top", 3, 'tyCB')] )

    # Rotate
    cmds.formLayout( mainForm, edit=True, attachForm=[(rTxt, "left", 25)], attachControl=[(rTxt, "top", 10, 'tzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('rxCB', "left", 100)], attachControl=[('rxCB', "top", 10, 'tzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('rxMinFloat', "left", 135)], attachControl=[('rxMinFloat', "top", 10, 'tzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('rxMaxFloat', "left", 210)], attachControl=[('rxMaxFloat', "top", 10, 'tzCB')] )
        
    cmds.formLayout( mainForm, edit=True, attachForm=[('ryCB', "left", 100)], attachControl=[('ryCB', "top", 7, rTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('ryMinFloat', "left", 135)], attachControl=[('ryMinFloat', "top", 7, rTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('ryMaxFloat', "left", 210)], attachControl=[('ryMaxFloat', "top", 7, rTxt)] )

    cmds.formLayout( mainForm, edit=True, attachForm=[('rzCB', "left", 100)], attachControl=[('rzCB', "top", 3, 'ryCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('rzMinFloat', "left", 135)], attachControl=[('rzMinFloat', "top", 3, 'ryCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('rzMaxFloat', "left", 210)], attachControl=[('rzMaxFloat', "top", 3, 'ryCB')] )
    
    # Scale
    cmds.formLayout( mainForm, edit=True, attachForm=[(sTxt, "left", 25)], attachControl=[(sTxt, "top", 10, 'rzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('sxCB', "left", 100)], attachControl=[('sxCB', "top", 10, 'rzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('sxMinFloat', "left", 135)], attachControl=[('sxMinFloat', "top", 10, 'rzCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('sxMaxFloat', "left", 210)], attachControl=[('sxMaxFloat', "top", 10, 'rzCB')] )
        
    cmds.formLayout( mainForm, edit=True, attachForm=[('syCB', "left", 100)], attachControl=[('syCB', "top", 7, sTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('syMinFloat', "left", 135)], attachControl=[('syMinFloat', "top", 7, sTxt)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('syMaxFloat', "left", 210)], attachControl=[('syMaxFloat', "top", 7, sTxt)] )

    cmds.formLayout( mainForm, edit=True, attachForm=[('szCB', "left", 100)], attachControl=[('szCB', "top", 3, 'syCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('szMinFloat', "left", 135)], attachControl=[('szMinFloat', "top", 3, 'syCB')] )
    cmds.formLayout( mainForm, edit=True, attachForm=[('szMaxFloat', "left", 210)], attachControl=[('szMaxFloat', "top", 3, 'syCB')] )
    
    # Buttons
    cmds.formLayout( mainForm, edit=True, attachForm=[(sep, "left", 0), (sep, "right", 0), (sep, "bottom", 25)] )
    cmds.formLayout( mainForm, edit=True, attachForm=[(okBtn, "left", 0), (okBtn, "bottom", 0)], attachControl=[(okBtn, "top", 0, sep)], attachPosition=[(okBtn, "right", 0, 50)] )
    cmds.formLayout( mainForm, edit=True, attachControl=[(cancelBtn, "left", 0, okBtn), (cancelBtn, "top", 0, sep)], attachForm=[(cancelBtn, "right", 0), (cancelBtn, "bottom", 0)] )

    cmds.showWindow( window )

def toggleCheckBox(control):
    enable = cmds.checkBox( (control + 'CB'), query=True, value=True )

    cmds.floatField( (control + 'MinFloat'), edit=True, enable=enable )
    cmds.floatField( (control + 'MaxFloat'), edit=True, enable=enable )

def randomizer():
    controls = { 'tx':[0.0,0.0], 'ty':[0.0,0.0], 'tz':[0.0,0.0],
                 'rx':[0.0,0.0], 'ry':[0.0,0.0], 'rz':[0.0,0.0],
                 'sx':[0.0,0.0], 'sy':[0.0,0.0], 'sz':[0.0,0.0] }

    for control in controls:
        controls[control][0] = cmds.floatField( (control + 'MinFloat'), query=True, value=True )
        controls[control][1] = cmds.floatField( (control + 'MaxFloat'), query=True, value=True )

    selectedRB = cmds.radioCollection( 'spaceRC', query=True, select=True )
    objects = cmds.ls( selection=True )

    for object in objects:
        for control in controls:
            if cmds.checkBox( (control + 'CB'), query=True, value=True ):
                if selectedRB == 'worldSpaceRB':
                    cmds.setAttr( (object + '.' + control), random.uniform(controls[control][0], controls[control][1]))
                else:
                    val = cmds.getAttr( object + '.' + control )
                    cmds.setAttr( (object + '.' + control), random.uniform((controls[control][0] + val), (controls[control][1] + val)))