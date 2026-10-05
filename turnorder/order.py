"""回合出手顺序：按速度降序排，被控制的角色占位但跳过。

缺陷：同速按加入顺序而不是名字升序、被控制的角色直接从顺序里删掉、同一个 round_id 重复结算会重算、
每次结算全扫角色表。
"""


class Order:
    """出手顺序台账。"""

    def __init__(self):
        self.units = {}
        self.stunned = set()
        self.rounds = {}
        self.scanned = 0

    def add(self, name, speed):
        """加入一个角色。"""
        self.units[name] = speed

    def set_speed(self, name, speed):
        """改速度（可能来自状态修正）。"""
        self.units[name] = speed

    def stun(self, name):
        """把角色标记为被控制。"""
        self.stunned.add(name)

    def resolve(self, round_id):
        """结算这一轮的出手顺序，返回 (名字, 是否跳过) 列表。

        缺陷：同速按加入顺序、被控的删掉、不按 round_id 幂等、全扫角色表。
        """
        self.scanned += len(self.units)
        names = sorted(self.units, key=lambda name: -self.units[name])
        return [(name, False) for name in names if name not in self.stunned]
