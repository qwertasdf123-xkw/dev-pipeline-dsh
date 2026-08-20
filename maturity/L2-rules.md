# L2 规则 — Small Team

> 继承 L1 + 加 PR review / CI 强制 / 文档规范。

## 时间盒
| 阶段 | 时限 |
|------|------|
| Spec | 30-60 min + peer review |
| Design | 1-2 天 |
| Research | 1-3 天 + spike report |
| Plan | 半天 |
| Setup | 半天 + CI 配置 |
| Code | PR review 节奏(SLA 24h) |
| Verify | 半天 + CI 覆盖度门槛 |
| Audit | 半天 + peer review |
| Deploy | 1h + 变更工单 + 灰度 |
| Observe | 双周 retro |

## 制品要求(强于 L1)
- Spec: 模板化 + 用户故事 + 验收标准 + NFR,下游角色全员 review
- Design: 设计文档 + 架构草图入版本化 repo
- Research: 对比表 + ADR 入版本化 repo
- Plan: 任务图入版本化 repo,技术选型入 tech radar
- Setup: 完整 CI 配置,PR 受保护分支
- Code: PR 流程,作者/审阅者分离
- Verify: CI 强制覆盖度门槛
- Audit: 共享清单,作者/审阅者分离
- Deploy: runbook + 变更工单 + 灰度 + 回滚方案
- Observe: 结构化 retro,有主人的实验

## 评审
- Spec / Design / Audit 必须有 peer review
- 设计方向由 tech lead 拍板
- Audit P0/P1 必须有人签字

## 自动化(强于 L1)
- CI 强制覆盖度门槛,PR 自动跑 lint + test
- 自动 changelog 生成,可选 SAST/SCA(推荐但不强制)

## 文档(强于 L1)
- ADR / Runbook 入版本化 repo,API 文档自动生成,决策记录关联 issue

## 安全/Docs/PDCA
- Security: 共享 threat model + review board
- Docs: ADR + runbook + API docs
- PDCA: 双周 retro,facilitator 轮值

## 流程(强于 L1)
- WIP 限制(Kanban),明确分支策略(trunk-based 或 GitFlow)
- Code review SLA,共享 STATUS 看板

## 不可妥协
- force-push: 禁止; 跳过 review: 禁止; 跳过 audit: 禁止; 合并到 main 无 review: 禁止