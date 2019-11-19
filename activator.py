PNN_REL_THRESHOLD = 0.10
PNN_ABS_THRESHOLD = 0.27

def rel_point_5(pnns):
    """ しきい値: 相対, 参照ポイント: 5つ前 """
    return (pnns[0]-pnns[5]) < -PNN_REL_THRESHOLD

def abs_point_0(pnns):
    """ しきい値: 絶対, 参照ポイント: 最新 """
    return pnns[0] < PNN_ABS_THRESHOLD

def rel_cont_3(pnns):
    """ しきい値: 相対, 参照ポイント: 直前3つ """
    return all([(pnns[i]-pnns[3]) < -PNN_REL_THRESHOLD for i in range(3)])

def abs_cont_3(pnns):
    """ しきい値: 絶対, 参照ポイント: 直前3つ """
    return all([pnns[i] < PNN_ABS_THRESHOLD for i in range(3)])

activators = {
    "0": rel_point_5,
    "1": abs_point_0,
    "2": rel_cont_3,
    "3": abs_cont_3
}
