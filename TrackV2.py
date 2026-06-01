
# -*- coding: UTF-8 -*-
# @author: aj
# @file: track
# @time: 2025-03-19
# @desc:
import json
from typing import List, Dict
import random
import numpy as np
import math
import time

class bezierTrajectory:
    def _bztsg(self, dataTrajectory):
        lengthOfdata = len(dataTrajectory)

        def staer(x):
            t = ((x - dataTrajectory[0][0]) / (dataTrajectory[-1][0] - dataTrajectory[0][0]))
            y = np.array([0, 0], dtype=np.float64)
            for s in range(len(dataTrajectory)):
                y += dataTrajectory[s] * ((math.factorial(lengthOfdata - 1) / (
                        math.factorial(s) * math.factorial(lengthOfdata - 1 - s))) * math.pow(t, s) * math.pow(
                    (1 - t), lengthOfdata - 1 - s))
            return y[1]

        return staer

    def _type(self, type, x, numberList):
        numberListre = []
        pin = (x[1] - x[0]) / numberList
        if type == 0:
            for i in range(numberList):
                numberListre.append(i * pin)
            if pin >= 0:
                numberListre = numberListre[::-1]
        elif type == 1:
            for i in range(numberList):
                numberListre.append(1 * ((i * pin) ** 2))
            numberListre = numberListre[::-1]
        elif type == 2:
            for i in range(numberList):
                numberListre.append(1 * ((i * pin - x[1]) ** 2))

        elif type == 3:
            dataTrajectory = [np.array([0, 0]), np.array([(x[1] - x[0]) * 0.8, (x[1] - x[0]) * 0.6]),
                              np.array([x[1] - x[0], 0])]
            fun = self._bztsg(dataTrajectory)
            numberListre = [0]
            for i in range(1, numberList):
                numberListre.append(fun(i * pin) + numberListre[-1])
            if pin >= 0:
                numberListre = numberListre[::-1]
        numberListre = np.abs(np.array(numberListre) - max(numberListre))
        biaoNumberList = ((numberListre - numberListre[numberListre.argmin()]) / (
                numberListre[numberListre.argmax()] - numberListre[numberListre.argmin()])) * (x[1] - x[0]) + x[0]
        biaoNumberList[0] = x[0]
        biaoNumberList[-1] = x[1]
        return biaoNumberList

    def getFun(self, s):
        '''
        :param s: 传入P点
        :return: 返回公式
        '''
        dataTrajectory = []
        for i in s:
            dataTrajectory.append(np.array(i))
        return self._bztsg(dataTrajectory)

    def simulation(self, start, end, le=1, deviation=0, bias=0.5):
        '''
        :param start:开始点的坐标 如 start = [0, 0]
        :param end:结束点的坐标 如 end = [100, 100]
        :param le:几阶贝塞尔曲线，越大越复杂 如 le = 4
        :param deviation:轨迹上下波动的范围 如 deviation = 10
        :param bias:波动范围的分布位置 如 bias = 0.5
        :return:返回一个字典equation对应该曲线的方程，P对应贝塞尔曲线的影响点
        '''
        start = np.array(start)
        end = np.array(end)
        cbb = []
        if le != 1:
            e = (1 - bias) / (le - 1)
            cbb = [[bias + e * i, bias + e * (i + 1)] for i in range(le - 1)]

        dataTrajectoryList = [start]

        t = random.choice([-1, 1])
        w = 0
        for i in cbb:
            px1 = start[0] + (end[0] - start[0]) * (random.random() * (i[1] - i[0]) + (i[0]))
            p = np.array([px1, self._bztsg([start, end])(px1) + t * deviation])
            dataTrajectoryList.append(p)
            w += 1
            if w >= 2:
                w = 0
                t = -1 * t

        dataTrajectoryList.append(end)
        return {"equation": self._bztsg(dataTrajectoryList), "P": np.array(dataTrajectoryList)}

    def trackArray(self, start, end, numberList, le=1, deviation=0, bias=0.5, type=0, cbb=0, yhh=10):
        '''
        :param start:开始点的坐标 如 start = [0, 0]
        :param end:结束点的坐标 如 end = [100, 100]
        :param numberList:返回的数组的轨迹点的数量 numberList = 150
        :param le:几阶贝塞尔曲线，越大越复杂 如 le = 4
        :param deviation:轨迹上下波动的范围 如 deviation = 10
        :param bias:波动范围的分布位置 如 bias = 0.5
        :param type:0表示均速滑动，1表示先慢后快，2表示先快后慢，3表示先慢中间快后慢 如 type = 1
        :param cbb:在终点来回摆动的次数
        :param yhh:在终点来回摆动的范围
        :return:返回一个字典trackArray对应轨迹数组，P对应贝塞尔曲线的影响点
        '''
        s = []
        fun = self.simulation(start, end, le, deviation, bias)
        w = fun['P']
        fun = fun["equation"]
        if cbb != 0:
            numberListOfcbb = round(numberList * 0.2 / (cbb + 1))
            numberList -= (numberListOfcbb * (cbb + 1))

            xTrackArray = self._type(type, [start[0], end[0]], numberList)
            for i in xTrackArray:
                s.append([i, fun(i)])
            dq = yhh / cbb
            kg = 0
            ends = np.copy(end)
            for i in range(cbb):
                if kg == 0:
                    d = np.array([end[0] + (yhh - dq * i),
                                  ((end[1] - start[1]) / (end[0] - start[0])) * (end[0] + (yhh - dq * i)) + (
                                          end[1] - ((end[1] - start[1]) / (end[0] - start[0])) * end[0])])
                    kg = 1
                else:
                    d = np.array([end[0] - (yhh - dq * i),
                                  ((end[1] - start[1]) / (end[0] - start[0])) * (end[0] - (yhh - dq * i)) + (
                                          end[1] - ((end[1] - start[1]) / (end[0] - start[0])) * end[0])])
                    kg = 0
                print(d)
                y = self.trackArray(ends, d, numberListOfcbb, le=2, deviation=0, bias=0.5, type=0, cbb=0, yhh=10)
                s += list(y['trackArray'])
                ends = d
            y = self.trackArray(ends, end, numberListOfcbb, le=2, deviation=0, bias=0.5, type=0, cbb=0, yhh=10)
            s += list(y['trackArray'])

        else:
            xTrackArray = self._type(type, [start[0], end[0]], numberList)
            for i in xTrackArray:
                s.append([i, fun(i)])
        return {"trackArray": np.array(s), "P": w}



def get_simple_pre_slider_fix_coordinates_trajectory(*, click_x, click_y):
    a = bezierTrajectory()
    nums = random.randint(30, 40)

    s_x = random.randint(600, 700)
    s_y = random.randint(100, 150)

    e_x = click_x
    e_y = click_y

    r = a.trackArray(
        start=[
            s_x,
            s_y
        ],
        end=[
            e_x,
            e_y
        ],
        numberList=nums,
        le=4,
        deviation=1,
        bias=1,
        type=3,
        cbb=0,
        yhh=5
    )
    g = []
    use_time = random.randint(3000, 3500)  # 开始是3秒或者3.5秒
    for i, l in enumerate(r['trackArray']):
        s = {}
        use_time += random.randint(8, 15)
        s["time"] = use_time
        s['x'] = int(l[0])
        s['y'] = int(l[1])
        s['isTrusted'] = 1
        g.append(s)

    return g, use_time


def get_simple_slider_fixed_coordinates_trajectory(*, click_x, click_y, end_x, end_y, has_spend_time) -> List[Dict]:
    a = bezierTrajectory()
    nums = random.randint(40, 60)
    s_x = click_x
    s_y = click_y

    e_x = end_x
    e_y = end_y

    r = a.trackArray(
        start=[
            s_x,
            s_y
        ],
        end=[
            e_x,
            e_y
        ],
        numberList=nums,
        le=4,
        deviation=1,
        bias=1,
        type=3,
        cbb=0,
        yhh=5
    )
    g = []
    use_time = has_spend_time
    for i, l in enumerate(r['trackArray']):
        s = {}
        use_time += random.randint(8, 15)
        s["time"] = use_time
        s['x'] = int(l[0])
        s['y'] = int(l[1])
        s['isTrusted'] = 1
        g.append(s)
    return g


def get_v2_trajectory(*, click_x, click_y, end_x, end_y):
    trajectory1, use_time = get_simple_pre_slider_fix_coordinates_trajectory(click_x=click_x, click_y=click_y)
    trajectory2 = get_simple_slider_fixed_coordinates_trajectory(click_x=click_x, click_y=click_y, end_x=end_x,
                                                                 end_y=end_y, has_spend_time=use_time)
    return use_time, trajectory2, trajectory1 + trajectory2

def slide_change(n):
    numerator = 0.6 * n * n + 13 * n
    denominator = 169
    return round(numerator / denominator)


def reverse_slide_change(R):
    """
    已知 slide_change(n) = R，求 n
    """
    # 方程为：0.6*n² + 13*n = R * 169
    # 即：0.6*n² + 13*n - 169*R = 0

    import math

    a = 0.6
    b = 13
    c = -169 * R

    # 计算判别式
    discriminant = b * b - 4 * a * c

    if discriminant < 0:
        # 无实数解
        return []
    elif discriminant == 0:
        # 一个解
        n = -b / (2 * a)
        return [n]
    else:
        # 两个解
        sqrt_disc = math.sqrt(discriminant)
        n1 = (-b + sqrt_disc) / (2 * a)
        n2 = (-b - sqrt_disc) / (2 * a)
        return [n1, n2]


# 更实用的版本：只返回正数解
def reverse_slide_change_positive(R):
    """
    已知 slide_change(n) = R，求正数 n 解
    """
    solutions = reverse_slide_change(R)

    # 过滤出正数解
    positive_solutions = [n for n in solutions if n >= 0]

    return round(positive_solutions[0])

def _create_track_list(click_x, click_y, xPos, start_time):
    slidePos = reverse_slide_change_positive(xPos)
    end_x, end_y = click_x+slidePos, click_y
    ya_mc_0_time, ya_mm, ya_mp = get_v2_trajectory(click_x=click_x, click_y=click_y, end_x=end_x, end_y=end_y)
    traj_mm = "|".join([f'{item["x"]},{item["y"]},{item["time"]},{item["isTrusted"]}' for item in ya_mm])
    traj_mp = "|".join([f'{item["x"]},{item["y"]},{item["time"]},{item["isTrusted"]}' for item in ya_mp])
    item_0 = ya_mm[0]
    item_1 = ya_mm[-1]
    traj = {
        "mc": f'{item_0["x"]},{item_0["y"]},{item_0["time"]}, ,{item_0["isTrusted"]}',
        "tc": "",
        "mu": f'{item_1["x"]},{item_1["y"]},{item_1["time"]}, ,{item_1["isTrusted"]}',
        "te": "",
        "mp": traj_mp,
        "tmv": "",
        "mm": traj_mm,
        "ks": "",
        "fi": "",
        "startTime": start_time,
        "si": "400,400,799,400,799,800,889,65.1890482246979,400"
    }
    traj_info = {
        "TrackList": traj,
        'TrackStartTime': start_time,
        'VerifyTime': start_time + ya_mp[-1]["time"] + random.randint(100, 200),
        "arg": "ZbzwUAsPUFIXLA==",
        "slidePos": str(slidePos),
        "xPos": str(xPos)
    }

    return json.dumps(traj_info, separators=(',', ':'))


if __name__ == '__main__':
    traj_info = _create_track_list(76, 482, 85, int(time.time()*1000))
    print(traj_info)