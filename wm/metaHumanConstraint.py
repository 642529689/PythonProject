import pymel.core as pm

def metaHumanConstraint():
    mh_dict = { 'Root':'pelvis',
                'Spine1':'spine_01',
                'Spine2':'spine_02',
                'Spine3':'spine_03',
                'Spine4':'spine_04',
                'Chest':'spine_05',
                'Scapula':'clavicle',
                'Shoulder':'upperarm',
                'Elbow':'lowerarm',
                'Wrist':'hand',
                'IndexFinger0':'index_metacarpal',
                'IndexFinger1':'index_01',
                'IndexFinger2':'index_02',
                'IndexFinger3':'index_03',
                'MiddleFinger0':'middle_metacarpal',
                'MiddleFinger1':'middle_01',
                'MiddleFinger2':'middle_02',
                'MiddleFinger3':'middle_03',
                'RingFinger0':'ring_metacarpal',
                'RingFinger1':'ring_01',
                'RingFinger2':'ring_02',
                'RingFinger3':'ring_03',
                'PinkyFinger0':'pinky_metacarpal',
                'PinkyFinger1':'pinky_01',
                'PinkyFinger2':'pinky_02',
                'PinkyFinger3':'pinky_03',
                'ThumbFinger1':'thumb_01',
                'ThumbFinger2':'thumb_02',
                'ThumbFinger3':'thumb_03',
                'Neck':'neck_01',
                'Head':'head',
                'Hip':'thigh',
                'Knee':'calf',
                'Ankle':'foot',
                'Toes':'ball'
             }
    sideRight = 'r_drv'
    sideLeft = 'l_drv'
    sideMiddle = 'drv'
    sideBeforeName = 0
    sideUnderScore = 1

    ## 遍历 mh_dict 字典的内容
    for adv_name, mh_name in mh_dict.items():
        if pm.objExists('%s_L'%adv_name):
            if pm.objExists('{}_{}'.format(mh_name, sideLeft)):
                pm.parentConstraint('%s_L'%adv_name, '{}_{}'.format(mh_name, sideLeft), mo=True)
        if pm.objExists('%s_R'%adv_name):
            if pm.objExists('{}_{}'.format(mh_name, sideRight)):
                pm.parentConstraint('%s_R'%adv_name, '{}_{}'.format(mh_name, sideRight), mo=True)
        if pm.objExists('%s_M'%adv_name):
            if pm.objExists('{}_{}'.format(mh_name, sideMiddle)):
                pm.parentConstraint('%s_M'%adv_name, '{}_{}'.format(mh_name, sideMiddle), mo=True)

# 运行 metaHumanConstraint
metaHumanConstraint()


    
    
        

    
        
        
        
        
        
        
        