import g
import math


def calcDeformationMM():
    return g.run_time * 0.486


def calcEstar(del_p, rad, defrm):

    # E* = 2.355*DP*(R/d)^0.5

    if (g.touched_flag == True):
        try:
            temp1 = math.sqrt(rad/defrm)

            g.EStar = 2.355*del_p*temp1
        except:
            g.EStar = 0.00
    else:
        g.EStar = 0.00

    return g.EStar


def calcDiameter(angle):
    return (54 - (0.52*angle-g.gripper_angle_min) - (0.012 * ((angle-g.gripper_angle_min)*(angle-g.gripper_angle_min))))
    # # radius = ((gripper_angle_max-angle) * degree_to_mm_factor)/2

    # # radius = (angle - deformation - gripper_angle_min)**2 * 0.0149 + \
    # # 0.0323 * (angle - deformation - gripper_angle_min)

    # x = (angle - g.deformation_mm - g.gripper_angle_min)

    # a = (x**2)*0.0179
    # b = x*0.241

    # g.diameter = (54.345 - a - b)*1.3

    # return g.diameter


def calcDiameterFromRunTime():
    return (59 - g.gripper_closing_time * 0.486)


def calcDeltaPressure(sensorV):
    g.delta_pressure = (sensorV-g.sensor_min) * g.sensor_to_pressure_factor

    return g.delta_pressure
