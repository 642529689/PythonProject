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
        pm.addAttr(node, ln='selObjects', dt='message', multi=True, im = False)
        for obj in objs:
            pm.connectAttr(obj + '.message', node + '.selObjects')

