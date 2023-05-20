import machine
import utime

class Light:
    """
    Represents a light with an ability to turn on and off.
    """

    def __init__(self, pin):
        """
        Initialize a light with the given pin.
        """
        self.led = machine.Pin(pin, machine.Pin.OUT)
        print("Light initialized.")

    def on(self):
        """
        Turns the light on.
        """
        self.led.value(1)
        print("Light turned on.")

    def off(self):
        """
        Turns the light off.
        """
        self.led.value(0)
        print("Light turned off.")


class PedestrianButton:
    """
    Represents a pedestrian button.
    """

    def __init__(self, pin):
        """
        Initialize a pedestrian button with the given pin.
        """
        self.button = machine.Pin(pin, machine.Pin.IN)
        print("Pedestrian button initialized.")

    def is_pressed(self):
        """
        Check if the pedestrian button is pressed.
        """
        print("Checking if pedestrian button is pressed.")
        return self.button.value(1) == 1


class State:
    """
    Represents a state of the traffic light system.
    """

    def __init__(self, traffic_light_system, light, next_state):
        """
        Initialize a state of the traffic light system.
        """
        self.traffic_light_system = traffic_light_system
        self.light = light
        self.next_state = next_state
        print("State initialized.")

    def activate(self):
        """
        Activates this state, turning on the associated light and turning off the others.
        """
        self.traffic_light_system.red_light.off()
        self.traffic_light_system.yellow_light.off()
        self.traffic_light_system.green_light.off()
        self.light.on()
        print("State activated.")

    def transition(self):
        """
        Transitions to the next state of the traffic light system.
        """
        if self.traffic_light_system.pedestrian_button.is_pressed():
            self.traffic_light_system.set_state(self.traffic_light_system.red_state)
        else:
            self.traffic_light_system.set_state(self.next_state)


class TrafficLightSystem:
    """
    Represents a traffic light system.
    """

    def __init__(self, red_light, yellow_light, green_light, pedestrian_button):
        """
        Initialize a traffic light system.
        """
        self.red_light = red_light
        self.yellow_light = yellow_light
        self.green_light = green_light
        self.pedestrian_button = pedestrian_button
        self.red_state = State(self, red_light, None)
        self.yellow_state = State(self, yellow_light, self.red_state)
        self.green_state = State(self, green_light, self.yellow_state)
        self.red_state.next_state = self.green_state
        self.current_state = self.red_state
        print("Traffic light system initialized.")

    def set_state(self, state):
        """
        Sets the current state of the traffic light system.
        """
        self.current_state = state

    def run(self):
        """
        Run the traffic light system.
        """
        while True:
            self.current_state.activate()
            utime.sleep(2)
            self.current_state.transition()


# Initialize the lights and the pedestrian button
red_light = Light(11)
yellow_light = Light(8)
green_light = Light(5)
pedestrian_button = PedestrianButton(2)  # Assuming pedestrian button is connected to pin 2

# Initialize the traffic light system
traffic_light_system = TrafficLightSystem(red_light, yellow_light, green_light, pedestrian_button)

# Run the traffic light system?
traffic_light_system.run()
