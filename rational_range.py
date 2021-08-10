from fractions import Fraction


class RationalRange:

    def __init__(self, start, stop, num_steps):
        if num_steps != int(num_steps):
            raise ValueError(f"The number of steps {num_steps} is not an integer value")
        if num_steps < 1:
            raise ValueError(f"Number of steps {num_steps} is not positive")
        self._start = Fraction(start)
        self._num_steps = num_steps
        self._step = Fraction(stop - start, num_steps)

    # If __next__() is not defined, it looks for the __getitem__() method
    def __getitem__(self, index):
        if not(0 <= index < self._num_steps):
            raise IndexError
        return self._start + index * self._step
