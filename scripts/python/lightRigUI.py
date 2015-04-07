from maya import cmds

def lightRigUI():

  lrWin = "lightRigWin"

  if cmds.window(lrWin, exists=True):
    cmds.deleteUI(lrWin)
  if cmds.windowPref(lrWin, exists=True):
    cmds.windowPref(lrWin, remove=True)

  winWidth = 425
  winHeight = 430

  cmds.window(lrWin, width=winWidth, height=winHeight, sizeable=False, menuBar=True, title="Light Rig")

  cmds.menu(label="Help")
  cmds.menuItem(label="About...", command="import lightRigUI;lightRigUI.glr_aboutWin()")

  cmds.frameLayout(borderVisible=1, borderStyle="etchedIn", labelVisible=0)
  mainForm = cmds.formLayout("mainForm")

  # Build controls
  numTxt = cmds.text("numTxt", label="Number of lights:")

  numLightsRC = cmds.radioCollection("numLightsRC")
  nineRB = cmds.radioButton("nineRB", label="9", select=True)
  sixteenRB = cmds.radioButton("sixteenRB", label="16")
  twentyfiveRB = cmds.radioButton("twentyfiveRB", label="25")
  thirtysixRB = cmds.radioButton("thirtysixRB", label="36")
      
  colorCSG = cmds.colorSliderGrp("colorCSG", label="Color", rgb=[1, 1, 1])
  intFSG = cmds.floatSliderGrp("intFSG", max=10, min=0, fieldMaxValue=10000, fieldMinValue=-10000, value=1, field=True, label="Intensity")
  specCB = cmds.checkBox("specCB", label="Emit Specular")
  caFSG = cmds.floatSliderGrp("caFSG", min=0,  max=180, value=40, field=True, label="Cone Angle")
  paFSG = cmds.floatSliderGrp("paFSG", min=-10, max=10, fieldMaxValue=180, fieldMinValue=-180, value=0, field=True, label="Penumbra Angle")
  dropFSG = cmds.floatSliderGrp("dropFSG", min=0, max=255, fieldMaxValue=10000, value=0, field=True, label="Dropoff")
  stTxt = cmds.text("stTxt", label="Shadow Type:")

  shadowTypesRC = cmds.radioCollection("shadowTypesRC")
  noneRB = cmds.radioButton("noneRB", label="None", select=True, onCommand=("from maya import cmds;cmds.colorSliderGrp('scCSG', edit=True, enable=False); " + \
                                                                            "cmds.intSliderGrp('drISG', edit=True, enable=False); " + \
                                                                            "cmds.intSliderGrp('dfISG', edit=True, enable=False); " + \
                                                                            "cmds.floatSliderGrp('dbFSG', edit=True, enable=False); " + \
                                                                            "cmds.floatSliderGrp('lrFSG', edit=True, enable=False); " + \
                                                                            "cmds.intSliderGrp('srISG', edit=True, enable=False)"))
  dmRB = cmds.radioButton("dmRB", label="Depth Map", onCommand=("from maya import cmds;cmds.colorSliderGrp('scCSG', edit=True, enable=True); " + \
                                                                "cmds.intSliderGrp('drISG', edit=True, enable=True); " + \
                                                                "cmds.intSliderGrp('dfISG', edit=True, enable=True); " + \
                                                                "cmds.floatSliderGrp('dbFSG', edit=True, enable=True); " + \
                                                                "cmds.floatSliderGrp('lrFSG', edit=True, enable=False); " + \
                                                                "cmds.intSliderGrp('srISG', edit=True, enable=False)"))
  rtRB = cmds.radioButton("rtRB", label="Ray Trace", onCommand=("from maya import cmds;cmds.colorSliderGrp('scCSG', edit=True, enable=True); " + \
                                                                "cmds.intSliderGrp('drISG', edit=True, enable=False); " + \
                                                                "cmds.intSliderGrp('dfISG', edit=True, enable=False); " + \
                                                                "cmds.floatSliderGrp('dbFSG', edit=True, enable=False); " + \
                                                                "cmds.floatSliderGrp('lrFSG', edit=True, enable=True); " + \
                                                                "cmds.intSliderGrp('srISG', edit=True, enable=True)"))
                                                 
  scCSG = cmds.colorSliderGrp("scCSG", label="Shadow Color", enable=False, rgb=[0, 0, 0])
  drISG = cmds.intSliderGrp("drISG", min=16, max=8192, enable=False, value=512, field=True, label="Dmap Resolution")
  dfISG = cmds.intSliderGrp("dfISG", min=0, max=5, fieldMaxValue=10000, enable=False, value=1, field=True, label="Dmap Filter Size")
  dbFSG = cmds.floatSliderGrp("dbFSG", min=0, max=1, fieldMaxValue=10000, pre=3, enable=False, value=.001, field=True, label="Dmap Bias")
  lrFSG = cmds.floatSliderGrp("lrFSG", min=0, max=1, fieldMaxValue=10000, enable=False, field=True, label="Light Radius")
  srISG = cmds.intSliderGrp("srISG", min=1, max=40, fieldMaxValue=10000, enable=False, value=1, field=True, label="Shadow Rays")
  sep = cmds.separator("sep", style="in")
  createBtn = cmds.button("createBtn", label="Create Rig", command=("print ('Success!');from maya import cmds;cmds.deleteUI('" + lrWin + "')"))
  cancelBtn = cmds.button("cancelBtn", label="Cancel", command=("from maya import cmds;cmds.deleteUI('" + lrWin + "')"))

  # Position controls
  cmds.formLayout(mainForm, edit=True, attachForm=[(numTxt, "left", 80), (numTxt, "top", 10)])
  cmds.formLayout(mainForm, edit=True, attachControl=[nineRB, "left", 15, numTxt], attachForm=[nineRB, "top", 10])
  cmds.formLayout(mainForm, edit=True, attachControl=[sixteenRB, "left", 10, nineRB], attachForm=[sixteenRB, "top", 10])
  cmds.formLayout(mainForm, edit=True, attachControl=[twentyfiveRB, "left", 10, sixteenRB], attachForm=[twentyfiveRB, "top", 10])
  cmds.formLayout(mainForm, edit=True, attachControl=[thirtysixRB, "left", 10, twentyfiveRB], attachForm=[thirtysixRB, "top", 10])

  cmds.formLayout(mainForm, edit=True, attachForm=[(colorCSG, "left", -40), (colorCSG, "right", 40)], attachControl=[colorCSG, "top", 10, numTxt])
  cmds.formLayout(mainForm, edit=True, attachForm=[(intFSG, "left", -40), (intFSG, "right", 40)], attachControl=[intFSG, "top", 5, colorCSG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(specCB, "left", 103), (specCB, "right", 40)], attachControl=[specCB, "top", 5, intFSG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(caFSG, "left", -40), (caFSG, "right", 40)], attachControl=[caFSG, "top", 5, specCB])
  cmds.formLayout(mainForm, edit=True, attachForm=[(paFSG, "left", -40), (paFSG, "right", 40)], attachControl=[paFSG, "top", 5, caFSG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(dropFSG, "left", -40), (dropFSG, "right", 40)], attachControl=[dropFSG, "top", 5, paFSG])

  cmds.formLayout(mainForm, edit=True, attachForm=[stTxt, "left", 55], attachControl=[stTxt, "top", 10, dropFSG])
  cmds.formLayout(mainForm, edit=True, attachControl=[(noneRB, "left", 15, stTxt), (noneRB, "top", 10, dropFSG)])
  cmds.formLayout(mainForm, edit=True, attachControl=[(dmRB, "left", 10, noneRB), (dmRB, "top", 10, dropFSG)])
  cmds.formLayout(mainForm, edit=True, attachControl=[(rtRB, "left", 10, dmRB), (rtRB, "top", 10, dropFSG)])

  cmds.formLayout(mainForm, edit=True, attachForm=[(scCSG, "left", -40), (scCSG, "right", 40)], attachControl=[scCSG, "top", 10, stTxt])
  cmds.formLayout(mainForm, edit=True, attachForm=[(drISG, "left", -40), (drISG, "right", 40)], attachControl=[drISG, "top", 5, scCSG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(dfISG, "left", -40), (dfISG, "right", 40)], attachControl=[dfISG, "top", 5, drISG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(dbFSG, "left", -40), (dbFSG, "right", 40)], attachControl=[dbFSG, "top", 5, dfISG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(lrFSG, "left", -40), (lrFSG, "right", 40)], attachControl=[lrFSG, "top", 5, dbFSG])
  cmds.formLayout(mainForm, edit=True, attachForm=[(srISG, "left", -40), (srISG, "right", 40)], attachControl=[srISG, "top", 5, lrFSG])

  cmds.formLayout(mainForm, edit=True, attachForm=[(sep, "left", 0), (sep, "right", 0), (sep, "bottom", 25)])
  cmds.formLayout(mainForm, edit=True, attachForm=[(createBtn, "left", 0), (createBtn, "bottom", 0)], attachControl=[createBtn, "top", 0, sep], attachPosition=[createBtn, "right", 0, 50])
  cmds.formLayout(mainForm, edit=True, attachControl=[(cancelBtn, "left", 0, createBtn), (cancelBtn, "top", 0, sep)], attachForm=[(cancelBtn, "right", 0), (cancelBtn, "bottom", 0)])

  cmds.window(lrWin, edit=True, width=winWidth, height=winHeight)

  cmds.showWindow(lrWin)


def glr_aboutWin():

  aboutWindow = "AboutWin"

  if cmds.window(aboutWindow, exists=True):
    cmds.deleteUI(aboutWindow)

  cmds.window(aboutWindow, resizeToFitChildren=True, sizeable=False, title="About Light Rig")

  cmds.frameLayout(borderVisible=True, borderStyle="etchedIn", labelVisible=False)
  cmds.columnLayout()
  cmds.text(label="Created by: Mike Harris", align="left")
  cmds.text(label="This is a Spot Light Rig utility that generates", align="left")
  cmds.text(label="a lighting setup to simulate soft area lighting.", align="left")
  cmds.text(label="")
  cmds.text(label="If you have any comments or suggestions", align="left")
  cmds.text(label="you can contact me at: pipeTD@gmail.com", align="left")

  cmds.showWindow(aboutWindow)
