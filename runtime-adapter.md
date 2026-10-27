# 运行时适配层 (Runtime Adapter)

> 本 skill 原生为 DSH(DeepSeek Harness) 编写。移植到其他 agent 宿主时，**能力语义必须保持等价**，但具体工具名可以换。
> 本文件是唯一的"宿主差异收敛点"——SKILL.md 与各 stage 只谈能力槽，不谈具体工具。

## 0. 一条铁律

> **门禁语义不可降级，工具实现可以降级。**

"人 approve 才能推进"是这个 skill 的**全部价值所在**。一个没有 `ask_user_question` 的宿主，必须退化成"文本三选项 + 显式停下等回复"，而**绝不能**退化成"agent 自己判断可以继续"。

宁可停下报错，不可假装通过。

---

## 1. 能力槽（12 个）

所有宿主差异都收敛到这 12 个槽。stage 与模板只引用槽名。

| 槽 | 能力 | 语义要求 | DSH 原生 | 通用实现 |
|---|---|---|---|---|
| `C1` | 读文件 | 能读任意工作区文件 | `read` | 文件读工具 |
| `C2` | 写/改文件 | 能写工作区内文件 | `write` / `edit` | 文件写工具 |
| `C3` | 执行命令 | 能跑 shell，含后台执行 | `pwsh` | shell 工具（POSIX 用 `bash`） |
| `C4` | 后台任务 | 能起长任务并事后取结果 | `pwsh run_in_background` + `job_output` | 后台任务 + 结果查询 |
| `C5` | 委托子 agent | 能派独立子任务并收回结果 | `subagent` | 子 agent 工具 |
| `C6` | 结构化提问 | 能向用户抛多选项并等选择 | `ask_user_question` | 文本选项 + 显式等待 |
| `C7` | 跨轮次目标 | 能记录跨会话目标 | `create_goal` / `update_goal` | 目标/待办工具 |
| `C8` | 步骤清单 | 能显示执行态待办 | `todo_write` | 待办清单工具 |
| `C9` | 联网检索 | 能查外部资料 | `web_search` | 检索工具 |
| `C10` | 加载关联 skill | 能按需加载别的 skill | `skill` | skill 加载工具 |
| `C11` | 大规模编排 | 能跑多 agent 编排 | `workflow` | 编排/团队工具（**可选**） |
| `C12` | 治理运行时 | 需求冻结/计划冻结/验证 | `vibe` | **可选**，缺失时按 §4.3 |

---

## 2. 宿主映射速查

### 2.1 DSH（原生，无降级）
`C1=read` `C2=write/edit` `C3=pwsh` `C4=pwsh run_in_background + job_output/job_kill`
`C5=subagent` `C6=ask_user_question` `C7=create_goal/update_goal/get_goal`
`C8=todo_write` `C9=web_search` `C10=skill` `C11=workflow` `C12=vibe`

### 2.2 Mavis / MiniMax Agent
`C1=read` `C2=write/edit` `C3=bash` `C4=bash(run_in_background) + task_output/task_stop`
`C5=task` `C6=chat_reply`（文本三选项 + 显式等待）`C7=self_reminder` `C8=todowrite`
`C9=web_search` `C10=skill` `C11=team` `C12=—`

### 2.3 Claude Code
`C1=Read` `C2=Write/Edit` `C3=Bash` `C4=Bash(run_in_background)` `C5=Task`
`C6=AskUserQuestion` `C7=TodoWrite` `C8=TodoWrite` `C9=WebSearch` `C10=Skill` `C11=—` `C12=—`

### 2.4 通用降级（只认得"文件 + shell + 对话"的最小宿主）
`C1=文件读` `C2=文件写` `C3=shell` `C4=同步执行（无后台则串行等待）`
`C5=无 → 自己做，记录为"未独立复核"` `C6=文本选项` `C7=无 → 写进 STATUS.md`
`C8=无 → 写进 plan.md` `C9=无 → 跳过调研或让人提供` `C10=无` `C11=无` `C12=无`

---

## 3. 能力探测协议（首次激活时跑一次）

**什么时候跑**：本 skill 第一次在一个项目里激活时（loading.md 加载完立刻跑），或用户显式说"重新探测环境"。

**怎么跑**：把当前宿主可用工具逐个对照 §1 的 12 个槽，产出一份映射。**不要真的去探测文件系统的能力**——工具清单就是事实来源。

**产物**：`.dev/runtime.json`

```json
{
  "host": "mavis",
  "probed_at": "2026-10-22T22:40:00Z",
  "slots": {
    "C1": { "impl": "read", "status": "ok" },
    "C2": { "impl": "write/edit", "status": "ok" },
    "C3": { "impl": "bash", "status": "ok", "note": "POSIX shell" },
    "C4": { "impl": "bash run_in_background + task_output", "status": "ok" },
    "C5": { "impl": "task", "status": "ok" },
    "C6": { "impl": "chat_reply", "status": "degraded", "note": "无结构化多选，退化为文本三选项" },
    "C7": { "impl": "self_reminder", "status": "degraded" },
    "C8": { "impl": "todowrite", "status": "ok" },
    "C9": { "impl": "web_search", "status": "ok" },
    "C10": { "impl": "skill", "status": "ok" },
    "C11": { "impl": "team", "status": "ok" },
    "C12": { "impl": null, "status": "missing", "note": "vibe 未安装" }
  }
}
```

**status 取值**：`ok`（原生等价）｜`degraded`（降级但语义等价，见 §4.2）｜`missing`（缺失，见 §4.1 / §4.3）

**记录到 STATUS**：把 `host` 与降级项摘要写进 `.dev/STATUS.md` 的上下文段，让人一眼看出这次跑在什么环境上。

**runtime.json 的生命周期**：它属于"落盘"类产物——上下文压缩时**必须保留**（它不在 STATUS / decision-log 里，丢了就得重新探测）。

---

## 4. 降级规则

### 4.1 不可降级项：缺失即 STOP

以下 3 项是本 skill 的存在理由，**没有等价实现就不启动流水线**：

| 保障 | 依赖槽 | 缺失时 |
|---|---|---|
| 门禁由人确认 | `C6` | STOP（见 §4.3） |
| 阶段产物落盘 | `C1`+`C2` | STOP |
| 决策留痕 | `C2` | STOP |

**STOP 的正确姿势**（不要静默降级，不要自己批）：

```
[环境不足] dev-pipeline-dsh 需要 <能力>，当前宿主不可用。
可替代方案：
  1. <方案 A>
  2. <方案 B>
等你的指示再继续。
```

### 4.2 可降级项：必须语义等价

| 槽 | 降级形态 | 等价性要求 |
|---|---|---|
| `C6` | 文本三选项 | **必须显式停下**，等下一条用户消息；不得在同一轮继续推进 |
| `C4` | 同步执行 | 长任务可串行等待，但不得丢失结果 |
| `C5` | 自己复核 | 必须在 gate-report 标注"**未独立复核**"，不能冒充独立验证 |
| `C7` | 写进 STATUS.md | 目标可追溯即可 |
| `C8` | 写进 plan.md | 步骤可追溯即可 |
| `C9` | 无 | 跳过调研必须**在 gate-report 明说**，不能假装调研过 |
| `C10`/`C11`/`C12` | 不用 | 见 §4.3 |

### 4.3 可选能力的缺失处理

- **`C11` 大规模编排缺失** → 本 skill 退化为单 agent 串行执行流水线。**不阻塞**。
- **`C12` vibe 缺失** → 走"**独立闭环模式**"：需求/计划由本 skill 自己在 Stage 1/Stage 4 产出并落盘，不再引用 vibe 的冻结产物。§与 vibe 协作 里的双轨条款全部不适用。**不阻塞**，但要在 STATUS 里标注 `mode: standalone`。
- **`C10` skill 加载缺失** → 本 skill 单独运行，路由与委托能力不可用。**不阻塞**。

---

## 5. 门禁在降级宿主下的正确行为（最重要）

`C6` 只有文本形态时，一次完整的门禁交互长这样：

**agent 的回合**（到这里必须停）：

```
⏸️ Gate Report — Stage 1 (Spec)
已完成：spec.md（8 节齐全，验收标准 6 条可测）
证据：.dev/spec.md
未决：验收标准第 4 条需你确认"是否包含导出功能"

请选择：
  A. approve（推荐）—— 进入 Stage 2 Design
  B. modify —— 需要修改（请指明改什么）
  C. abort —— 中止本工作流
```

**然后停下。** 不写下一阶段内容，不预设选择，不"按推荐项走"。

**绝对禁止**（即使只差一个字也不许）：
- 把"用户没有反对"当作 approve
- 复用上一阶段的 approve 充当本阶段的
- 在同一轮里既发门禁又继续写下一阶段产物
- 在 gate-report 里勾选 `[x] approve` 而没有用户明示

**用户的回复**必须是明确的 `approve` / `modify` / `abort`（或 A/B/C、或中文"通过/改/停"）。收到后：
1. 把选择写进 `.dev/gate-report-NN.md` 的 status 字段
2. 追加一条 decision-log
3. 更新 STATUS.md
4. 才推进下一阶段

---

## 6. 跨平台路径与沙箱

**路径表达**：一律用**相对工作区根**的路径，不用盘符绝对路径。

| 概念 | 通用写法 | DSH/Windows 实际 | POSIX 实际 |
|---|---|---|---|
| 项目状态目录 | `.dev/` | `.dev\` | `.dev/` |
| 技能安装位置 | `<skills-root>/<skill-name>/` | `%USERPROFILE%\.dsh\skills\...` | `~/.dsh/skills/...` |
| 外部技能根 | `<skills-root>` | `E:\dsh-ecosystem\skills` | `~/dsh-ecosystem/skills` |

**工作区约束**：默认只写工作区内。越区写入需要显式授权 + 一次一令 + 说明理由。授权边界写在 STATUS.md。

**Shell 差异**：DSH 用 `pwsh`(PowerShell 5.1，ConstrainedLanguage 模式)；其他宿主用宿主默认 shell。**不要把 PowerShell 语法写进 stage 文件**——stage 只说"执行 X"，由 §1 的 `C3` 决定用什么执行。stage 文件里出现 `pwsh` 一律视为待修的宿主绑定。

---

## 7. 宿主专属扩展（不影响通用路径）

`vibe`（治理运行时，槽 `C12`）是 DSH 生态的外部依赖，不是本 skill 的一部分。

- 本 skill **不依赖** vibe 才能运行；vibe 在时是"协作增强"，不在时走 §4.3 的独立闭环模式。
- 不要在通用路径里写死 vibe 的安装位置或发现方式。
- 若未来 vibe 开源或提供标准发现接口，在本文件 §2 增加一节映射即可，**不要**改动 stage 文件。

---

## 8. 自检清单（每次改动本 skill 后跑）

- [ ] stages/ 与 templates/ 中**没有**出现具体宿主工具名（`pwsh` / `ask_user_question` / `job_output` / `create_goal`）
- [ ] SKILL.md 能力槽表里出现的工具名**仅限 "DSH 原生" 列**，"通用实现"列不得写具体工具
- [ ] stage 文件中**没有**出现盘符绝对路径
- [ ] 门禁语义在 §5 的三条禁止项上没有被弱化
- [ ] `runtime.json` 被列入 state-preservation 的"落盘"清单
- [ ] 预算表数字与 `scripts/measure_tokens.py` 实测一致（误差 ≤ 15%）
- [ ] `C12` 缺失时流程仍可端到端跑完
