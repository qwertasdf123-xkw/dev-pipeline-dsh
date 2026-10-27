---
name: dev-pipeline-dsh
description: 11 步可移植开发流水线（v3.0.1）。阶段门禁 approve 推进，维护 .dev/STATUS.md 与 decision-log，L1/L2/L3 成熟度动态加载，可与 vibe 治理运行时协作。当用户要求走 dev-pipeline / 用流水线 / 按流程来 / 立项 / 继续当前阶段，或需要多阶段门禁、可追溯决策、存量环境/代码改造时激活。不用于轻量问答、单命令检查或用户已指定其他流程的任务。
metadata:
  id: dev-pipeline-dsh
  portable: true
  hosts:
    - dsh
    - mavis
    - claude-code
    - generic
  notFor:
    - 轻量问答、单命令检查
    - 用户明确指定其他技能的任务
    - 已有既定流程且用户未要求流水线
  inputs:
    - 用户任务描述（原样保留，不摘要）
    - 现有 .dev/STATUS.md 与 decision-log（续跑时）
    - 工作区路径与宿主能力（探测结果见 runtime-adapter.md）
  outputs:
    - .dev/STATUS.md（maturity + stage + action）
    - .dev/decision-log.md（Reason + Alternatives + Supersedes）
    - .dev/runtime.json（宿主能力映射，首次激活时生成）
    - gate-report-NN.md（每阶段，等 approve）
    - spec / design / research / plan 等阶段制品
  planHints:
    - 首次激活先读 runtime-adapter.md 做能力探测，产出 .dev/runtime.json
    - 每阶段先读 stages/NN-*.md 与对应模板
    - 门禁用宿主的多选能力确认；无则文本三选项 + 显式停下等回复
    - 跨轮次目标用宿主 goal 能力；无则记在 STATUS.md
  verifyHints:
    - 检查 STATUS.md 与 decision-log 已更新
    - 检查 gate-report 已存档且状态一致
    - 检查上一阶段产物可恢复（重启入口）
    - 检查 runtime.json 与当前宿主仍匹配
  tags:
    - dev-pipeline
    - workflow
    - gates
    - dsh
    - portable
  priority: 50
---

# dev-pipeline-dsh (v3.0.1 · 可移植版)

只在显式触发时激活。阶段: 0 Inspiration → 1 Spec → 2 Design → 3 Research → 4 Plan → 5 Setup → 6 Code → 7 Verify → 8 Audit → 9 Deploy → 10 Observe

## 适用场景（关键词）
- 走 dev-pipeline / 用流水线 / 按流程来 / 立项 / 继续当前阶段
- 多阶段开发、存量环境改造、需要门禁与决策留痕的任务
- 复杂任务与 vibe 协作时的执行流程层

## 硬性规则
1. 每阶段结束产出 Gate Report，必须等用户 approve 才进下一阶段；不自行跨阶段
2. 维护项目 .dev/STATUS.md（maturity + stage + action）与 .dev/decision-log.md（Reason + Alternatives + Supersedes）
3. 改 .env / 凭证 / 删文件 / git push 必须先 ask（用宿主的多选/提问能力；无则文本询问后停下等回复）
4. 切成熟度: 读 maturity/L<new>-rules.md + 更新 STATUS + 记决策
5. 跨轮次目标: 用宿主 goal 能力立项（运行态）；STATUS.md 作档案（两者同步）
6. 工具不可用时按 runtime-adapter.md 降级；**门禁语义不降级**——缺能力就停下报告，不自批

## 门禁确认（宿主无关）
- 用宿主的多选能力发 Gate Report：选项 [approve（推荐）| modify | abort]，一次问清
- 宿主无多选能力 → 文本三选项 + **显式停下等下一条回复**（见 [runtime-adapter.md](runtime-adapter.md) §5）
- agent 不自行 approve；abort 走 templates/gate-report.md §Abort 联动

## 能力槽映射（宿主无关）
本 skill 只依赖 12 个能力槽，不绑定具体工具。首次激活时按 [runtime-adapter.md](runtime-adapter.md) 探测宿主，把映射写入 `.dev/runtime.json`，此后所有 stage 按槽取工具。

| 槽 | 能力 | DSH 原生 | 通用实现 |
|---|---|---|---|
| C1/C2 | 读写文件 | read / write / edit | 文件读写工具 |
| C3 | 执行命令 | pwsh | 宿主默认 shell |
| C4 | 后台任务 | pwsh run_in_background + job_output | 后台任务 + 结果查询 |
| C5 | 委托子 agent | subagent | 子 agent 工具 |
| C6 | 结构化提问 | ask_user_question | 文本选项 + 显式等待 |
| C7 | 跨轮次目标 | create_goal / update_goal | 目标工具；无则记 STATUS.md |
| C8 | 步骤清单 | todo_write | 待办工具；无则记 plan.md |
| C9 | 联网调研 | web_search | 检索工具 |
| C10 | 加载关联 skill | skill | skill 加载工具 |
| C11 | 大规模编排 | workflow | 编排工具（可选） |
| C12 | 治理运行时 | vibe | 可选，缺失走独立闭环模式 |

> stage 与模板中**不应出现**具体工具名。若出现，即为待修的宿主绑定。

## 沙箱与权限（跨宿主）
- 默认只写当前工作区；工作区路径以实际会话为准，**不要写死盘符**
- 写入工作区外需显式授权 + 一次一令 + 说明理由，授权范围记入 STATUS.md
- 沙箱拒绝即停止并说明，不绕行、不换方式重试
- 宿主有只读/受限 shell 模式（如 DSH 的 ConstrainedLanguage）时，遵守其限制
- Setup/Deploy 涉及越区写入前，先确认目标路径与授权范围

## 存量改造路径（v2 新增）
任务对象是现有环境/代码时（如本机环境恢复）：
1. Stage 0-1 先盘点现状（读配置/列目录/确认基线）
2. 改造方案优先最小侵入：diff 式变更 + 备份点（如 _backup_YYYYMMDD）
3. 每步可回滚：变更前记录恢复命令
4. Stage 7 Verify 用验收清单验证（无代码项目不需要测试套件）

## 与 vibe 协作（v2 新增，可选）
- vibe = 治理运行时（冻结需求/计划/执行闭环）；本技能 = 项目流程纪律（阶段/门禁/制品）
- 复杂任务模式: vibe 冻结需求与计划 → dev-pipeline-dsh 执行阶段门禁 → vibe 验证
- 制品不双轨：需求/计划由 vibe 产出时，本技能引用而非重写
- **vibe 不可用时**：走独立闭环模式——需求/计划由 Stage 1 / Stage 4 自行产出并落盘，STATUS 标注 `mode: standalone`，上述双轨条款不适用，流程照常走完

## 永不做
默删 / force-push / 密钥轮换 / 改 settings 无确认 / 跳门禁 / 无 approve 跨阶段

## 中止而非删除
用户中止项目时保留所有文件，仅切 STATUS 状态（aborted / paused）。禁止删除 aborted 项目。

## 进阶 (L2+ 推荐)
- 加载细节: 见 loading.md
- 换宿主 / 重新探测能力: 见 runtime-adapter.md
- 复杂任务: 委托子 agent → templates/subagent-prompts.md
- 上下文压缩: templates/state-preservation.md
