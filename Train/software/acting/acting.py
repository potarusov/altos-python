import config

class Acting:
    def __init__(self, motor):
        self.motor = motor
        self.velocity = config.min_velocity

    def move_forward(self, step):
        if self.velocity + step >= config.min_velocity and self.velocity + step <= config.max_velocity:
            self.velocity += step
            self.motor.forward(self.velocity)
        elif self.velocity + step < config.min_velocity:
            print("The minimum velocity has been reached")
        elif self.velocity + step > config.max_velocity:
            print(self.velocity)
            print("The maximum velocity has been reached")

        print("Velocity [%f]" % self.velocity)

    def move_backward(self, step):
        if self.velocity + step >= config.min_velocity and self.velocity + step <= config.max_velocity:
            self.velocity += step
            self.motor.backward(self.velocity)
        elif self.velocity + step < config.min_velocity:
            print("The minimum velocity has been reached")
        elif self.velocity + step > config.max_velocity:
            print(self.velocity)
            print("The maximum velocity has been reached")

        print("Velocity [%f]" % self.velocity)

    def stop(self):
        self.motor.stop()

    def shutdown(self):
        self.motor.stop()
        self.motor.cleanup()

    def run(self, decision):
        if decision == "TO ACCELERATE":
            print("Decision to accelerate")
            self.move_forward(config.step)
        elif decision == "TO DECELERATE":
            self.move_forward(-config.step)
        elif decision == "TO MOVE FORWARD":
            self.move_forward(0.0)
        elif decision == "TO MOVE BACKWARD":
            self.move_backward(0.0)
        elif decision == "TO STOP":
            self.stop()
        elif decision == "TO SHUT DOWN":
            self.shutdown()
