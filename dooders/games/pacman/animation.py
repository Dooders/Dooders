from dooders.games.pacman.settings import *


class Animator:
    """
    Class is designed to manage animations by allowing you to specify a sequence
    of frames, the speed at which they should be played, and whether the
    animation should loop or stop when it reaches the end.

    The update method is typically called in each frame to determine which frame
    should be displayed at that moment.

    Attributes
    ----------
    frames : list
        A list of frames to be animated.
    current_frame : int
        The index of the current frame.
    speed : int
        The speed at which the animation should play.
    loop : bool
        Whether or not the animation should loop.
    dt : int
        The time increment.
    finished : bool
        Whether or not the animation has finished playing.

    Methods
    -------
    reset()
        Resets the animation to its initial state, setting current_frame to 0
        and marking it as not finished.
    update(dt)
        Takes a time increment (dt) as a parameter and updates the animation.
        If the animation is not marked as finished, it calls the nextFrame
        method to determine the next frame to display.
        Checks if the current_frame has reached the end of the animation sequence.
        If loop is True, it resets the animation to the beginning
            (current_frame = 0) when it reaches the end.
        If loop is False, it marks the animation as finished
            (finished = True) and keeps current_frame at its last value.
    nextFrame(dt)
        Increments dt with the provided dt value.
        If dt exceeds the time required to advance to the next frame (based on
        the speed attribute), it increments current_frame by 1 and resets dt to 0.
    """

    def __init__(self, frames: list = [], speed: int = 20, loop: bool = True) -> None:
        """
        Initializes the frames, current_frame, speed, loop, dt, and finished
        attributes.

        Parameters
        ----------
        frames : list
            A list of frames to be animated.
        speed : int
            The speed at which the animation should play.
        loop : bool
            Whether or not the animation should loop.
        """
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    def reset(self) -> None:
        """
        Resets the animation to its initial state, setting current_frame to 0
        and marking it as not finished.
        """
        self.current_frame = 0
        self.finished = False

    def update(self, dt: int) -> None:
        """
        Takes a time increment (dt) as a parameter and updates the animation.

        If the animation is not marked as finished, it calls the nextFrame
        method to determine the next frame to display.

        Checks if the current_frame has reached the end of the animation sequence.

        If loop is True, it resets the animation to the beginning
            (current_frame = 0) when it reaches the end.
        If loop is False, it marks the animation as finished
            (finished = True) and keeps current_frame at its last value.

        Parameters
        ----------
        dt : int
            The time increment.
        """
        if not self.finished:
            self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.finished = True
                self.current_frame -= 1

        return self.frames[self.current_frame]

    def nextFrame(self, dt: int) -> None:
        """
        Increments dt with the provided dt value.

        If dt exceeds the time required to advance to the next frame (based on
        the speed attribute), it increments current_frame by 1 and resets dt to 0.

        Parameters
        ----------
        dt : int
            The time increment.
        """
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0
