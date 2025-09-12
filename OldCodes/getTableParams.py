# Not using anywhere
import g
from calculations import calcDiameter, calcDeltaPressure, calcEstar
from updateConsole import updateConsole


def getTableParams():
    g.table_diameter = calcDiameter(g.gripper_degree)
    g.table_deformation_mm = g.deformation_in_mm
    g.table_delta_pressure = g.delta_pressure

    updateConsole("Table: " + str(g.table_index))
    updateConsole("Diameter: " + str(g.table_diameter))
    updateConsole("Deformation: " + str(g.table_deformation_mm))
    updateConsole("Pressure: " + str(g.table_delta_pressure))
