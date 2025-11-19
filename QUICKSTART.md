# Quick Start Guide - Jungle Game

## 1. 快速开始 (Quick Start)

```bash
cd /Users/bits12/Desktop/JungleGame
python3 main.py
```

## 2. 第一个游戏 (First Game)

### 启动游戏
```
$ python3 main.py
Start a new game? (y/n): y
✓ New game started!
```

### 查看棋盘
棋盘会自动显示，RED 在底部（小写），BLUE 在顶部（大写）

### 移动棋子
```
Enter command: move E3 E4
```
这会将 E3 位置的棋子移动到 E4

### 查看合法移动
```
Enter command: show E3
```
会高亮显示 E3 位置棋子的所有合法移动

### 撤销移动
```
Enter command: undo
```

### 保存游戏
```
Enter command: save mygame
✓ Game saved to mygame.json
```

### 加载游戏
```
Enter command: load mygame
✓ Game loaded from mygame.json
```

## 3. 游戏规则速查 (Rules Quick Reference)

### 棋子等级 (Piece Ranks)
```
8. Elephant (象)  - 最强，但怕老鼠
7. Lion (狮)      - 可跳河
6. Tiger (虎)     - 可跳河
5. Leopard (豹)
4. Wolf (狼)
3. Dog (狗)
2. Cat (猫)
1. Rat (鼠)       - 最弱，但能吃象，能游泳
```

### 特殊规则
- **老鼠吃象**: Rat (rank 1) 可以吃 Elephant (rank 8)
- **跳河**: Lion 和 Tiger 可以跳过 3 格宽的河流
- **游泳**: 只有 Rat 可以进入水域
- **陷阱**: 进入对方陷阱的棋子战力变为 0
- **兽穴**: 进入对方兽穴即获胜

### 胜负判定
- ✅ **胜利**: 进入对方兽穴 (D1 或 D9)
- ✅ **胜利**: 对方无合法移动
- 🤝 **平局**: 50 步无吃子
- 🤝 **平局**: 局面重复 3 次

## 4. 进阶功能 (Advanced Features)

### 回放模式 (Replay)
```
Enter command: replay
Replay command: next     # 下一步
Replay command: prev     # 上一步
Replay command: goto 5   # 跳到第 5 步
Replay command: play     # 自动播放
Replay command: exit     # 退出回放
```

### 查看历史 (History)
```
Enter command: history
--- Last 10 Moves ---
  1. RED Rat E3→E4
  2. BLUE Lion G7→F7
  3. RED Rat E4→E5 (captured BLUE Cat)
```

## 5. 常见问题 (FAQ)

### Q: 如何知道哪些棋子可以移动？
A: 使用 `show <position>` 命令，例如 `show E3`

### Q: 如何撤销错误的移动？
A: 使用 `undo` 命令，最多可以撤销 10 步

### Q: 游戏如何结束？
A: 当一方棋子进入对方兽穴，或对方无法移动时

### Q: 如何保存游戏进度？
A: 使用 `save <filename>` 命令

### Q: Lion/Tiger 如何跳河？
A: 直接移动到河对岸，例如 `move C4 C7`（如果河中没有 Rat）

## 6. 示例游戏 (Example Game)

```bash
# 开始新游戏
Start a new game? (y/n): y

# RED 移动 Rat
Enter command: move E3 E4
✓ Move successful

# BLUE 移动 Rat
Enter command: move C7 C6
✓ Move successful

# 查看 RED Rat 可以去哪里
Enter command: show E4
Legal moves for Rat at E4:
  E5
  E3
  D4
  F4

# RED Rat 进入水中
Enter command: move E4 F4  # F4 是河流
✓ Move successful

# 继续游戏...
```

## 7. 快捷键盘操作建议

为了快速游戏，建议：
1. 先用 `show` 查看合法移动
2. 再用 `move` 执行移动
3. 定期用 `save` 保存进度
4. 用 `history` 查看之前的移动

## 8. 测试游戏 (Test the Game)

运行测试确保一切正常：
```bash
python3 test_game.py
```

应该看到：
```
==================================================
RUNNING TESTS
==================================================
...
✓ ALL TESTS PASSED!
==================================================
```

## 9. 项目文件结构

```
JungleGame/
├── model/              # 游戏逻辑（不依赖界面）
├── view/               # 界面显示
├── controller/         # 控制器
├── main.py             # 程序入口
├── test_game.py        # 测试文件
└── README.md           # 详细文档
```

## 10. 获取帮助

- 查看 `README.md` 了解完整功能
- 查看 `JungleGame_Spec.md` 了解详细规则
- 运行 `python3 test_game.py` 测试功能

---

**Enjoy the game! 祝游戏愉快！** 🎮
