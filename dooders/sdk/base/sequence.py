import copy
import json
from collections import deque

import numpy as np


class State:
    pass


class Sequence:
    """
    Sequence of states over time.

    The sequence is stored as a deque, with the most recent state at the start
    of the sequence.

    Attributes
    ----------
    history : deque
        The sequence of states
    current_index : int
        The current index in the sequence

    Methods
    -------
    add_state(state)
        Add a state to the sequence
    get_next_state()
        Get the next state in the sequence
    get_previous_state()
        Get the previous state in the sequence
    get_state(steps_back)
        Get a state from the sequence
    clear_history()
        Clear the sequence history
    reduce_states(n)
        Reduce the number of states in the sequence by a factor of n
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        max_length : int, optional
            The maximum number of states to store in the sequence, by default 1000
        """
        self.history = deque()
        self.current_index = 0

    def add_state(self, state: "State") -> None:
        """
        Add a state to the sequence.

        Sets the current index to the start of the sequence.

        Parameters
        ----------
        state : State
            The state to add to the sequence
        """
        # # Only add state if the cycle number is different from most recent state
        if self.history and state.cycle == self.history[0].cycle:
            return
        new_state = copy.deepcopy(state)
        self.history.appendleft(new_state)
        self.current_index = 0  # Reset index to the start on new state addition

    def get_next_state(self) -> "State":
        """
        Get the next state in the sequence.

        Increments the current index by 1.

        Returns
        -------
        State
            The next state in the sequence
        """
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None

    def get_previous_state(self) -> "State":
        """
        Get the previous state in the sequence.

        Decrements the current index by 1.

        Returns
        -------
        State
            The previous state in the sequence
        """
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None

    def get_state(self, steps_back: int = 0) -> "State":
        """
        Get a state from the sequence.

        Parameters
        ----------
        steps_back : int, optional
            The number of states to go back in the sequence, by default 0 which
            returns the current state
        """
        if steps_back < len(self.history):
            return self.history[steps_back]
        return None

    def clear_history(self) -> None:
        """
        Clear the sequence history.
        """
        self.history.clear()

    def reduce_states(self, n: int) -> None:
        """
        Reduce the number of states in the sequence by a factor of n.

        Parameters
        ----------
        n : int
            The factor to reduce the number of states by
        """
        if n <= 1:
            return  # Avoid removing all states

        reduced_history = deque()
        for i, state in enumerate(self.history):
            if i % n != 0:
                reduced_history.appendleft(state)

        self.history = reduced_history
        self.current_index = min(self.current_index, len(self.history) - 1)

    def process(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Process the sequence creating features and targets.

        The target is tied to the previous state. Since the features should
        precede the target for a model to predict.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            The features and targets extracted from the sequence
        """

        features = np.array([state.features for state in list(self.history)[1:]])
        targets = np.array([state.features for state in list(self.history)[:-1]])

        return features, targets

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            The number of states in the sequence
        """
        return len(self.history)

    def __getitem__(self, key: int) -> "State":
        """
        Returns
        -------
        State
            The state at the given index
        """
        return self.history[key]

    def __iter__(self):
        """
        Returns
        -------
        iter
            An iterator over the sequence
        """
        return iter(self.history)

    def __reversed__(self):
        """
        Returns
        -------
        reversed
            A reversed iterator over the sequence
        """
        return reversed(self.history)

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            A string representation of the sequence
        """
        return str(self.history)

    def __repr__(self) -> str:
        """
        Returns
        -------
        str
            A string representation of the sequence
        """
        return str(self.history)


class SequenceList(list):
    """
    List of state sequences.

    Attributes
    ----------
    features : list
        The features extracted from the sequence list
    targets : list
        The targets extracted from the sequence list

    Methods
    -------
    process()
        Process the sequence list creating features and targets
    to_dict()
        A dictionary representation of the sequence
    to_json()
        A JSON representation of the sequence
    save(path)
        Save the sequence to a file.
    """

    def __init__(self, *args) -> None:
        self.features = []
        self.targets = []
        super(SequenceList, self).__init__(args)

    def process(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Process the sequence list creating features and targets.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            The features and targets extracted from the sequence list
        """
        self.features = []
        self.targets = []

        for sequence in self:
            features, targets = sequence.process()
            self.features.append(features)
            self.targets.append(targets)

        self.features = np.concatenate(self.features).tolist()
        self.targets = np.concatenate(self.targets).tolist()

        return self.features, self.targets

    def to_dict(self) -> dict:
        """
        Returns
        -------
        dict
            A dictionary representation of the sequence
        """
        return {"features": self.features, "targets": self.targets}

    def to_json(self) -> str:
        """
        Returns
        -------
        str
            A JSON representation of the sequence
        """
        return json.dumps(self.to_dict())

    def save(self, path: str) -> None:
        """
        Save the sequence to a file.

        Parameters
        ----------
        path : str
            The path to save the sequence to
        """
        with open(path, "w") as f:
            f.write(self.to_json())

    def sample(self, n: int) -> "SequenceList":
        """
        Sample n sequences from the sequence list

        Parameters
        ----------
        n : int
            Number of sequences to sample

        Returns
        -------
        SequenceList
            Sampled sequence list
        """
        sampled_indices = np.random.choice(len(self), n, replace=False)
        return SequenceList(*[self[i] for i in sampled_indices])

    @property
    def sequences(self, n: int) -> list:
        """
        Bundle sequences into a list of n sequences

        Parameters
        ----------
        n : int
            Number of sequences to bundle together

        Returns
        -------
        list
            List of n sequences
        """

        return [self[i : i + n] for i in range(0, len(self), n)]
