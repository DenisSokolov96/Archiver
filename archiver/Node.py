from typing import Optional


class Node:
    def __init__(self):
        self._symbol = 0
        self._k = 0
        self._left = None
        self._right = None

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, k):
        self._k = k

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left: Optional['Node']):
        self._left = left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right: Optional['Node']):
        self._right = right

    def is_leave(self):
        return True if self._left is None and self._right is None else False

    def __repr__(self):
        return f"Node(sym='{self.symbol}', k={self.k})"
