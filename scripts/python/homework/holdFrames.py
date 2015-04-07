'''
    holdFrames.py

    Author: Teal Owyang
    Date:   2015-01-27

    Description: Takes in a blank "hold" frame, and copy the image to fill in the frames of a given
                 frame range and padding to a destination output directory

    FUTURE TO DO:
    [] Add : functionality to frame range
'''
from maya import cmds
import shutil
import os
import re

def process():
    '''
        Brings up the Hold Frames UI.
        
        Hold Frames:        Hold frame image.
        Base Name:          Start of file name to be created. {Base Name}.{Frame Number}.{File Format}
        Frame Range:        Range of hold frames to be created.
        Frame Padding:      Frame range padding to be used on file creation. Padding must be same
                            length or shorter than the largest frame in frame range.
        Output Directory:   Directory to copy hold frames to.
    '''
    _buildUI( 'holdFramesUI', (650, 175) )

def _buildUI( window, widthHeight ):
    imageFile = 'imageFile'
    outputDir = 'outputDir'
    baseName = 'baseName'
    frameRange = 'frameRange'
    framePadding = 'framePadding'
    
    _cleanupWindow( window )
    mainForm = _setupWindow( window, widthHeight )
    _addControls( window, imageFile, outputDir, baseName, frameRange, framePadding )
    _positionControls( mainForm, imageFile, outputDir, baseName, frameRange, framePadding )
    _resizeAndShowWindow( window, widthHeight )

def _cleanupWindow( window ):
    if cmds.window( window, exists=True ):
        cmds.deleteUI( window )
    if cmds.windowPref( window, exists=True ):
        cmds.windowPref( window, remove=True )

def _setupWindow( window, widthHeight ):
    cmds.window( window, 
        widthHeight=widthHeight, 
        sizeable=False, 
        menuBar=True, 
        title='Hold Frames' )
    
    return cmds.formLayout()

def _addControls( window, imageFile, outputDir, baseName, frameRange, framePadding ):
    _addTextFieldButton( imageFile, 'Hold Frame:',
        'from homework import holdFrames; holdFrames._dialog(1, "Image", "' + imageFile + '")' )
    _addTextField( baseName, 'Base Name:', 200 )
    _addTextField( frameRange, 'Frame Range:', 200 )
    _addOptionMenu( framePadding, 'Frame Padding:' )
    _addTextFieldButton( outputDir, 'Output Directory:', 
        ('from homework import holdFrames; holdFrames._dialog(3, "Output Directory", "' + outputDir + '")') )
    _addButtons( window, 
        'from homework import holdFrames; holdFrames._doIt( \
        "' + imageFile + '", \
        "' + outputDir + '", \
        "' + baseName + '", \
        "' + frameRange + '", \
        "' + framePadding + '", )' )
    
def _addTextFieldButton( text, label, command ):
    _addTextField( text, label, 410 )
    cmds.button( (text + 'Btn'), label='Browse...', width=105, command=command )
    
def _addTextField( text, label, width ):
    _addText( text, label )
    cmds.textField( (text + 'TF'), width=width )
    
def _addText( text, label ):
    cmds.text( (text + 'Txt'), label=label )
    
def _addOptionMenu( text, label ):
    _addText( text, label )
    cmds.optionMenu( ( text + 'DD') )
    _buildFramePaddings( 4 )
    
def _addButtons( window, command ):
    cmds.separator( 'sep', style='in' )
    cmds.button( 'okBtn', label='OK', width=150, command=command )
    cmds.button( 'cancelBtn', label='Cancel', width=150, 
        command=('cmds.deleteUI( "' + window + '")') )
    
def _positionControls( mainForm, imageFile, outputDir, baseName, frameRange, framePadding ):
    _attachFileField( mainForm, imageFile, 'top', [12, 10, 8] )
    _attachField( mainForm, baseName, 'TF', (imageFile + 'TF') )
    _attachField( mainForm, frameRange, 'TF', (baseName + 'TF') )
    _attachField( mainForm, framePadding, 'DD', (frameRange + 'TF') )
    _attachFileField( mainForm, outputDir, 'bottom', [45, 40, 39] )
    _attachButtons( mainForm )
    
def _attachFileField( mainForm, attach, topBottom, position ):
    cmds.formLayout( mainForm, edit=True,
        attachForm=[((attach + 'Txt'), "left", 22),
                    ((attach + 'Txt'), topBottom, position[0])] )
    
    cmds.formLayout( mainForm, edit=True,
        attachForm=[((attach + 'TF'), "left", 120),
                    ((attach + 'TF'), topBottom, position[1])] )
    
    cmds.formLayout( mainForm, edit=True,
        attachForm=[((attach + 'Btn'), "left", 535),
                    ((attach + 'Btn'), topBottom, position[2])] )
    
def _attachField( mainForm, attach, type, attachTo ):
    _attachFormControl( mainForm, (attach + 'Txt'), 22, attachTo, 7 )
    _attachFormControl( mainForm, (attach + type), 120, attachTo, 5 )

def _attachButtons( mainForm ):
    cmds.formLayout( mainForm, edit=True,
        attachForm=[('sep', "left", 0),
                    ('sep', "right", 0),
                    ('sep', "bottom", 25)] )
                    
    cmds.formLayout( mainForm, edit=True,
        attachForm=[('okBtn', "left", 350),
                    ('okBtn', "bottom", 0),
                    ('okBtn', 'right', 500)],
        attachControl=[('okBtn', "top", 0, 'sep')] )
        
    cmds.formLayout( mainForm, edit=True,
        attachForm=[('cancelBtn', "right", 1000),
                    ('cancelBtn', "bottom", 0)],
        attachControl=[('cancelBtn', "left", 0, 'okBtn'),
                       ('cancelBtn', "top", 0, 'sep')] )
    
def _attachFormControl( mainForm, control, leftValue, topOf, topValue ):
    cmds.formLayout( mainForm, edit=True,
        attachForm=[(control, "left", leftValue)],
        attachControl=[(control, "top", topValue, topOf)] )
    
def _resizeAndShowWindow( window, widthHeight ):
    cmds.window( window, edit=True, widthHeight=widthHeight )
    cmds.showWindow( window )
    
def _dialog(mode, caption, text):
    filename = cmds.fileDialog2( fileMode=mode, caption=caption )
    cmds.textField( (text + 'TF'), edit=True, text=filename[0] )
    
def _buildFramePaddings( max ):
    for i in reversed(range(1,(max+1))):
        cmds.menuItem( label=('#'*i) )
    
def _doIt( imageFile, outputDir, baseName, frameRange, framePadding ):
    cmds.waitCursor( state=True )
    
    src = _getTextFieldValue( imageFile + 'TF' )
    fileName, fileExtension = os.path.splitext( src )
    dir = _getTextFieldValue( outputDir + 'TF' )
    baseName = _getTextFieldValue( baseName + 'TF' )
    frames = _getFrames( frameRange + 'TF' )
    padding = len( _getOptionMenuValue(framePadding + 'DD') )

    if not re.search('^[a-zA-Z0-9_-]+$', baseName):
        _cursorError( 'Invalid base name.' )

    if int(max(frames)) > int('9'*padding):
        _cursorError( '1 or more frames in the frame range are longer than the frame padding.' )
    
    for frame in frames:
        frameNumPadded = (('0'*padding) + str(frame))[(-1*padding):]
        newFileName = baseName + '.' + frameNumPadded + fileExtension
        dst = dir + '/' + newFileName
        
        try:
            shutil.copy2(src, dst)
        except IOError:
            _cursorError( 'Invalid Hold Frame source file or output directory.' )
        
    cmds.waitCursor( state=False )
    
def _getTextFieldValue( field ):
    return cmds.textField( field, query=True, text=True )
    
def _getOptionMenuValue( field ):
    return cmds.optionMenu( field, query=True, value=True )
    
def _getFrames( frameRange ):
    fr = _getTextFieldValue( frameRange )
    frames = []
    
    if not re.search('^\d+(\s*[-,]?\s*\d+)*$', fr):
        _invalidFrameRange()
    
    fr = fr.replace(' ', '')
    frameRanges = fr.split(',')
    
    for f in frameRanges: 
        if re.search('^[0-9]+[-][0-9]+$', f):
            start, end = f.split('-')
            
            if int(start) > int(end):
                cmds.warning( 'Start of range is greater than end. Will not create any frames.' )
            
            for i in range(int(start), (int(end)+1)):
                frames.append(i)
        elif re.search('^[0-9]+$', f):
            frames.append( re.search('^[0-9]+$', f).group() )
        else:
            _invalidFrameRange()
    
    if len(frames) == 0:
        _invalidFrameRange()
    
    return frames
    
def _invalidFrameRange():
    _cursorError( 'Invalid frame range' )
    
def _cursorError( errorMessage ):
    cmds.waitCursor( state=False )
    cmds.error( errorMessage )