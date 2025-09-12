import g
import math


def calcDeltaPressure(sensorV):
    g.delta_pressure = (sensorV-g.sensor_idle_value) * \
        g.sensor_to_pressure_factor

    return g.delta_pressure


def calcDiameterFromSteps():
    """Calculate diameter based on motor steps from fully open position"""
    # Start from max diameter and subtract based on steps taken
    # Steps are counted from the fully open position (after auto-calibration)
    current_diameter = g.max_diameter_mm - \
        (g.gripper_steps * g.step_dia_mm_factor)

    # Ensure diameter doesn't go below 0
    current_diameter = max(0, current_diameter)

    return current_diameter


def calcDiameterFromRunTime():
    """Legacy function - kept for compatibility but now calls step-based calculation"""
    return calcDiameterFromSteps()


def calcDeformationMM():
    return g.aftertouch_runtime * 0.486
