# Initialize your global variables
exit_flag = False
test_var = "Hello World"
test_var2 = test_var

# Run Servo Flag
run_flag = False

# System Run Flag
runSystem_flag = False

# Sensor Touch Flag
touched_flag = False

# Sample Rate Globals
sample_rate = 10

# Board setup globals
board = None

# Servo Globals
gripper_pin = 13
gripper_speed = 100
gripper_precision = 0.001
gripper_direction = 0
gripper_angle_min = 20
gripper_angle_max = 70

# Sensor Globals
# Analog 2 pin is sensor pin in boardsetup.py
sensor_value = 0.0
sensor = None
sensor_min = 0.67
sensor_max = 5.0
sensor_to_pressure_factor = (6.895/0.8)
sensor_touch_value = 0.05

# Sensor Touch Globals
touched_angle = 0.0
time_of_touch = 0.0


# Value Export Array Globals
export_timestamp = []
export_diameter = []
export_delta_pressure = []
export_deformation = []
export_sensor_value = []
export_closing_time = []

# Calculation Globals
# EStar = 0.0
gripper_degree = 0.0
delta_pressure = 0.0
deformation_in_mm = 0.0
diameter = 0.0
# deformation_to_mm = ((0.0179*deformation*deformation) +
#                      (0.241*deformation))*1.3
deformation_degree = 3.0

# Table Globals
# Not using anywhere
get_table_params_flag = False
table_index = 1
table_diameter = 0
table_estar = 0
table_deformation_mm = 0
table_delta_pressure = 0

# global components
consoleBox = None

# FileName Index
fileNumber = 0

# TK Entry to show data
gripper_closing_time_entry = None
diameter_entry = None
delta_pressure_entry = None
sensor_reading_entry = None
gripper_angle_entry = None

# Stepper Motor Variables
# CLK+ jabe pin 6 e, CW+ jabe pin 7 e
pin_step_direction = 7
pin_step_active = 6

# speed = 1
run_time = 2.5
direction = 1
motor_active = False
active_run_time = 0

# Stop Switch digital pin 5 in boardsetup
stop_switch = False
stop_switch_pin = None

# Motor Active Time Variables
gripper_closing_time = 0.0
gripper_starting_time = 0
gripper_start_time_flag = False

# Test Mode Variables
step_count = 0
