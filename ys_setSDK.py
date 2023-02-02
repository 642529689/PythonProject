import maya.cmds as cmds
import pymel.core as pm

class ys_setSDk:
    defnumT = 0
    defnumR = 0
    defnumS = 0
    def showWin(self):  
        if cmds.window('setSDKWin', ex= True):
            cmds.deleteUI('setSDKWin')
            
        cmds.window('setSDKWin')
        cmds.columnLayout( 'setSDKcolumnLayout', columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )

        cmds.setParent('setSDKcolumnLayout')
        cmds.rowLayout('jointLayout', numberOfColumns = 3,columnWidth3 = (30,150,20))
        cmds.text('jointText',l='joint')
        cmds.textField('jointTextField', w = 180)
        cmds.button('jointbtn',l='...',c = "lodSelectedName('joint')")

        cmds.setParent('setSDKcolumnLayout')
        cmds.rowLayout('objLayout', numberOfColumns = 3,columnWidth3 = (30,150,20))
        cmds.text('objText',l='ctrl')
        cmds.textField('objTextField', w = 180)
        cmds.button('objbtn',l='...',c = "lodSelectedName('obj')")
        
        cmds.setParent('setSDKcolumnLayout')
        cmds.columnLayout('rebuildLayout')
        cmds.rowColumnLayout('ctrlDefLayout', numberOfColumns = 6)
        cmds.text('objText',l='ctrl', w = 40)
        cmds.textField('objTextField', w = 40)

        cmds.setParent('setSDKcolumnLayout')
        cmds.button('ctrlDef', l= 'ctrlDef', c = "ctrlDef()")
        cmds.button('apple', l= 'apple', c = "action()")
        
        cmds.showWindow()


def lodSelectedName(btnname):
    obj = pm.selected()[0]
    cmds.textField('%sTextField'%btnname, e= True, tx= str(obj))
    if btnname == 'joint':
        defnumT = obj.t.get()
        defnumR = obj.r.get()
        defnumS = obj.s.get()
            
def action():
    joint = cmds.textField('jointTextField', q= True, tx= True)
    obj = cmds.textField('objTextField', q= True, tx= True)

def ctrlDef():
    if cmds.rowColumnLayout('ctrlDefLayout', ex= True):
        cmds.deleteUI('ctrlDefLayout')
    cmds.setParent('rebuildLayout')
    cmds.rowColumnLayout('ctrlDefLayout', numberOfColumns =2)
    obj = pm.selected()[0]
    attrs = pm.listAttr(obj, k = True)
    for attr in attrs:
        num = pm.PyNode('%s.%s'%(obj,attr)).get()
        cmds.text('%sText'%attr, l= attr, w = 80)
        cmds.textField('%sTextField'%attr, tx = '%.2f'%num, w = 40)
    
win = ys_setSDk()
win.showWin()
