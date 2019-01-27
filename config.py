
""" Train """
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

""" Controller Area Network """

initial_position = [0, 0]
exit = 0

""" Environment """
map = "map.json"