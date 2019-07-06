import config

class BaseState(object):
    def is_obstacle_ahead(self, distance_2_obstacle):
        if distance_2_obstacle > 0.0 and distance_2_obstacle < config.min_safe_distance_2_obstacle:
            return True
        return False

    def enter(self):
        raise NotImplementedError()

    def execute(self, distance_2_obstacle, btrc_command):
        raise NotImplementedError()

    def exit(self):
        raise NotImplementedError()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MovingForward(BaseState):
    __metaclass__ = Singleton
    def __init__(self, fsm):
        self.fsm = fsm
        self.decision = "TO MOVE FORWARD"

    def enter(self):
        print("Entering MovingForward state")
        return self.decision

    def execute(self, distance_2_obstacle, btrc_command):
        self.decision = "NO"
        if self.is_obstacle_ahead(distance_2_obstacle):
            self.fsm.change_state(ObstacleAhead(self.fsm))

        if btrc_command == 'accelerate':
            self.decision = "TO ACCELERATE"
        elif btrc_command == 'decelerate':
            self.decision = "TO DECELERATE"
        elif btrc_command == 'stop':
            self.decision = 'TO STOP'
            self.fsm.change_state(Stopped(self.fsm))
        elif btrc_command == 'shutdown':
            self.decision = "TO SHUT DOWN"
            self.fsm.change_state(ShutDown(self.fsm))
            config.exit = 1

        return self.decision

    def exit(self):
        print("Leaving MovingForward state")

class MovingBackward(BaseState):
    __metaclass__ = Singleton
    def __init__(self, fsm):
        self.fsm = fsm
        self.decision = "TO MOVE BACKWARD"

    def enter(self):
        print("Entering MovingBackward state")
        return self.decision

    def execute(self, distance_2_obstacle, btrc_command):
        self.decision = "NO"
        if self.is_obstacle_ahead(distance_2_obstacle):
            self.fsm.change_state(ObstacleAhead(self.fsm))

        if btrc_command == 'accelerate':
            self.decision = "TO ACCELERATE"
        elif btrc_command == 'decelerate':
            self.decision = "TO DECELERATE"
        elif btrc_command == 'stop':
            self.decision = "TO STOP"
            self.fsm.change_state(Stopped(self.fsm))
        elif btrc_command == 'shutdown':
            self.decision = "TO SHUT DOWN"
            self.fsm.change_state(ShutDown(self.fsm))
            config.exit = 1

        return self.decision

    def exit(self):
        print("Leaving MovingBackward state")

class ObstacleAhead(BaseState):
    __metaclass__ = Singleton
    def __init__(self, fsm):
        self.fsm = fsm
        self.decision = "TO STOP"

    def enter(self):
        print("Entering ObstacleAhead state")
        return self.decision

    def execute(self, distance_2_obstacle, btrc_command):
        if not self.is_obstacle_ahead(distance_2_obstacle):
            #prev_state = self.fsm.prev_state
            print(type(self.fsm.prev_state))
            self.fsm.change_state(self.fsm.prev_state)

        if btrc_command == 'shutdown':
            self.decision = "TO SHUT DOWN"
            self.fsm.change_state(ShutDown(self.fsm))

        return self.decision

    def exit(self):
        print("Leaving ObstacleAhead state")

class Stopped(BaseState):
    __metaclass__ = Singleton
    def __init__(self, fsm):
        self.fsm = fsm
        self.decision = "TO STOP"

    def enter(self):
        print("Entering Stopped state")
        return self.decision

    def execute(self, distance_2_obstacle, btrc_command):
        self.decision = "NO"
        if btrc_command == 'accelerate':
            self.decision = "TO ACCELERATE"
            self.fsm.change_state(MovingForward(self.fsm))
        elif btrc_command == 'decelerate':
            self.decision = "DECELERATE"
            self.fsm.change_state(MovingForward(self.fsm))
        elif btrc_command == 'shutdown':
            self.decision = "TO SHUT DOWN"
            self.fsm.change_state(ShutDown(self.fsm))

        return self.decision

    def exit(self):
        print("Leaving Stopped state")

class ShutDown(BaseState):
    __metaclass__ = Singleton
    def __init__(self, fsm):
        self.fsm = fsm

    def enter(self):
        print("Entering ShutDown state")
        self.decision = "TO SHUT DOWN"

        return self.decision

    def execute(self, distance_2_obstacle, btrc_command):
        config.exit = 1

        return "NO"

    def exit(self):
        pass

class MFSM:
    def __init__(self):
        self.prev_state = None
        self.cur_state = None
        self.global_state = None
        self.decision = None

    def set_prev_state(self, state):
        self.prev_state = state

    def set_cur_state(self, state):
        self.cur_state = state

    def set_global_state(self, state):
        self.global_state = state

    def update(self, distance_2_obstacle, btrc_command):
        if self.cur_state:
            self.decision = self.cur_state.execute(distance_2_obstacle, btrc_command)

        return self.decision

    def change_state(self, new_state):
        self.prev_state = self.cur_state
        self.cur_state.exit()
        self.cur_state = new_state
        self.cur_state.enter()