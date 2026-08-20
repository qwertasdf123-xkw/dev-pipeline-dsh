---
name: dev-pipeline-dsh
description: 11 步开发流水线（DSH agent 版 v2）。阶段门禁 approve 推进，维护 .dev/STATUS.md 与 decision-log，L1/L2/L3 成熟度动态加载，与 vibe 治理运行时协作。用户说走 dev-pipeline / 用流水线 / 按流程来 / 立项 / 继续当前阶段时激活。
whenToUse: 用户要求走 dev-pipeline / 用流水线 / 按流程来 / 立项 / 继续当前阶段；或多阶段开发需要门禁推进与可追溯决策；或存量环境/代码改造任务（盘点到部署全流程）；或与 vibe 协作时作为项目执行流程层。
metadata:
  id: dev-pipeline-dsh
  notFor:
    - 轻量问答、单命令检查
    - 用户明确指定其他技能的任务
    - 已有既定流程且用户未要求流水线
  inputs:
    - 用户任务描述（原样保留，不摘要）
    - 现有 .dev/STATUS.md 与 decision-log（续跑时）
    - 工作区路径与沙箱模式（DSH 会话上下文）
  outputs:
    - .dev/STATUS.md（maturity + stage + action）
    - .dev/decision-log.md（Reason + Alternatives + Supersedes）
    - gate-report-NN.md（每阶段，等 approve）
    - spec / design / research / plan 等阶段制品
  planHints:
    - 每阶段先读 stages/NN-*.md 与对应模板
    - 门禁用 ask_user_question 确认（多选题 + 推荐默认）
    - 跨轮次用 goal 工具立项，STATUS.md 作档案
  verifyHints:
    - 检查 STATUS.md 与 decision-log 已更新
    - 检查 gate-report 已存档且状态一致
    - 检查上一阶段产物可恢复（重启入口）
  tags:
    - dev-pipeline
    - workflow
    - gates
    - dsh
  priority: 50
---

# dev-pipeline-dsh (v2)

只在显式触发时激活。阶段: 0 Inspiration → 1 Spec → 2 Design → 3 Research → 4 Plan → 5 Setup → 6 Code → 7 Verify → 8 Audit → 9 Deploy → 10 Observe

## 适用场景（关键词）
- 走 dev-pipeline / 用流水线 / 按流程来 / 立项 / 继续当前阶段
- 多阶段开发、存量环境改造、需要门禁与决策留痕的任务
- 复杂任务与 vibe 协作时的执行流程层

## 硬性规则
1. 每阶段结束产出 Gate Report，必须等用户 approve 才进下一阶段；不自行跨阶段
2. 维护项目 .dev/STATUS.md（maturity + stage + action）与 .dev/decision-log.md（Reason + Alternatives + Supersedes）
3. 改 .env / 凭证 / 删文件 / git push 必须先 ask（用 ask_user_question）
4. 切成熟度: 读 maturity/L<new>-rules.md + 更新 STATUS + 记决策
5. 跨轮次目标: create_goal 立项（goal=运行态）；STATUS.md 作档案（两者同步）

## 门禁确认（DSH 原生）
- 用 ask_user_question 发 Gate Report：选项 [approve（推荐）| modify | abort]，一次问清
- agent 不自行 approve；abort 走 templates/gate-report.md §Abort 联动

## DSH 工具映射
| 需要 | 工具 |
|---|---|
| 读/写/改文件 | read / write / edit |
| 执行命令 | pwsh（PowerShell 5.1） |
| 步骤清单 | todo_write（执行态）；plan.md 存档 |
| 跨轮次目标 | create_goal / update_goal / get_goal |
| 门禁/提问 | ask_user_question（多选题 + 推荐） |
| 后台命令 | pwsh run_in_background + job_output / job_kill |
| 并行/委派 | subagent（后台）+ job_output 收集 |
| 调研 | web_search + subagent 并行 |
| 大规模编排 | workflow |
| 加载关联技能 | skill（如 vibe） |

## 沙箱与权限（DSH 执行现实）
- 默认文件沙箱为 workspace-write：只允许写当前工作区（如 E:\test）
- 写入工作区外（如 E:\dsh-ecosystem、C:\Users\...\.dsh）需 sandbox_permissions: danger-full-access + justification，一次一令
- 沙箱拒绝即停止并说明，不绕行、不换方式重试；pwsh 只读运行在 ConstrainedLanguage 模式
- Setup/Deploy 涉及越区写入前，先确认目标路径与授权范围

## 存量改造路径（v2 新增）
任务对象是现有环境/代码时（如本机环境恢复）：
1. Stage 0-1 先盘点现状（读配置/列目录/确认基线）
2. 改造方案优先最小侵入：diff 式变更 + 备份点（如 _backup_YYYYMMDD）
3. 每步可回滚：变更前记录恢复命令
4. Stage 7 Verify 用验收清单验证（无代码项目不需要测试套件）

## 与 vibe 协作（v2 新增）
- vibe = 治理运行时（冻结需求/计划/执行闭环）；本技能 = 项目流程纪律（阶段/门禁/制品）
- 复杂任务模式: vibe 冻结需求与计划 → dev-pipeline-dsh 执行阶段门禁 → vibe 验证
- 制品不双轨：需求/计划由 vibe 产出时，本技能引用而非重写

## 永不做
默删 / force-push / 密钥轮换 / 改 settings 无确认 / 跳门禁 / 无 approve 跨阶段

## 中止而非删除
用户中止项目时保留所有文件，仅切 STATUS 状态（aborted / paused）。禁止删除 aborted 项目。

## 进阶 (L2+ 推荐)
- 加载细节: 见 loading.md
- 复杂任务: 调 subagent → templates/subagent-prompts.md
- 上下文压缩: templates/state-preservation.md
