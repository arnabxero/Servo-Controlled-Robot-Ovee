import g
from updateConsole import updateConsole
import csv


def resetParams():
    # Need to implement more reset params
    g.touched_flag = False
    g.gripper_closing_time = False
    g.time_of_touch = 0.0
    updateConsole("Parameters Reset Successfully")


def pauseClaw():
    g.gripper_direction = 0
    g.motor_active = False
    updateConsole("Claw in pause, although time is counting")


def handleGripperButton(direction, motorStat):
    if (direction == 2):
        g.touched_flag = False
        g.gripper_closing_time = 0.0
        g.gripper_starting_time = 0
        g.gripper_start_time_flag = False

    g.gripper_direction = direction
    g.motor_active = motorStat


def updateSysFlag(flag):

    if (flag == '1'):
        g.runSystem_flag = True
        print("System is running")
        updateConsole("System is running...")
    else:
        g.runSystem_flag = False
        print("System is paused!")
        updateConsole("System is paused!")

    print("runSystem_flag: ", g.runSystem_flag)


# def append_to_csv(file_path, column1_data, column2_data, column3_data, column4_data, column5_data):

#     # with open(file_path, 'a', newline='') as file:
#     with open('Data_'+str(g.fileNumber)+'.csv', 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([column1_data, column2_data,
#                         column3_data, column4_data, column5_data])


def append_to_csv(first_row, file_path, column1_data, column2_data, column3_data, column4_data, column5_data, column6_data):
    with open('Data_'+str(g.fileNumber)+'.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if first_row:
            writer.writerow(
                ['Time', 'Dia (mm)', 'd (mm)', 'Delta P (KPa)', 'Sensor Voltage', 'Closing Time (Sec)'])

        writer.writerow([str(column1_data), str(column2_data), str(
            column3_data), str(column4_data), str(column5_data), str(column6_data)])


def export_data(array1, array2, array3, array4, array5, array6, file_name):

    for i in range(len(array1)):
        element1 = array1[i]
        element2 = array2[i]
        element3 = array3[i]
        element4 = array4[i]
        element5 = array5[i]
        element6 = array6[i]

        first_row = False

        if i == 0:
            first_row = True
        else:
            first_row = False

        print(element1, element2, element3, element4, element5, element6)

        append_to_csv(first_row, file_name, element1, element2,
                      element3, element4, element5, element6)

    g.fileNumber = g.fileNumber + 1
