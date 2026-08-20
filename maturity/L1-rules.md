# L1 规则 — Solo Developer

> 单人/单兵。最大化价值/小时,最小化仪式。

## 时间盒
| 阶段 | 时限 |
|------|------|
| Spec | 30 min |
| Design | 30-60 min |
| Research | 仅在未知点承重时,30 min 封顶 |
| Plan | 30-60 min |
| Setup | 10-30 min |
| Code | 每周期 90 min |
| Verify | 30 min |
| Audit | 30 min(时限即门限) |
| Deploy | 15 min |
| Observe | 每周 10 min |

## 制品要求
- Spec: 1 页,8 节齐全
- Design: 1 段理由 + mermaid 草图
- Research: 对比表 + 推荐
- Plan: 任务图 + 依赖
- Setup: 能跑通 dev 环境
- Code: commit message 清晰,单测同步写
- Verify: 覆盖率报告（有测试时）或验收清单（无测试时）
- Audit: 5 项清单全勾
- Deploy: runbook 存在
- Observe: 每周复盘

## 评审
- 所有 Gate Report 自己批准
- 无 peer review,无架构评审委员会

## 自动化
- 保存/提交时跑测试(pwsh 或 git hook)
- 不要求 CI/CD 完整流水线,不要求 coverage gate,不要求 SAST/SCA

## 文档
- Spec 即 v0 文档,README 够用
- 决策记 decision-log,不要求 ADR 完整归档

## 切换提示
- 想要 peer review → 试 L2
- 需要多人协作 / CI 强制 → 进 L2
- 涉及合规 / 客户级 SLO → 进 L3
