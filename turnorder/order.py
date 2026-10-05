"""回合出手顺序：按速度降序排，被控制的角色占位但跳过。

排序口径：速度降序，同速按名字升序，与加入先后无关；被控制的角色仍在顺序里，
skip 标记为真；每轮用当前速度重排；同一个 round_id 只结算一次，重复调用返回
上一次的结果。速度索引随 add/set_speed 增量维护，结算不全扫角色表。
"""

from bisect import bisect_left, insort


class Order:
    """出手顺序台账。"""

    def __init__(self):
        self.units = {}
        self.stunned = set()
        self.rounds = {}
        self.scanned = 0
        # 按 (-速度, 名字) 升序维护的索引，即速度降序、同速名字升序。
        self._index = []

    def add(self, name, speed):
        """加入一个角色。"""
        if name in self.units:
            self._remove_from_index(name)
        self.units[name] = speed
        insort(self._index, (-speed, name))
        self.scanned += 1

    def set_speed(self, name, speed):
        """改速度（可能来自状态修正），只让受影响的顺序失效。"""
        if name in self.units:
            self._remove_from_index(name)
        self.units[name] = speed
        insort(self._index, (-speed, name))
        self.scanned += 1

    def _remove_from_index(self, name):
        key = (-self.units[name], name)
        pos = bisect_left(self._index, key)
        if pos < len(self._index) and self._index[pos] == key:
            del self._index[pos]

    def stun(self, name):
        """把角色标记为被控制。"""
        self.stunned.add(name)

    def resolve(self, round_id):
        """结算这一轮的出手顺序，返回 (名字, 是否跳过) 列表。

        按速度降序、同速名字升序；被控制的角色占位但 skip 为真；同一个
        round_id 幂等，重复调用返回上一次的顺序；结算只读增量索引，不全扫
        角色表。
        """
        if round_id in self.rounds:
            return self.rounds[round_id]
        order = [(name, name in self.stunned) for _, name in self._index]
        self.rounds[round_id] = order
        return order
