import maya.cmds as cmds

def ysNewConnect(*args):
    sel = cmds.ls(sl=True)
    if len(sel) != 2:
        cmds.warning('请先选择自己创建的曲线 再加选 "All_Con" 控制器')
        return
    
    defCurve = sel[1].split(':')
    if len(defCurve) == 1:
        defCurve = 'pathCurve'
    else:
        defCurve = '%s:pathCurve' % defCurve[0]

    cmds.connectAttr(sel[0]+'.worldSpace[0]', defCurve+'.create', force = True)
    
def ysDefConnect(*args):
    sel = cmds.ls(sl=True)
    if len(sel) != 1:
        cmds.warning('请选择 "All_Con" 控制器')
        return
    
    defCurve = sel[0].split(':')
    if len(defCurve) == 1:
        oldCurve = 'oldCurve'
        defCurve = 'pathCurve'        
    else:
        oldCurve = '%s:oldCurve'% defCurve[0]
        defCurve = '%s:pathCurve'% defCurve[0]        

    cmds.connectAttr(oldCurve+'.worldSpace[0]', defCurve+'.create', force = True)
  
if cmds.window('connectWin', exists=True):
    cmds.deleteUI('connectWin')

cmds.window('connectWin', width=150 )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='创建新链接', command=ysNewConnect )
cmds.button( label='恢复默认', command=ysDefConnect )

cmds.showWindow('connectWin')
