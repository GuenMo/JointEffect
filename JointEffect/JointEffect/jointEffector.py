# coding:utf-8

import pymel.all as pm

def hingeEffector(baseName, start, mid, end):
    startLoc = pm.spaceLocator(n=baseName + 'StartLoc')
    midLoc   = pm.spaceLocator(n=baseName + 'MidLoc')
    endLoc   = pm.spaceLocator(n=baseName + 'EndLoc')
    
    startLocShape = startLoc.getShape()
    midLocShape   = midLoc.getShape()
    endLocShape   = endLoc.getShape()
    
    pm.parent(endLoc, mid)
    endLoc.t.set(mid.t.get())
    endLoc.r.set(0,0,0)
    pm.parent(endLoc,w=True)
    
    pm.parentConstraint(start, startLoc, n=startLoc+'ParentConstraint', mo=False)
    pm.parentConstraint(mid, midLoc, n=midLoc+'ParentConstraint', mo=False)
    pm.parentConstraint(end, endLoc, n=endLoc+'ParentConstraint', mo=True)
    
    startToMidVector = pm.createNode('plusMinusAverage', n=baseName+'StartToMidVector'.format(start,mid))
    startToEndVector = pm.createNode('plusMinusAverage', n=baseName+'StartToEndVector'.format(start,end))
    startToMidVector.operation.set(2)
    startToEndVector.operation.set(2)
    
    midLocShape.worldPosition.connect(startToMidVector.input3D[0])
    startLocShape.worldPosition.connect(startToMidVector.input3D[1])
    
    endLocShape.worldPosition.connect(startToEndVector.input3D[0])
    startLocShape.worldPosition.connect(startToEndVector.input3D[1])
    
    #Rotation
    xAxis = pm.createNode('vectorProduct', n=baseName+'XAxis')
    yAxis = pm.createNode('vectorProduct', n=baseName+'YAxis')
    zAxis = pm.createNode('vectorProduct', n=baseName+'ZAxis')
    xAxis.operation.set(0)
    yAxis.operation.set(2)
    zAxis.operation.set(2)
    xAxis.normalizeOutput.set(1)
    yAxis.normalizeOutput.set(1)
    zAxis.normalizeOutput.set(1)
    
    startToEndVector.output3D.connect(xAxis.input1)
    startToMidVector.output3D.connect(yAxis.input1)
    startToEndVector.output3D.connect(yAxis.input2)
    startToMidVector.output3D.connect(zAxis.input1)
    yAxis.output.connect(zAxis.input2)
    
    #Translate
    dot = pm.createNode('vectorProduct', n=baseName+'Dotproduct')
    dot.operation.set(1)
    startToMidVector.output3D.connect(dot.input1)
    startToEndVector.output3D.connect(dot.input2)
    
    distance = pm.createNode('distanceBetween', n=baseName+'StartToEndDistance')
    endLocShape.worldPosition.connect(distance.point1)
    startLocShape.worldPosition.connect(distance.point2)
    
    project = pm.createNode('multiplyDivide', n=baseName+'Project')
    project.operation.set(2)
    dot.output.connect(project.input1)
    distance.distance.connect(project.input2X)
    distance.distance.connect(project.input2Y)
    distance.distance.connect(project.input2Z)
    
    startToEndNVector = pm.createNode('vectorProduct', n=baseName+'StartToEndNVector')
    startToEndNVector.operation.set(0)
    startToEndVector.output3D.connect(startToEndNVector.input1)
    startToEndNVector.normalizeOutput.set(1)
    
    projectVector = pm.createNode('multiplyDivide', n=baseName+'ProjectVector')
    projectVector.operation.set(1)
    project.output.connect(projectVector.input2)
    startToEndNVector.output.connect(projectVector.input1)
    
    arrowVector = pm.createNode('plusMinusAverage', n=baseName+'ArrowVector')
    arrowVector.operation.set(2)
    projectVector.output.connect(arrowVector.input3D[0])
    startToMidVector.output3D.connect(arrowVector.input3D[1])
    
    arrowOffset = pm.createNode('multiplyDivide', n=baseName+'ArrowOffset')
    arrowOffset.operation.set(1)
    arrowVector.output3D.connect(arrowOffset.input1)
    
    effectDriver = pm.createNode('plusMinusAverage', n=baseName+'Driver')
    effectDriver.operation.set(1)
    midLocShape.worldPosition.connect(effectDriver.input3D[0])
    arrowOffset.output.connect(effectDriver.input3D[1])
    
    #Decompose Matrix
    matrix = pm.createNode('fourByFourMatrix', n=baseName+'Matrix')
    xAxis.outputX.connect(matrix.in00)
    xAxis.outputY.connect(matrix.in01)
    xAxis.outputZ.connect(matrix.in02)
    yAxis.outputX.connect(matrix.in10)
    yAxis.outputY.connect(matrix.in11)
    yAxis.outputZ.connect(matrix.in12)
    zAxis.outputX.connect(matrix.in20)
    zAxis.outputY.connect(matrix.in21)
    zAxis.outputZ.connect(matrix.in22)
    effectDriver.output3Dx.connect(matrix.in30)
    effectDriver.output3Dy.connect(matrix.in31)
    effectDriver.output3Dz.connect(matrix.in32)
    
    decomposMatrix = pm.createNode('decomposeMatrix', n=baseName+'DecomposeMatrix')
    matrix.output.connect(decomposMatrix.inputMatrix)
    
    
    effectCtrl = pm.curve(n=baseName+'EffectCtrl',d=3, p=[ (-0.500000, 0.000000, -0.000000), (-0.500000, 0.130602, -0.000000), (-0.391806, 0.391806, -0.000000), (-0.130602, 0.500000, -0.000000), (0.000000, 0.500000, -0.000000), (0.000000, 0.500000, 0.130602), (0.000000, 0.391806, 0.391806), (0.000000, 0.130602, 0.500000), (0.000000, -0.000000, 0.500000), (0.130602, -0.000000, 0.500000), (0.391806, -0.000000, 0.391806), (0.500000, -0.000000, 0.130602), (0.500000, -0.000000, 0.000000), (0.500000, 0.130602, -0.000000), (0.391806, 0.391806, -0.000000), (0.130602, 0.500000, -0.000000), (0.000000, 0.500000, -0.000000), (0.000000, 0.500000, -0.130602), (0.000000, 0.391806, -0.391806), (-0.000000, 0.130602, -0.500000), (-0.000000, 0.000000, -0.500000), (0.130602, 0.000000, -0.500000), (0.391806, 0.000000, -0.391806), (0.500000, 0.000000, -0.130602), (0.500000, -0.000000, 0.000000), (0.500000, -0.130602, 0.000000), (0.391806, -0.391806, 0.000000), (0.130602, -0.500000, 0.000000), (-0.000000, -0.500000, 0.000000), (-0.130602, -0.500000, 0.000000), (-0.391806, -0.391806, 0.000000), (-0.500000, -0.130602, 0.000000), (-0.500000, 0.000000, -0.000000), (-0.500000, 0.000000, -0.130602), (-0.391806, 0.000000, -0.391806), (-0.130602, 0.000000, -0.500000), (0.000000, 0.000000, -0.500000), (-0.000000, -0.130602, -0.500000), (-0.000000, -0.391806, -0.391806), (-0.000000, -0.500000, -0.130602), (-0.000000, -0.500000, -0.000000), (-0.000000, -0.500000, 0.130602), (-0.000000, -0.391806, 0.391806), (0.000000, -0.130602, 0.500000), (0.000000, -0.000000, 0.500000), (-0.130602, -0.000000, 0.500000), (-0.391806, -0.000000, 0.391806), (-0.500000, -0.000000, 0.130602), (-0.500000, 0.000000, -0.000000) ], k=[ 8, 8, 8, 9, 10, 10, 10, 11, 12, 12, 12, 13, 14, 14, 14, 15, 16, 16, 16, 17, 18, 18, 18, 19, 20, 20, 20, 21, 22, 22, 22, 23, 24, 24, 24, 25, 26, 26, 26, 27, 28, 28, 28, 29, 30, 30, 30, 31, 32, 32, 32 ])
    pm.addAttr(effectCtrl, ln='offset', at='double', dv=1, k=True)
    effectCtrlDrv = pm.group(effectCtrl,    n=effectCtrl+'Drv')
    effectCtrlGrp = pm.group(effectCtrlDrv, n=effectCtrl+'Grp')
    decomposMatrix.outputRotate.connect(effectCtrlGrp.rotate)
    decomposMatrix.outputTranslate.connect(effectCtrlGrp.translate)
    
    #
    grp = pm.group(n=baseName + 'Grp', em=True)
    pm.select(cl=True)
    effectJnt = pm.joint(n=baseName+'EffectJnt')
    pm.parentConstraint(effectCtrl, effectJnt, n=effectJnt+'ParentConstraint', mo=False)
    
    pm.parent(effectJnt, mid)
    pm.parent([startLoc,midLoc,endLoc,effectCtrlGrp], grp)
    
    offsetReverse = pm.createNode('multDoubleLinear', n=baseName+'OffsetReverse')
    offsetReverse.input2.set(-.1)
    effectCtrl.offset.connect(offsetReverse.input1)
    offsetReverse.output.connect(arrowOffset.input2X)
    offsetReverse.output.connect(arrowOffset.input2Y)
    offsetReverse.output.connect(arrowOffset.input2Z)
    
    
    for attr in ['rx','ry','rz','sx','sy','sz']:
        pm.setAttr(effectCtrl+'.'+attr, k=False, l=True)
    pm.setAttr(effectCtrl + '.v', k=False, cb=True)
    
    for loc in [startLoc, midLoc, endLoc]:
        loc.v.set(False)


#Sphere
def jointSet(name, direction):
    pm.select(cl=True)
    if direction == 'Up':
        pos = (0,1,0)
    elif direction == 'Down':
        pos = (0,-1,0)
    elif direction == 'Left':
        pos = (0,0,-1)
    elif direction == 'Right':
        pos = (0,0,1)
    elif direction == 'Front':
        pos = (1,0,0)
    elif direction == 'Back':
        pos = (-1,0,0)
    else:
        pos = (1,0,0)
    
    baseJnt = pm.joint(n=name+direction+'DrvJnt', p=(0, 0, 0))
    tipJnt  = pm.joint(n=name+direction+'Jnt', p=pos)
    pm.joint(baseJnt, sao='yup', zso=1, e=1, oj='xyz')
    tipJnt.jointOrientZ.set(0)
    loc = pm.spaceLocator(n=name+direction+'Loc')
    loc.translate.set(pos)
    locShape = loc.getShape()
    locShape.localScale.set(0.1,0.1,0.1)
    return [baseJnt, loc]

def createRange(baseName, distance1, distance2, defalutDistance):
    normalizeNode = pm.createNode('multiplyDivide', n=baseName+'Normalize')
    normalizeNode.operation.set(2)
    distance1.distance.connect(normalizeNode.input1X)
    distance2.distance.connect(normalizeNode.input1Y)
    defalutDistance.output.connect(normalizeNode.input2X)
    defalutDistance.output.connect(normalizeNode.input2Y)
    
    rangeNode = pm.createNode('setRange', n=baseName+'Range')
    rangeNode.min.set(0,0,0)
    rangeNode.max.set(1,1,1)
    rangeNode.oldMin.set(-1,-1,-1)
    rangeNode.oldMax.set(0,0,0)
    normalizeNode.outputX.connect(rangeNode.valueX)
    normalizeNode.outputY.connect(rangeNode.valueY)
    return rangeNode

def connectJoint(baseName, rangeNode, ctrl, direction1, direction2, joint1, joint2):
                                # mult1, mult2, init1, init2, joint1, joint2):
    
    multNode = pm.createNode('multiplyDivide', n=baseName + 'Mult')
    rangeNode.outValue.connect(multNode.input1)
    mult1 = pm.PyNode(ctrl.name() + '.' + direction1 + 'Mult')
    mult2 = pm.PyNode(ctrl.name() + '.' + direction2 + 'Mult')
    mult1.connect(multNode.input2X)
    mult2.connect(multNode.input2Y)
    
    addNode = pm.createNode('plusMinusAverage', n=baseName + 'Output')
    multNode.outputX.connect(addNode.input2D[0].input2Dx)
    multNode.outputY.connect(addNode.input2D[0].input2Dy)
    init1 = pm.PyNode(ctrl.name() + '.' + direction1 + 'Init')
    init2 = pm.PyNode(ctrl.name() + '.' + direction2 + 'Init')
    init1.connect(addNode.input2D[1].input2Dx)
    init2.connect(addNode.input2D[1].input2Dy)
    
    addNode.output2Dx.connect(joint1.tx)
    addNode.output2Dy.connect(joint2.tx)


def sphericalEffector(baseName):
    ctrl = pm.curve(n=baseName+'EffectorCtrl', p=[(0, 0, 1), (-1, 0, 0), (0, 0, -1), (1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (0, 0, 1), (0, 1, 0), (-1, 0, 0), (0, -1, 0), (1, 0, 0), (0, 1, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], d=1)
    pm.addAttr(ctrl, ln='defalutDistance', at='double', dv=1.414214, keyable=True)
    defalutDistance = pm.createNode('multDoubleLinear', n=baseName+'DefaultDistance')
    defalutDistance.input2.set(-1)
    ctrl.defalutDistance.connect(defalutDistance.input1)
    
    directions = ['Up','Down', 'Left', 'Right', 'Front', 'Back']
    for direction in directions:
        pm.addAttr(ctrl, ln=direction+'Init', at='double', dv=1, keyable=True)
        pm.addAttr(ctrl, ln=direction+'Mult', at='double', dv=1, keyable=True)
    
    
    upEffect    = jointSet(baseName, 'Up')
    downEffect  = jointSet(baseName, 'Down')
    leftEffect  = jointSet(baseName, 'Left')
    rightEffect = jointSet(baseName, 'Right')
    frontEffect = jointSet(baseName, 'Front')
    backEffect  = jointSet(baseName, 'Back')
    reader      = jointSet(baseName, 'Reader')
    
    effectList = [upEffect, downEffect, leftEffect, rightEffect, frontEffect, backEffect, reader]
    
    pm.select(cl=True)
    baseJnt = pm.joint(n=baseName+'BaseJnt')
    baseLoc = pm.spaceLocator(n=baseName+'BaseLoc')
    pm.parent([baseJnt,baseLoc], ctrl)
    
    for effect in effectList:
        pm.parent(effect[0], baseJnt)
        pm.parent(effect[1], baseLoc)
        
    pm.parentConstraint(reader[0].getChildren(), reader[1], n=reader[1]+'ParentConstraint', mo=False)
    
    # Distance
    readerLoc = reader[1]
    readerShape = readerLoc.getShape() 
    effectorNum = len(effectList)-1 
    
    distanceList = []
    for i in range(effectorNum):
        loc = effectList[i][1]
        locShape = loc.getShape()
        distancNode = pm.createNode('distanceBetween', n=loc.name().replace('Loc','_Distance'))
        locShape.worldPosition.connect(distancNode.point1)
        readerShape.worldPosition.connect(distancNode.point2)
        distanceList.append(distancNode)
    
    
    # Range
    UDRange = createRange(baseName+'_UD_', distanceList[0], distanceList[1], defalutDistance)
    LRRange = createRange(baseName+'_LR_', distanceList[2], distanceList[3], defalutDistance)
    FBRange = createRange(baseName+'_FB_', distanceList[4], distanceList[5], defalutDistance)
    
    # Connect Joint
    upJnt    = upEffect[0].getChildren()[0]
    downJnt  = downEffect[0].getChildren()[0]
    leftJnt  = leftEffect[0].getChildren()[0]
    rightJnt = rightEffect[0].getChildren()[0]
    frontJnt = frontEffect[0].getChildren()[0]
    backJnt  = backEffect[0].getChildren()[0]
    
    connectJoint(baseName+'_UD_', UDRange, ctrl, 'Up',   'Down',  upJnt, downJnt)
    connectJoint(baseName+'_LR_', LRRange, ctrl, 'Left', 'Right', leftJnt, rightJnt)
    connectJoint(baseName+'_FB_', FBRange, ctrl, 'Front','Back',  frontJnt, backJnt)


