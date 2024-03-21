
import json
import pymel.core as pm
import maya.cmds as cmds


class facial_edit():
    def __init__(self):
        self.jsonData = {}
        self.jointName = {}
        self.ctrlName = {}
        self.attrName = []


    def create_window(self):
        if cmds.window('facial_edit_Window', exists=True):
            cmds.deleteUI('facial_edit_Window')
        myWindow = cmds.window('facial_edit_Window', title='facial_edit')
        cmds.scrollLayout( 'scrollLayout', w = 370 )
        cmds.columnLayout('columnLayout', rowSpacing=10)
        cmds.frameLayout('eFrameLayout', label='额', collapsable=True)
        cmds.columnLayout('eColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('meiFrameLayout', label='眉', collapsable=True)
        cmds.columnLayout('meiColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('yanFrameLayout', label='眼', collapsable=True)
        cmds.columnLayout('yanColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('biFrameLayout', label='鼻', collapsable=True)
        cmds.columnLayout('biColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('zuiFrameLayout', label='嘴', collapsable=True)
        cmds.columnLayout('zuiColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('erFrameLayout', label='耳', collapsable=True)
        cmds.columnLayout('erColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('lianFrameLayout', label='脸', collapsable=True)
        cmds.columnLayout('lianColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('xiaheFrameLayout', label='下颌', collapsable=True)
        cmds.columnLayout('xiaheColumnLayout', w = 350)
        cmds.setParent('columnLayout')
        cmds.frameLayout('otherFrameLayout', label='其他', collapsable=True)
        cmds.columnLayout('otherColumnLayout', w = 350)

        self.bulid_Slider('etouliangce_T_LR','meiColumnLayout','额头两侧—位移—左右')

        cmds.setParent('columnLayout')
        cmds.button(label='读取json', w=150, c=self.load_button_cmd)
        cmds.showWindow(myWindow)

    def load_json(self, file_path):
        self.jsonData = {}
        with open(file_path, 'r') as file:
            self.jsonData = json.load(file)
    
    def load_json_jointName(self, json_data):
        joint_name = json_data['Jointname']
        return joint_name
    
    def load_json_ctrlName(self, json_data):
        self.ctrlName.clear()
        for i in json_data:
            self.ctrlName[i] = None
    
    def build_UI(self, json_data):
        joint_name = self.load_json_jointName(json_data)
        ctrl_name = self.load_json_ctrlName(json_data)
        self.bulid_Slider(ctrl_name,joint_name)

    def load_button_cmd(self,*args):
        jsonFile = cmds.fileDialog2(fileFilter='*.json',fileMode=1,caption='选择json文件')
        self.load_json(jsonFile[0])
        self.load_json_ctrlName(self.jsonData)
        for ctrlName in self.ctrlName:
            names = ctrlName.split('_')
            cn_name = ''
            for name in names:
                cn_name += self.en_to_cn(name)
            parent = self.ctrlName_to_parent(names[0])
            self.bulid_Slider(ctrlName,parent,cn_name)
        print('orve')

    def en_to_cn(self,en):
        cn_str = {
        'yingtang':'印堂','etou':'额头','xiaerkuo':'下耳廓','menya':'门牙','yachixia':'牙齿下','yachishang':'牙齿上',
        'shangyanpinei':'上眼皮内','shangyanpiwai':'上眼皮外','xiayanpiwai':'下眼皮外','xiayanpizhong':'下眼皮中',
        'xiahejiao':'下颌角','lianjia':'脸颊','quangu':'颧骨','saibang':'腮帮','xiaba':'下巴','xiahe':'下颌',
        'etouliangce':'额头两侧','pinguoji':'苹果机','xiabaliangce':'下巴两侧','erchui':'耳垂','erkuo':'耳廓',
        'erduo':'耳朵','bizhong':'鼻梁','biyi':'鼻翼','bitou':'鼻头','bidi':'鼻底','waiyanjiao':'外眼角',
        'shangyanpi':'上眼皮','xiayanpi':'下眼皮','yanjing':'眼睛','taiyangxue':'太阳穴','shangyanpizhong':'上眼皮中',
        'xiayanpinei':'下眼皮内','neiyanjiao':'内眼角','xiachunzhong':'下唇两侧','shangchunzhong':'上唇两侧','chunjiao':'唇角',
        'xiachun':'下唇中','shangchun':'上唇中','meiwei':'眉尾','meizhong':'眉中','meitou':'眉头','shangerkuo':'上耳廓',        
        'meimaozhengti':'眉毛','bizizhengti':'鼻子','zuizhengti':'嘴','yanqiu':'眼球','boziliangce':'脖子两侧',
        'T':'_位移','R':'_旋转','S':'_缩放','UL':'_上下','FB':'_前后','LR':'_左右',
        }
        return cn_str[en]
    
    def ctrlName_to_parent(self,ctrlName):
        e = ['etou', 'etouliangce']
        mei = ['meimaozhengti', 'meizhong', 'meitou', 'meiwei','yingtang']
        yan = ['yanqiu', 'yanjing', 
            'shangyanpi', 'shangyanpinei', 'shangyanpizhong', 'shangyanpiwai', 
            'xiayanpi', 'xiayanpinei', 'xiayanpizhong','xiayanpiwai',
            'neiyanjiao','waiyanjiao']
        bi = ['bizhong', 'bizizhengti', 'biyi', 'bitou', 'bidi', ]
        zui = ['zuizhengti', 'shangchunzhong', 'shangchun', 'xiachunzhong', 'xiachun', 'chunjiao']
        er = ['erduo', 'erkuo', 'shangerkuo', 'xiaerkuo', 'erchui',]
        lian = ['pinguoji','quangu','taiyangxue', 'lianjia','saibang']
        xiahe = ['xiaba','xiabaliangce','xiahe','xiahejiao','boziliangce',]
        other = ['yachixia','yachishang','mengya']

        if ctrlName in e:
            return 'eColumnLayout'
        if ctrlName in mei:
            return 'meiColumnLayout'
        if ctrlName in yan:
            return 'yanColumnLayout'
        if ctrlName in bi:
            return 'biColumnLayout'
        if ctrlName in zui:
            return 'zuiColumnLayout'
        if ctrlName in er:
            return 'erColumnLayout'
        if ctrlName in lian:
            return 'lianColumnLayout'
        if ctrlName in xiahe:
            return 'xiaheColumnLayout'
        if ctrlName in other:
            return 'otherColumnLayout'
        else:
            return 'otherColumnLayout'

    def set_zero(self, *args):
        for name in args:
            if cmds.floatSliderButtonGrp(name, ex= True):
                attr = cmds.floatSliderButtonGrp(name, query=True, ann=True)
                attr = attr.replace('_T', '.T')
                attr = attr.replace('_R', '.R')
                attr = attr.replace('_S', '.S')  
                pm.setAttr(attr, 0)                
                cmds.floatSliderButtonGrp(name, edit=True, v=0)  
            else:
                pass


    def slider_Changed(self, *args):
        # 在这里处理滑块变化的逻辑
        for name in args:
            if cmds.floatSliderButtonGrp(name, ex= True):
                new_val = cmds.floatSliderButtonGrp(name, query=True, value=True)
                attr = cmds.floatSliderButtonGrp(name, query=True, ann=True)
                attr = attr.replace('_T', '.T')
                attr = attr.replace('_R', '.R')
                attr = attr.replace('_S', '.S')                
                pm.setAttr(attr, new_val)
            else:
                pass

    def bulid_Slider(self, name, parent,cn_name):
        cmds.setParent(parent) 
        cmds.floatSliderButtonGrp ( name, ann = name, l = cn_name, field=True,
                                    minValue = -10, maxValue = 10, value = 0, 
                                    buttonLabel='Edit',bc='data.getDefaultValue(\'%s\')' % name,
                                    cw=[(1, 100), (2, 40), (3, 160), (4, 60)],
                                    cc='facial_edit().slider_Changed(\'%s\')' % name)   
        cmds.popupMenu( '%sPopupMenu'% name)
        cmds.menuItem( label='reset', c='facial_edit().set_zero(\'%s\')' % name)
        cmds.setParent('..')

class SDK_data():
    @classmethod
    def __init__(self):
        self.name = ''
        self.resetValue = []
        self.value0 = []
        self.value1 = []
        self.animCurveName = []
        print('create SDK_data')

    def  getDefaultValue(self,name):
        self.name = name
        if cmds.floatSliderButtonGrp(name, ex= True):
                attr = cmds.floatSliderButtonGrp(name, query=True, ann=True)
                attr = attr.replace('_T', '.T')
                attr = attr.replace('_R', '.R')
                attr = attr.replace('_S', '.S')  
                attr = pm.PyNode(attr)
                for curve in attr.outputs(p = True):
                    curve = pm.PyNode(curve.split('.')[0]) 
                    value0 = curve.getValue(index = 1)
                    value1 = curve.getValue(index = 2)

                    self.animCurveName.append(curve)
                    self.resetValue.append(value1 - value0)
                    self.value1.append(value1 - value0)
                    self.value0.append(value0)
        
        SDK_edit(name).create_window()

    def changed_button(self,value):
        print(self.animCurveName)
        if value == -0.5:            
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] - (self.value1[i] * 0.5)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))

        if value == -0.25:
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] - (self.value1[i] * 0.25)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))
        if value == -0.1:
           for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] - (self.value1[i] * 0.1)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))
        if value == 0:
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.resetValue[i]
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))
        if value == 0.1:
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] + (self.value1[i] * 0.1)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))
        if value == 0.25:
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] + (self.value1[i] * 0.25)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))
        if value == 0.5:
            for i in range(len(self.animCurveName)):
                self.value1[i] = self.value1[i] + (self.value1[i] * 0.5)
                self.animCurveName[i].setValue(2,(self.value0[i] + self.value1[i]))
                self.animCurveName[i].setValue(0,(self.value0[i] - self.value1[i]))

class SDK_edit():
    def __init__(self, name):
        self.name = name

    def create_window(self,):
        if cmds.window('SDK_edit_Window', exists=True):
            cmds.deleteUI('SDK_edit_Window')
        myWindow = cmds.window('SDK_edit_Window', title='SDK_edit')
        root = cmds.formLayout( w = 290, h = 110)
        alyout = cmds.rowLayout(numberOfColumns=7,adj = True)
        cmds.button(label='-0.5', c = 'data.changed_button(-0.5)')
        cmds.button(label='-0.25', c = 'data.changed_button(-0.25)')
        cmds.button(label='-0.1', c = 'data.changed_button(-0.1)')
        cmds.button(label='reset', c = 'data.changed_button(0)')
        cmds.button(label='+0.1', c = 'data.changed_button(0.1)')
        cmds.button(label='+0.25', c = 'data.changed_button(0.25)')
        cmds.button(label='+0.5', c = 'data.changed_button(0.5)')
        cmds.setParent('..')
        blyout = cmds.rowLayout(numberOfColumns=2,adj = True)
        cmds.button(label='apply', c = "cmds.deleteUI('SDK_edit_Window')")
        cmds.button(label='cancel', c = 'data.changed_button(0),cmds.deleteUI(\'SDK_edit_Window\')')
        cmds.setParent('..')

        cmds.formLayout(root, e=True, af=[(alyout, 'top',  20),
                                          (alyout, 'left', 20),
                                          (blyout, 'top',  70),
                                          (blyout, 'left', 170),])
                        
        cmds.showWindow(myWindow)  



            

            
fe = facial_edit()
data = SDK_data()
fe.create_window()