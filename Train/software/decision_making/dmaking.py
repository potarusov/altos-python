import time
import config
from Environment.map.map import Map
from Train.hardware.can import WiFiTrainStateCANFrame
from Train.software.decision_making.planning.mission.dijkstra import DijkstraPlanner

class DecisionMaking:
    def __init__(self, can):
        self.most_recent_position = config.initial_position
        self.can = can

        self.map = Map(config.map)
        self.mission_planner = DijkstraPlanner(self.map.adjacency_list)
        self.path = []

        self.modes = ["UNKNOWN", "MANUAL", "DRIVERLESS"]
        self.mode = "MANUAL"

        self.states = ["UNKNOWN", "READY", "MOVING FORWARD", "MOVING BACKWARD", "ARRIVING AT STOP", "AT STOP",
                       "OBSTACLE AHEAD", "STOPPED", "SHUT DOWN"]
        self.state = "READY"

        self.decisions = ["NO", "TO ACCELERATE", "TO DECELERATE", "TO MOVE FORWARD", "TO MOVE BACKWARD", "TO CHANGE DIRECTION",
                          "TO STOP", "TO SHUT DOWN"]
        self.decision = "NO"

    def plan(self, origin, destination):
        self.mission_planner.plan(origin)
        self.path = self.mission_planner.find_path(destination, origin)

    def is_on_path(self, position):
        for node in self.path:
            if position == node:
                return True
        print("Train out of path!!!")
        print(position)
        return False

    def has_arrived_2_destination(self, position):
        if position == self.path[0]:
            return True
        return False

    def update_path(self, position):
        if position == self.path[-1]:
            self.path.pop()
            print("Path: ")
            print(self.path)

    def is_obstacle_ahead(self, distance_2_obstacle):
        if distance_2_obstacle > 0.0 and distance_2_obstacle < config.min_safe_distance_2_obstacle:
            return True
        return False

    def run(self, position, distance_2_obstacle, btrc_command, message_from_cc):
        self.message_from_cc = message_from_cc
        # print(self.message_from_cc)
        self.decision = "NO"
        if self.mode == "MANUAL":
            if self.state == "MOVING FORWARD" and self.is_obstacle_ahead(distance_2_obstacle):
                self.state = "OBSTACLE AHEAD"
                self.decision = "TO STOP"
            elif self.state == "OBSTACLE AHEAD" and not self.is_obstacle_ahead(distance_2_obstacle):
                self.state = "MOVING FORWARD"
                self.decision = "TO MOVE FORWARD"

            if btrc_command == 'accelerate':
                self.state = "MOVING FORWARD"
                self.decision = "ACCELERATE"
            elif btrc_command == 'decelerate':
                self.decision = "DECELERATE"
            elif btrc_command == "direction":
                print("In DRIVERLESS mode now!!")
                self.mode = "DRIVERLESS"
                self.state = "READY"
                self.decision = "TO STOP"
            elif btrc_command == 'stop':
                self.state = "STOPPED"
                self.decision = "TO STOP"
            elif btrc_command == 'shutdown':
                self.state = "SHUT DOWN"
                self.decision = "TO SHUT DOWN"
                config.exit = 1

        elif self.mode == "DRIVERLESS":
            destination = 0
            if btrc_command == 'accelerate':
                destination = 11
                print("Going to 11")
                self.state = "READY"
            elif btrc_command == 'decelerate':
                destination = 3
                print("Going to 3")
                self.state = "READY"
            elif btrc_command == "direction" and not self.path:
                self.mode = "MANUAL"
                print("In MANUAL mode now!!!")
                self.state = "READY"
            elif btrc_command == 'stop':
                self.state = "READY"
                destination = 9
                print("Going to 9")
            elif btrc_command == 'shutdown':
                self.state = "SHUT DOWN"
                self.decision = "TO SHUT DOWN"
                config.exit = 1

            if self.state == "READY" and destination:
                self.plan(position, destination)
                self.most_recent_position = position
                print("I have a plan!!!")
                time.sleep(config.time_2_switch)
                destination = 0
                self.state = "MOVING FORWARD"
                self.decision = "TO MOVE FORWARD"
            elif self.state == "MOVING FORWARD":
                if self.most_recent_position != position:
                    if not self.is_on_path(position):
                        self.state = "STOPPED"
                        self.decision = "TO STOP"
                    self.most_recent_position = position
                if self.has_arrived_2_destination(self.most_recent_position):
                    self.state = "READY"
                    self.decision = "TO STOP"
                self.update_path(self.most_recent_position)

        timestamp = time.time()
        self.can.update_wfts_buffer(self.most_recent_position, self.mode, self.state, self.decision, timestamp)

        return self.decision
