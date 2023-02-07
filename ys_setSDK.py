import maya.cmds as cmds
import pymel.core as pm

defnumT = 0
defnumR = 0
defnumS = 0
ctrlDefnum = []
ctrlNewnum = []
class ys_setSDk:
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
    joint = pm.PyNode(joint)
    obj = pm.PyNode(obj)
    attrs = pm.listAttr(obj, k = True)
    for attr in attrs:
        attr = pm.PyNode(attr)
        num = obj.attr.get()
        ctrlNewnum.append([attr,num])
    if ctrlNewnum != ctrlDefnum:
        attr = 0
        attrT = joint.t.get()
        attrR = joint.r.get()
        attrS = joint.s.get()
        for i in enumerate(ctrlNewnum):
            if ctrlNewnum[i] != ctrlDefnum[i]:
                attr = i

        if attrT[0] != defnumT[0]:
            pm.setDrivenKeyframe(joint.tx, cd = '%s.%s'%(obj,ctrlNewnum[attr][0]), v = attrT[0], dv = ctrlNewnum[attr][1])
            pm.setDrivenKeyframe(joint.tx, cd = '%s.%s'%(obj,ctrlDefnum[attr][0]), v = defnumT[0], dv = ctrlDefnum[attr][1])

        if attrT[1] != defnumT[1]:
            pm.setDrivenKeyframe(joint.ty, cd = '%s.%s'%(obj,ctrlNewnum[attr][0]), v = attrT[1], dv = ctrlNewnum[attr][1])
            pm.setDrivenKeyframe(joint.ty, cd = '%s.%s'%(obj,ctrlDefnum[attr][0]), v = defnumT[1], dv = ctrlDefnum[attr][1])

        if attrT[2] != defnumT[2]:
            pm.setDrivenKeyframe(joint.tz, cd = '%s.%s'%(obj,ctrlNewnum[attr][0]), v = attrT[2], dv = ctrlNewnum[attr][1])
            pm.setDrivenKeyframe(joint.tz, cd = '%s.%s'%(obj,ctrlDefnum[attr][0]), v = defnumT[2], dv = ctrlDefnum[attr][1])

def ctrlDef():
    obj = pm.selected()[0]
    attrs = pm.listAttr(obj, k = True)
    for attr in attrs:
        num = pm.PyNode('%s.%s'%(obj,attr)).get()
        ctrlDefnum.append([attr,num])
    
win = ys_setSDk()
win.showWin()
