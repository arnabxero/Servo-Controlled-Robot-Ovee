import g
import math


def calcDeltaPressure(sensorV):
    g.delta_pressure = (sensorV-g.sensor_idle_value) * \
        g.sensor_to_pressure_factor

    return g.delta_pressure


def calcDiameterFromRunTime():
    return (59 - g.gripper_closing_time * 0.486)


def calcDeformationMM():
    return g.aftertouch_runtime * 0.486
