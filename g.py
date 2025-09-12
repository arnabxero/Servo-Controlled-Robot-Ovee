# All Global Variables
######################
# Arduino Board Variables
board = None
# Analog Pin 2 is sensor pin
# Digital Pin 5 is stop switch pin

# Sensor Variables
sensor = None
sensor_value = 0.0
sensor_idle_value = 0.67
sensor_touch_value = 0.05
sensor_touch_flag = False
sensor_to_pressure_factor = (6.895/0.8)

# Time calculation variables
time_of_touch = 0.0

# Sampling and delays
sample_rate = 10

# Export File number tracking
fileNumber = 0

# Grasper Variables
gripper_pin = 13
gripper_speed = 100
gripper_direction = 0
gripper_active = False
aftertouch_runtime = 0.0
gripper_steps = 0

# Gripper Run Time Variables
gripper_closing_time = 0.0
gripper_starting_time = 0.0
gripper_start_time_flag = False

# Gripper Stop Switch
stop_switch_pin = None

# Gripper Control Pins
pin_step_direction = 7
pin_step_active = 6

# Exporting Variables
export_timestamp = []
export_diameter = []
export_delta_pressure = []
export_deformation = []
export_sensor_value = []
export_closing_time = []

# Calculation Variables
diameter_in_mm = 0.0
delta_pressure = 0.0
deformation_in_mm = 0.0

# Export File Index
fileNumber = 0

# Input Entry Variables

# Display Entry Variables
diameter_mm_entry = None
deformation_mm_entry = None
live_sensor_value_entry = None
delta_pressure_entry = None
gripper_closing_time_entry = None
