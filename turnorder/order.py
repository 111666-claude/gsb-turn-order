"""回合出手顺序：按速度降序排，速度相同按名字升序，被控制的角色占位但跳过。"""


class Order:
    """出手顺序台账。"""

    def __init__(self):
        self.units = {}
        self.stunned = set()
        self.rounds = {}
        self.scanned = 0
        self._order = None

    def add(self, name, speed):
        """加入一个角色。"""
        self.units[name] = speed
        self._order = None

    def set_speed(self, name, speed):
        """改速度（可能来自状态修正）。"""
        self.units[name] = speed
        self._order = None

    def stun(self, name):
        """把角色标记为被控制。"""
        self.stunned.add(name)
        self._order = None

    def resolve(self, round_id):
        """结算这一轮的出手顺序，返回 (名字, 是否跳过) 列表。

        同一个 round_id 只结算一次：重复调用直接返回上一次的顺序。
        不同轮次按当前速度重新排序；只有状态发生变化后才需要重新扫描角色表，
        连续结算不随角色数乘结算次数增长。
        """
        if round_id in self.rounds:
            return self.rounds[round_id]
        if self._order is None:
            self.scanned += len(self.units)
            self._order = tuple(
                (name, name in self.stunned)
                for name in sorted(self.units, key=lambda name: (-self.units[name], name))
            )
        order = self._order
        self.rounds[round_id] = order
        return order
