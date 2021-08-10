def _is_perfect_length(sequence):
    n = len(sequence)
    return ((n + 1) & n == 0) and (n != 0)


class LevelOrderIterator:

    def __init__(self, sequence):
        if not _is_perfect_length(sequence):
            raise ValueError(
                f"Sequence of length {len(sequence)} does not represent "
                "a perfect binary tree with length 2^n - 1"
            )
        self._sequence = sequence
        self._index = 0

    def __next__(self):
        if self._index >= len(self._sequence):
            raise StopIteration
        result = self._sequence[self._index]
        self._index += 1
        return result

    def __iter__(self):
        return self


# _left_child method returns the index of the  child given the index of the parent
def _left_child(index):
    return 2 * index + 1


# _right_child method returns the index of the  child given the index of the parent
def _right_child(index):
    return 2 * index + 2


class PreOrderIterator:

    def __init__(self, sequence):
        if not _is_perfect_length(sequence):
            raise ValueError(
                f"Sequence of length {len(sequence)} does not represent "
                "a perfect binary tree with length 2^n - 1"
            )
        self._sequence = sequence
        self._stack = [0]

    def __next__(self):
        if len(self._stack) == 0:
            raise StopIteration

        index = self._stack.pop()
        result = self._sequence[index]

        # Pre-order: Push right child first so left child is
        # popped and processed first. Last-in, first-out
        right_child_index = _right_child(index)
        if right_child_index < len(self._sequence):
            self._stack.append(right_child_index)

        left_child_index = _left_child(index)
        if left_child_index < len(self._sequence):
            self._stack.append(left_child_index)

        return result

    def __iter__(self):
        return self


class InOrderIterator:

    def __init__(self, sequence):
        if not _is_perfect_length(sequence):
            raise ValueError(
                f"Sequence of length {len(sequence)} does not represent "
                "a perfect binary tree with length 2^n - 1"
            )
        self._sequence = sequence
        self._stack = []
        self._index = 0

    def __next__(self):
        if (len(self._stack) == 0) and (self._index >= len(self._sequence)):
            raise StopIteration

        # Push left children onto the stack while possible
        while self._index < len(self._sequence):
            self._stack.append(self._index)
            self._index = _left_child(self._index)

        # Pop from stack and process, before moving to the right child
        index = self._stack.pop()
        result = self._sequence[index]
        self._index = _right_child(index)
        return result

    def __iter__(self):
        return self


missing = object()


# This class iterate an imperfect tree using  the "missing" word to occupy
# the missing positions. Ex: iterator = ["+", "r", "*", missing, missing, "p", "q"]
class SkipMissingIterator:

    def __init__(self, iterator):
        self._iterator = iter(iterator)

    def __next__(self):
        while True:
            item = next(self._iterator)
            if item is not missing:
                return item

    def __iter__(self):
        return self


# This class iterates an iterator composed of symbols like "* or /"
# and transform them.
class TranslationIterator:

    def __init__(self, table, iterator):
        self.table = table
        self.iterator = iterator

    def __next__(self):
        item = next(self.iterator)
        return self.table.get(item, item)

    def __iter__(self):
        return self


class PerfectBinaryTree:

    def __init__(self, breadth_first_items):
        self._sequence = tuple(breadth_first_items)
        if not _is_perfect_length(self._sequence):
            raise ValueError(
                f"Sequence of length {len(self._sequence)} does not represent "
                "a perfect binary tree with length 2^n - 1"
            )

    def __iter__(self):
        return SkipMissingIterator(PreOrderIterator(self._sequence))
