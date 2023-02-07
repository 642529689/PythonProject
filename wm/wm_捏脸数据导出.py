

import pymel.core as pm
import os 

for path in os.walk('E:\\Projects\\maya_Project\\scenes'):
    for fileName in path[2]:
        pm.newFile(force = True)
        pm.importFile('%s\\%s'%(path[0], fileName))
        pm.select('Facial', hi = True)
        for obj in pm.selected():
            pm.currentTime(0)
            t0 = obj.t.get()
            r0 = obj.r.get()
            s0 = obj.s.get()
            pm.currentTime(2)
            t1 = obj.t.get()
            r1 = obj.r.get()
            s1 = obj.s.get()
            if t0 == t1 and r0 == r1 and s0 == s1:
                continue
            if t0 != t1:
                with open('E:\\Projects\\maya_Project\\scenes\\data.txt','a') as dataFile:
                    dataFile.write('%s--%s--tranlate--%.3f,%.3f,%.3f--%.3f,%.3f,%.3f\n'%(fileName[:-4], obj, t0[0], t0[1], t0[2], t1[0], t1[1], t1[2]))
            if t0 != t1:
                with open('E:\\Projects\\maya_Project\\scenes\\data.txt','a') as dataFile:
                    dataFile.write('%s--%s--tranlate--%.3f,%.3f,%.3f--%.3f,%.3f,%.3f\n'%(fileName[:-4], obj, t0[0], t0[1], t0[2], t1[0], t1[1], t1[2]))
            if t0 != t1:
                with open('E:\\Projects\\maya_Project\\scenes\\data.txt','a') as dataFile:
                    dataFile.write('%s--%s--tranlate--%.3f,%.3f,%.3f--%.3f,%.3f,%.3f\n'%(fileName[:-4], obj, t0[0], t0[1], t0[2], t1[0], t1[1], t1[2]))



