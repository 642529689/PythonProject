import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import re

def ys_replaceHash(string, number):
    result = ''
    substring = '#'
    # 提取 批量命名中的字符串部分
    substringName = re.sub(substring, '', string)
    print(substringName)
    # 提取 批量命名中的数字部分
    substringNum = string.count(substring)
    print(substringNum) 
    # 替换 批量命名中的字符串部分
    result = '{}{}'.format(substringName, number.zfill(substringNum))
    return result

def ys_hashRename(newName):
    count = 0
    result = []
    objs = pm.selected()
    if len(objs) > 0:
        node = pm.createNode('unknown')
        pm.select(node, r=True)
        mel.eval('addAttr -ln "selObjects" -at message -multi -im 0;')   
        ##pm.addAttr(node, ln='selObjects', dt='message', multi=True, im = False)
        for obj in objs:
            pm.connectAttr(obj + '.message', node + '.selObjects', na =True)
        con = pm.listConnections(node + '.selObjects')

        for x in range(len(con)):
            tmp = pm.listConnections(node  + '.selObjects[{}]'.format(x))
            obj = tmp[0]
            name = ys_replaceHash(newName, str(int(x) + 1))
            pm.rename(obj, name)
            print('ReName: {} --> {} \n'.format(obj, name))
        
        result = pm.listConnections(node + '.selObjects')
        pm.delete(node)
    
    if len(result) > 0:
        pm.select(result)   
    return result

            
ys_hashRename('asdf_###')