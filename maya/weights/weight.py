# coding:utf-8

import re

import pymel.core as pm
from maya.OpenMaya import *
from maya.OpenMayaAnim import *
import compute
reload(compute)


def convert_p(p):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(pm.currentUnit(q=1, l=1))
    return [p[i]*unit for i in range(3)]


def convert_length(l):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(pm.currentUnit(q=1, l=1))
    return l*unit


def convert_y(y):
    unit = {"mm": 0.1, "cm": 1.0, "m": 100.0, "in": 2.45, "ft": 7.62, "yd": 91.44}.get(pm.currentUnit(q=1, l=1))
    return y/unit


def get_shape(polygon):
    for shape in polygon.getShapes():
        if not shape.io.get():
            return shape


def assert_geometry(geometry=None, shape_type="mesh"):
    u"""
    :param geometry: 几何体
    :param shape_type: 形节点类型
    :return:
    判断物体是否为集合体
    """
    if geometry is None:
        selected = pm.selected(o=1)
        if len(selected) == 0:
            return pm.warning("please select a " + shape_type)
        geometry = selected[0]
    if geometry.type() == shape_type:
        return geometry.getParent()
    if geometry.type() != "transform":
        return pm.warning("please select a " + shape_type)
    shape = get_shape(geometry)
    if not shape:
        return pm.warning("please select a " + shape_type)
    if shape.type() != shape_type:
        return pm.warning("please select a " + shape_type)
    return geometry


def get_skin_cluster(polygon=None):
    u"""
    :param polygon: 多边形
    :return: 蒙皮节点
    """
    if polygon is None:
        polygon = assert_geometry(shape_type="mesh")
    if polygon is None:
        return
    for history in polygon.history(type="skinCluster"):
        return history
    pm.warning("\ncan not find skinCluster")


def ik_kwargs():
    polygon = assert_geometry()
    sk = get_skin_cluster(polygon)

    unlock_joints = [joint for joint in sk.getInfluence()
                     if joint.type() == "joint" and not joint.liw.get()]
    if len(unlock_joints) != 1:
        return pm.mel.warning("\nyou need a unlock joint")
    unlock_joint = unlock_joints[0]

    paint_joints = [joint for joint in sk.paintTrans.inputs() if joint.type() == "joint"]
    if len(paint_joints) != 1:
        return pm.mel.warning("\nyou need a paint joint")
    paint_joint = paint_joints[0]
    p = paint_joint.getTranslation(space="world")
    p = convert_p(p)
    v = [(i+j)/2 for i, j in zip(unlock_joint.getMatrix(ws=1)[0][:3], paint_joint.getMatrix(ws=1)[0][:3])]
    if (pm.datatypes.Point(p) * unlock_joint.getMatrix(ws=1).inverse())[0] < 0:
        v = [-i for i in v]

    ps = get_shape(polygon).getPoints(space="world")
    ps = [[ps[i][j] for j in range(3)] for i in range(len(ps))]
    wxs = compute.ik_xs(v, p, ps)
    return dict(
         wxs=wxs,
         sk=sk,
    )


def update_paint():
    polygon = assert_geometry()
    sk = get_skin_cluster(polygon)
    paint_joints = [joint for joint in sk.paintTrans.inputs() if joint.type() == "joint"]
    if len(paint_joints) != 1:
        return pm.mel.warning("\nyou need a paint joint")
    paint_joint = paint_joints[0]
    index = sk.influenceObjects().index(paint_joint)

    sk.ptw.set(sk.getWeights(get_shape(polygon), index))


def ik_solve(sk, wxs, xs, ys, r):
    r = pm.softSelect(q=1, ssd=1) * r * 2
    weights = compute.ik_weights(wxs, xs, ys, r)
    sk.ptw.set(weights)


def paint_ik(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制关节权重
    """
    ik_solve(xs=xs, ys=ys, r=r, **ik_kwargs())


def soft_xs(old_points, new_points):
    return [2 * (1 - (new[1] - old[1])) for old, new in zip(old_points, new_points)]


def soft_kwargs(*args):
    polygon = assert_geometry(shape_type="mesh")
    sk = get_skin_cluster(polygon)
    mesh = get_shape(polygon)
    pm.softSelect(sse=1)
    pm.softSelect(ssc="0,1,1,1,0,1")
    radius = pm.softSelect(q=1, ssd=1)
    pm.softSelect(ssd=radius * 2)
    old_points = mesh.getPoints(space="world")
    pm.move([0, convert_y(1), 0], r=1)
    new_points = mesh.getPoints(space="world")
    pm.move([0, -convert_y(1), 0], r=1)
    pm.softSelect(ssd=radius)
    wxs = [2 * (1 - (new[1] - old[1])) for old, new in zip(old_points, new_points)]
    return dict(
        wxs=wxs,
        sk=sk,
    )


def soft_solve(sk, wxs, xs, ys, r):
    ys = [1 - y for y in ys]
    weights = compute.soft_weights(wxs, xs, ys, r)
    sk.ptw.set(weights)


def paint_soft(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制软选次级权重
    """
    soft_solve(xs=xs, ys=ys, r=r, **soft_kwargs())


def joint_len(joint1, joint2):
    return convert_length((joint1.getTranslation(space="world")-joint2.getTranslation(space="world")).length())


def split_kwargs(vp=0):
    polygon = assert_geometry(shape_type="mesh")
    sk = get_skin_cluster(polygon)

    # indices
    influences = sk.getInfluence()
    joints = [joint for joint in influences if not joint.liw.get()]
    if vp:
        distance_joints = {(joint1.getTranslation(space="world")-joint2.getTranslation(space="world")).length(): [joint1, joint2]
                           for i, joint1 in enumerate(joints) for joint2 in joints[i+1:]}
        soft_joints = distance_joints[min(distance_joints.keys())]
        joints.remove(soft_joints[0])
        joints.remove(soft_joints[1])
        for i in range(len(joints)):
            distance_joints = {joint_len(joint1, joint2): [joint1, joint2]
                               for joint1 in joints for joint2 in [soft_joints[0], soft_joints[-1]]}
            soft_joint, star_end = distance_joints[min(distance_joints.keys())]
            if star_end == soft_joints[0]:
                soft_joints.insert(0, soft_joint)
            else:
                soft_joints.append(soft_joint)
            joints.remove(soft_joint)
        joints = soft_joints
    indices = MIntArray()
    indices.setLength(len(joints))
    for i, joint in enumerate(joints):
        indices[i] = influences.index(joint)

    # x_matrix
    def spine_vp(joint1, joint2):
        p = convert_p(joint2.getTranslation(space="world"))
        v = [(i + j) / 2 for i, j in zip(joint1.getMatrix(ws=1)[0][:3], joint2.getMatrix(ws=1)[0][:3])]
        if (pm.datatypes.Point(p) * joint1.getMatrix(ws=1).inverse())[0] < 0:
            v = [-i for i in v]
        return v, p

    def brow_vp(joint1, joint2):
        p1, p2 = joint1.getTranslation(space="world"), joint2.getTranslation(space="world")
        p2[1] = p1[1]
        p2[2] = p1[2]
        p = (p1 + p2) / 2
        v = (p2 - p1).normal()
        p = convert_p(p)
        return v, p

    def belt_vp(joint1, joint2):
        p1, p2 = joint1.getTranslation(space="world"), joint2.getTranslation(space="world")
        p = (p1 + p2) / 2
        v = (p2 - p1).normal()
        p = convert_p(p)
        return v, p

    vp_fns = [spine_vp, brow_vp, belt_vp]
    vps = [vp_fns[vp](joints[i], joint) for i, joint in enumerate(joints[1:])]
    vps = [[[v[0], v[1], v[2]], [p[0], p[1], p[2]]] for v, p in vps]
    ps = get_shape(polygon).getPoints(space="world")
    ps = [[ps[i][j] for j in range(3)] for i in range(len(ps))]
    wx_matrix = compute.split_wx_matrix(vps, ps)

    # max_weight
    selected = MSelectionList()
    selected.add(sk.name())
    selected.add(get_shape(polygon).name()+".vtx[*]")
    depend_node = MObject()
    selected.getDependNode(0, depend_node)
    fn_skin = MFnSkinCluster(depend_node)
    path = MDagPath()
    components = MObject()
    weights = MDoubleArray()
    selected.getDagPath(1, path, components)
    vtx_length = len(ps)
    joint_length = len(joints)
    fn_skin.getWeights(path, components, indices, weights)
    weights = [weights[i] for i in range(weights.length())]
    max_weights = compute.get_max_weights(weights, joint_length, vtx_length)
    return dict(
        wx_matrix=wx_matrix,
        max_weights=max_weights,
        fn_skin=fn_skin,
        path=path,
        components=components,
        indices=indices,
    )


def split_solve(wx_matrix, max_weights, fn_skin, path, components, indices,  xs, ys, r):
    r = pm.softSelect(q=1, ssd=1) * r * 2
    weights = compute.split_weights(wx_matrix, max_weights, xs, ys, r)
    api_weights = MDoubleArray()
    api_weights.setLength(len(weights))
    for i, w in enumerate(weights):
        api_weights[i] = weights[i]
    fn_skin.setWeights(path, components, indices, api_weights)
    update_paint()


def paint_spine(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制脊椎尾巴权重
    """
    split_solve(xs=xs, ys=ys, r=r, **split_kwargs(0))


def paint_brow(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制眉毛权重
    """
    split_solve(xs=xs, ys=ys, r=r, **split_kwargs(1))


def paint_belt(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制背带权重
    """
    split_solve(xs=xs, ys=ys, r=r, **split_kwargs(2))


def cloth_kwargs():
    polygon = assert_geometry(shape_type="mesh")
    sk = get_skin_cluster(polygon)

    # indices
    influences = sk.getInfluence()
    joints = [joint for joint in influences if not joint.liw.get()]
    indices = MIntArray()
    indices.setLength(len(joints))
    for i, joint in enumerate(joints):
        indices[i] = influences.index(joint)

    # wxs
    vtx_points = get_shape(polygon).getPoints(space="world")
    vtx_points = [[vtx_points[i][j] for j in range(3)] for i in range(len(vtx_points))]
    joint_points = [joint.getTranslation(space="world") for joint in joints]
    joint_points = [convert_p(joint_points[i]) for i in range(len(joint_points))]
    wx_matrix = compute.cloth_wx_matrix(vtx_points, joint_points)
    selected = MSelectionList()
    selected.add(sk.name())
    selected.add(get_shape(polygon).name()+".vtx[*]")
    depend_node = MObject()
    selected.getDependNode(0, depend_node)
    fn_skin = MFnSkinCluster(depend_node)
    path = MDagPath()
    components = MObject()
    weights = MDoubleArray()
    selected.getDagPath(1, path, components)
    vtx_length = len(vtx_points)
    joint_length = len(joints)
    fn_skin.getWeights(path, components, indices, weights)
    weights = [weights[i] for i in range(weights.length())]
    max_weights = compute.get_max_weights(weights, joint_length, vtx_length)
    return dict(
        wx_matrix=wx_matrix,
        max_weights=max_weights,
        fn_skin=fn_skin,
        path=path,
        components=components,
        indices=indices,
    )


def cloth_solve(wx_matrix, max_weights, fn_skin, path, components, indices,  xs, ys, r):
    ys = [1 - y for y in ys]
    r = pm.softSelect(q=1, ssd=1) * r
    weights = compute.cloth_weights(wx_matrix, max_weights, xs, ys, r)
    api_weights = MDoubleArray()
    api_weights.setLength(len(weights))
    for i, w in enumerate(weights):
        api_weights[i] = weights[i]
    fn_skin.setWeights(path, components, indices, api_weights)
    update_paint()


def paint_cloth(xs=(0, 0.33, 0.67, 1), ys=(0, 0, 1, 1), r=1):
    u"""
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    绘制布料权重
    """
    cloth_solve(xs=xs, ys=ys, r=r, **cloth_kwargs())


def null_kwargs():
    return {}


def paint_eye(**kwargs):
    u"""
    绘制眼睛权重
    """
    polygon = assert_geometry(shape_type="mesh")
    sk = get_skin_cluster(polygon)

    # indices
    influences = sk.getInfluence()
    joints = [joint for joint in influences if not joint.liw.get()]
    indices = MIntArray()
    indices.setLength(len(joints))
    for i, joint in enumerate(joints):
        indices[i] = influences.index(joint)

    # joint_vtx_ids = {joint_id : set([vtx_id])} 骨骼对应可以拥有权重的点
    mesh = get_shape(polygon)
    joint_vtx_ids = {}
    for i, joint in enumerate(joints):
        point = joint.getTranslation(space="world")
        _, face_id = mesh.getClosestPoint(point, space="world")
        face = mesh.f[face_id]
        length_map = {(mesh.vtx[vId].getPosition(space="world") - point).length(): mesh.vtx[vId] for vId in
                      face.getVertices()}
        joint_vtx_ids[indices[i]] = set([length_map[min(length_map.keys())].index()])
    pm.select([mesh.vtx[i] for ids in joint_vtx_ids.values() for i in ids])

    # max weights 可拆分的最大权重
    selected = MSelectionList()
    selected.add(sk.name())
    selected.add(get_shape(polygon).name()+".vtx[*]")
    depend_node = MObject()
    selected.getDependNode(0, depend_node)
    fn_skin = MFnSkinCluster(depend_node)
    path = MDagPath()
    components = MObject()
    weights = MDoubleArray()
    selected.getDagPath(1, path, components)
    vtx_length = mesh.vtx.count()
    joint_length = len(joints)
    fn_skin.getWeights(path, components, indices, weights)
    weights = [weights[i] for i in range(weights.length())]
    max_weights = compute.get_max_weights(weights, joint_length, vtx_length)

    # weight_ids 拥有权重的点
    weight_ids = [i for i, w in enumerate(max_weights) if w > 0.0001]
    pm.select([mesh.vtx[i] for i in weight_ids])
    selected = MSelectionList()
    MGlobal.getActiveSelectionList(selected)
    selected.getDagPath(0, path, components)

    # vv = {vtx_id: set(vtx_id)} 模型点的邻接点的点序
    pattern = re.compile("[0-9]+")
    ve = {i: set(int(s) for s in pattern.findall(line)[1:]) for i, line in enumerate(pm.polyInfo(mesh, ve=1))}
    ev = {i: set(int(s) for s in pattern.findall(line)[1:]) for i, line in enumerate(pm.polyInfo(mesh, ev=1))}
    vv = {v: set(v for e in es for v in ev[e]) for v, es in ve.items()}

    # joint_vtx_ids = {joint_id : set([vtx_id])} 骨骼对应可以拥有权重的点
    ids = set(weight_ids) - set(vtx_id for vtx_ids in joint_vtx_ids.values() for vtx_id in vtx_ids)
    while ids:
        for joint_id, vtx_ids in joint_vtx_ids.items():
            joint_vtx_ids[joint_id].update(set(i for vtx_id in vtx_ids for i in vv.get(vtx_id, set())) & ids)
            ids -= joint_vtx_ids[joint_id]
    pm.select([mesh.vtx[i] for i in joint_vtx_ids.values()[0]])

    weights = MDoubleArray()
    weights.setLength(joint_length*len(weight_ids))
    for i in range(joint_length*len(weight_ids)):
        weights[i] = 0
    py_indices = [indices[i] for i in range(joint_length)]
    for joint_id, vtx_ids in joint_vtx_ids.items():
        for vtx_id in vtx_ids:
            vtx_index = weight_ids.index(vtx_id)
            k = vtx_index*joint_length + py_indices.index(joint_id)
            weights[k] = max_weights[vtx_id]
    fn_skin.setWeights(path, components, indices, weights)
    update_paint()
    pm.select(polygon)
