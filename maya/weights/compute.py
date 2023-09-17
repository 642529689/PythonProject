# coding:utf-8


def bezier_v(p, t):
    u"""
    :param p: [float, float, float, float] 贝塞尔曲线x/y轴控制点
    :param t: 曲线上位置t/param
    :return: x/y轴数值
    """
    return p[0]*(1-t)**3.0 + 3*p[1]*t*(1-t)**2 + 3*p[2]*t**2*(1-t) + p[3]*t**3


def bezier_t(p, v):
    u"""
    :param p: [float, float, float, float] 贝塞尔曲线x/y轴控制点
    :param v: x/y轴数值
    :return: 曲线上位置t/param
    """
    min_t = 0.0
    max_t = 1.0
    while True:
        t = (min_t+max_t)/2.0
        error_range = bezier_v(p, t) - v
        if error_range > 0.0001:
            max_t = t
        elif error_range < -0.0001:
            min_t = t
        else:
            return t


def get_weight(x, xs, ys):
    u"""
    :param x: x轴坐标
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :return: weight/y轴坐标
    """
    if x <= 0.0:
        return ys[0]
    elif x >= 1.0:
        return ys[3]
    t = bezier_t(xs, x)
    return bezier_v(ys, t)


def ik_x(v, p):
    u"""
    :param v: 向量
    :param p: 点坐标
    :return: 点p在向量v轴上的坐标值。或理解为点p到向量v所在直线的最近点与远点的距离
    """
    return sum(v[i] * p[i] for i in range(3)) / sum(v[i] ** 2 for i in range(3))


def ik_xs(v, p, ps):
    u"""
    :param v: 关节x轴向量
    :param p: 关节点坐标
    :param ps: 模型点坐标
    :return: 模型点在关节x轴上的坐标值列表
    """
    x = ik_x(v, p)
    return [ik_x(v, p) - x for p in ps]


def ik_weights(wxs, xs, ys, r):
    u"""
    :param wxs: 模型点在关节x轴上的坐标值列表
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    :return: 关节权重
    """
    return [get_weight(x / r + 0.5, xs, ys) for x in wxs]


def soft_weights(wxs, xs, ys, r):
    u"""
    :param wxs: 模型点到所选点的距离
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    :return: 软选权重
    """
    return [get_weight(x/r, xs, ys) for x in wxs]


def get_max_weights(weights, joint_length, vtx_length):
    u"""
    :param weights: 权重
    :param joint_length: 骨骼长度
    :param vtx_length: 点长度
    :return: 每点最大权重值
    """
    return [sum([weights[joint_length*j+i] for i in range(joint_length)]) for j in range(vtx_length)]


def split_wx_matrix(vps, ps):
    u"""
    :param vps: [(v, p), (v, p)]点全追踪列表
    :param ps: 模型点坐标
    :return: 模型点在关节x轴上的坐标值矩阵
    """
    return [ik_xs(v, p, ps) for v, p in vps]


def split_weights(wx_matrix, max_weights, xs, ys, r):
    u"""
    :param wx_matrix: 模型点在关节x轴上的坐标值矩阵
    :param max_weights: 每点最大权重值
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    :return: 拆分权重
    """
    weight_matrix = [[1 for _ in wx_matrix[0]]]
    for wxs in wx_matrix:
        weights = ik_weights(wxs, xs, ys, r)
        weights = [min(w1, w2) for w1, w2 in zip(weight_matrix[-1], weights)]
        weight_matrix.append(weights)
        weight_matrix[-2] = [w2 - w1 for w1, w2 in zip(weight_matrix[-1], weight_matrix[-2])]
    weight_matrix = [[w*m for w, m in zip(ws, max_weights)]for ws in weight_matrix]
    weights = sum([list(ws) for ws in zip(*weight_matrix)], [])
    return weights


def distance(p1, p2):
    u"""
    :param p1: 点坐标
    :param p2: 点坐标
    :return: 模型点到选择点之间的距离
    """
    return sum([(p1[i]-p2[i])**2 for i in range(3)])**0.5


def cloth_wx_matrix(vtx_points, joint_points):
    u"""
    :param vtx_points: 模型点坐标列表
    :param joint_points: 骨骼点坐标列表
    :return: 模型点到骨骼点之间的距离矩阵
    """
    return [[distance(vtx_point, joint_point) for vtx_point in vtx_points] for joint_point in joint_points]


def cloth_weights(wx_matrix, max_weights, xs, ys, r):
    u"""
    :param wx_matrix: 模型点到骨骼点之间的距离矩阵
    :param max_weights: 每点最大权重值
    :param xs: [float, float, float, float] 贝塞尔曲线x轴控制点
    :param ys: [float, float, float, float] 贝塞尔曲线y轴控制点
    :param r: 过度半径
    :return: 拆分权重
    :return: 布料权重
    """
    vtx_len = len(wx_matrix[0])
    joint_len = len(wx_matrix)
    weights = [get_weight(wx_matrix[joint_id][vtx_id]/r, xs, ys)
               for vtx_id in range(vtx_len)
               for joint_id in range(joint_len)]
    for vtx_id in range(vtx_len):
        vtx_weight = sum([weights[vtx_id*joint_len+joint_id] for joint_id in range(joint_len)])
        vtx_weight = max(vtx_weight, 0.000000001)
        for joint_id in range(joint_len):
            k = vtx_id*joint_len+joint_id
            weights[k] = weights[k] / vtx_weight * max_weights[vtx_id]
    return weights
