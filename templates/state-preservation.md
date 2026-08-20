# 上下文压缩 / 状态保存 (DSH 版)

> 触发: context 使用超过 50%，或阶段切换需清空工作集。

## 保留（进主上下文）
1. .dev/STATUS.md — 当前阶段 + maturity + 状态
2. .dev/decision-log.md — 前 3 条决策（含 Supersedes）
3. 当前 gate-report 状态
4. 当前 stage 的入口指令

## 落盘（写文件，不进上下文）
1. 阶段产物: spec.md / design.md / research.md / plan.md
2. subagent 输出摘要 → .dev/research-notes/ 或 .dev/subagent-output/
3. 代码进度 → 版本控制 commit

## 丢弃
- 中间调试输出、临时文件
- 已归档的 subagent 原始输出

## 恢复入口
记录重启命令: 从 STATUS.md 的下一步 + 对应 stage 文件继续。

## 压缩后必做
1. 更新 STATUS.md（压缩时间）
2. decision-log 追加压缩决策
3. 验证重启入口可执行
