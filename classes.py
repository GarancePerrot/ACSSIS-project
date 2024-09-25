
class BreathingPattern:
    """Represents a breathing pattern with inhaling and exhaling times"""

    def __init__(self, inhaling_time, exhaling_time):
        """Initializes a new BreathingPattern object
        args: t_inh (float) in seconds, t_exh (float) in seconds
        """
        self.t_inh = inhaling_time
        self.t_exh = exhaling_time

    def get_t_inh(self):
        return self.t_inh

    def get_t_exh(self):
        return self.t_exh

    def set_t_inh(self, new_inhaling_time):
        self.t_inh = new_inhaling_time

    def set_t_exh(self, new_exhaling_time):
        self.t_exh = new_exhaling_time

    def __str__(self):
        """Returns a string representation of the breathing pattern"""
        return f"Inhaling time: {self.inhaling_time} seconds, Exhaling time: {self.exhaling_time} seconds"
        
        
#___________________________________________________________________________________________________________________



class ReactionTime:
    """Represents a reaction time measurement"""

    def __init__(self, value):
        """Initializes a new ReactionTime object.
        args : value (float) in milliseconds.
        """
        self.value = value

    def __str__(self):
        """Returns a string representation of the reaction time."""
        return f"Reaction time: {self.value} ms"


class SimpleRT(ReactionTime):
    """Simple reaction time experiment"""

    def __init__(self, value):
        super().__init__(value)


class RecognitionRT(ReactionTime):
    """Recognition reaction time experiment"""

    def __init__(self, value):
        super().__init__(value)


class ChoiceRT(ReactionTime):
    """Choice reaction time experiment"""

    def __init__(self, value):
        super().__init__(value)