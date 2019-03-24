exit = 0

""" Environment """
map = "Environment//map//network.yaml"

""" Train """
delay = 0.001
""" Motor """
pin_A = "P9_16"
pin_B = "P9_14"
min_velocity = 75.0
max_velocity = 100.0
velocity_step = 5

""" Sensors """
# Bluetooth
service_uuid = "00001101-0000-1000-8000-00805F9B34FB"
android_application_name = "PerkyBlue"

# Ultrasonic
pin_trigger = "P9_15"
pin_echo = "P9_12"
log_distance = False

""" Kalman Filter """
k_stab = 0.03

""" Decision Making """
initial_position = 0
min_safe_distance_2_obstacle = 15
time_2_switch = 10

""" Acting """
step = 5