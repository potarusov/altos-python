import config
from Environment.map.map import Map
from Train.software.decision_making.planning.mission.dijkstra import DijkstraPlanner

class DecisionMaking:
    def __init__(self, ps):
        self.map = Map(config.map)
        self.mission_planner = DijkstraPlanner(self.map.adjacency_list)
        self.path = []

        self.modes = ["MANUAL", "DRIVERLESS"]
        self.mode = "MANUAL"

        self.states = ["READY", "MOVING FORWARD", "MOVING BACKWARD", "ARRIVING AT STOP", "AT STOP", "OBSTACLE AHEAD", "STOPPED",
                       "SHUT DOWN"]
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
        return False

    def has_arrived_2_destination(self, position):
        if position == self.path[0]:
            self.path.pop()
            return True
        return False

    def update_path(self, position):
        if position == self.path[-1]:
            self.path.pop()

    def is_obstacle_ahead(self, distance_2_obstacle):
        if distance_2_obstacle > 0.0 and distance_2_obstacle < config.min_safe_distance_2_obstacle:
            return True
        return False

    def run(self, position, distance_2_obstacle, btrc_command, keyboard_input):
        self.decision = "NO"
        if self.state == "MOVING_FORWARD" and self.is_obstacle_ahead(distance_2_obstacle):
            self.state = "OBSTACLE AHEAD"
            self.decision = "TO STOP"
        elif self.state == "OBSTACLE AHEAD" and not self.is_obstacle_ahead(distance_2_obstacle):
            self.state = "MOVING FORWARD"
            self.decision = "TO MOVE FORWARD"

        if btrc_command == 'accelerate':
            self.decision = "ACCELERATE"
        elif btrc_command == 'decelerate':
            self.decision = "DECELERATE"
        elif btrc_command == "direction":
            if self.mode == "MANUAL":
                self.mode = "DRIVERLESS"
            else:
                self.mode = "MANUAL"
        elif btrc_command == 'stop':
            self.state = "STOPPED"
            self.decision = "TO STOP"
        elif btrc_command == 'shutdown':
            self.state = "SHUT DOWN"
            self.decision = "TO SHUT DOWN"
            config.exit = 1

        if self.mode == "DRIVERLESS" and self.path:
            if self.is_on_path(position) and self.state == "MOVING":
                self.decision = "TO STOP"

            if self.has_arrived_2_destination(position) and self.state == "MOVING":
                self.decision = "TO STOP"

            self.update_path(position)

        return self.decision
