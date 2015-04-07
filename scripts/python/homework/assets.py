'''
    assets.py

    Author: Teal Owyang
    Date:   2015-01-13

    Description: Sets up an asset hierarchy.
                 Enter an asset name and build the proper upper level transform nodes for animation.
'''
from maya import cmds

def assets():
    result = cmds.promptDialog(
            title='Asset Creation',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)
        createAssets(text)

def createAssets(name):
    controls = ( 'tx', 'ty', 'tz',
                 'rx', 'ry', 'rz',
                 'sx', 'sy', 'sz' )

    # Don't create asset hierarchy if an object with the name exists
    objects = cmds.ls()
    if objects.count(name) > 0:
        cmds.error( 'Element "' + name + '" already exists!' )

    # Create groups
    model = cmds.group( empty=True, name=(name + '_model') )
    rig = cmds.group( empty=True, name=(name + '_rig') )
    aux = cmds.group( model, rig, name=(name + '_aux') )
    shot = cmds.group( aux, name=(name + '_shot') )
    master = cmds.group( shot, name=(name + '_master') )
    top = cmds.group( master, name=name )
   
    # Lock and hide spotlight controls
    for control in controls:
        cmds.setAttr ( (top + "." + control), lock=True, keyable=False )
        cmds.setAttr ( (model + "." + control), lock=True )
        cmds.setAttr ( (rig + "." + control), lock=True )