# 当前状态

> 由 dev-pipeline 自动维护
> 每阶段开始/结束时 agent 更新此处

# 终止态不等于删除：文件保留，仅切状态

## 当前阶段
- **Stage**: 0
- **名称**: Inspiration 灵感收集
- **开始时间**:
- **成熟度**: L1
- **目标**: （跨轮次目标；宿主无 goal 能力时直接写在这里）
- **状态**: 进行中 / 阻塞 / 等门禁 / 已完成

## 终止态
- aborted: 用户显式终止（不做了/abort/算了）
- paused: 临时挂起（可指定 resume 条件）
- archived-pending-restart: 重新开始前的备份窗口期

## 终止态附加字段（建议填充）
- **aborted_at**: YYYY-MM-DD（终止时间）
- **aborted_stage**: N（终止的阶段号）
- **abort_reason**: 简短的终止原因（用户原话摘录即可）

## 上下文
- **项目**:
- **工作目录**:
- **上一次完成**:
- **宿主**: (mavis / dsh / claude-code / other)
- **模式**: standalone | vibe-collab
- **能力映射**: .dev/runtime.json

## 当前任务
- [ ]

## 阻塞 / 待决策
-

## 下一步
→ Stage 1: Spec（触发：我想做 X）

---

最后更新: