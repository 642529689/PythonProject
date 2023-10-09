import maya.cmds as cmds

def ysNewConnect(*args):
    print 'Button 1 was pushed.'
    
def ysNewConnect(*args):
    print 'Button 1 was pushed.'
  
if cmds.window('connectWin', exists=True):
    cmds.deleteUI('connectWin')

cmds.window('connectWin', width=150 )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='创建新链接', command=ysNewConnect )
cmds.button( label='恢复默认', command=defaultButtonPush )

cmds.showWindow('connectWin')
