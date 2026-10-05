# turn-order

回合出手顺序：按速度降序排，被控制的角色占位但跳过。仓库里没有命令行入口，
现状值用 `python3 -m unittest -v tests.test_anchors` 打印，只用 Python 标准库。

```
python3 -m unittest -v tests.test_anchors
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **排序**：按速度降序；速度相同按角色名字升序，顺序与加入先后无关。
- **控制**：被控制的角色仍然出现在这一轮的顺序里，但 `skip` 标记为真，不占别人的位置。
- **每轮重排**：每轮都用当前速度重新排序，速度被状态修正后要反映出来。
- **幂等**：同一个 `round_id` 只结算一次，重复调用返回上一次的顺序。
- **代价**：结算不许全扫角色表（速度变化只让受影响的顺序失效），`scanned` 不随角色数乘结算次数增长；
  10 万角色每秒 10 万次结算。

## 输出契约（不改格式）

```
first=..
len=.. skip=..
same=..
scanned=..
```

## 目录

```
turnorder/order.py        排序、控制占位与每轮重排
tests/test_order.py       单元用例
tests/test_anchors.py     现状值样例
```
