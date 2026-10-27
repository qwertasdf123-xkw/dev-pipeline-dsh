# dev-pipeline-dsh 使用说明 (v3.0.1)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/qwertasdf123-xkw/dev-pipeline-dsh)](https://github.com/qwertasdf123-xkw/dev-pipeline-dsh)
[![GitHub repo](https://img.shields.io/badge/GitHub-qwertasdf123--xkw%2Fdev--pipeline--dsh-blue)](https://github.com/qwertasdf123-xkw/dev-pipeline-dsh)

> **v3 = 可移植版**。本 skill 原生为 DSH(DeepSeek Harness) 编写，v3 起不再绑定具体宿主：
> 工具依赖收敛为 12 个**能力槽**（见 `runtime-adapter.md`），首次激活时探测宿主并把映射写入
> `.dev/runtime.json`，之后按槽取工具。**门禁语义不随工具降级**——缺能力就停下报告，绝不自批。

## 30 秒上手
1. agent 在项目根目录创建 `.dev/STATUS.md`（首次自动引导）
2. 首次激活做一次**能力探测** → 写入 `.dev/runtime.json`（换宿主时才需重探）
3. 用触发短语启动流程
4. 每阶段结束 agent 给出 Gate Report 三选项（approve / modify / abort），**选 approve 才进下一步**

## 触发短语速查
| 你想说 | 阶段 |
|--------|------|
| 我有个想法 / 记一下灵感 | Step 0 |
| 我想做 X / 新需求 | Step 1 |
| 设计 / 架构 | Step 2 |
| 调研 / 查资料 | Step 3 |
| 计划 / 拆任务 | Step 4 |
| 搭环境 / 初始化 / 盘点现状 | Step 5 |
| 开工 / 编码 | Step 6 |
| 验证 / 跑测试 | Step 7 |
| 审计 / 上线前检查 | Step 8 |
| 上线 / 部署 | Step 9 |
| 观察 / 看数据 | Step 10 |

## 控制流触发（中止 / 重启 / 推翻 / 并行调研）
- 不做了 / abort / 算了 → STATUS 切 aborted，保留所有文件，联动 gate-report §Abort
- 重新开始 → 当前项目改名为 `.archived-{date}/`，新建 STATUS
- 我想改回之前的决定 → 决策推翻流程（Supersedes），并追问 spec/design/plan 是否级联更新
- 长调研 / 并行调研 → 派多个子 agent（见 `templates/subagent-prompts.md`）

## 切换成熟度
- 切换到 L1 / 切换到 L2 / 切换到 L3

## 运行环境（跨平台）
| 概念 | 通用写法 | DSH/Windows | POSIX |
|---|---|---|---|
| 项目状态目录 | `.dev/` | `.dev\` | `.dev/` |
| 技能安装位置 | `<skills-root>/dev-pipeline-dsh/` | `%USERPROFILE%\.dsh\skills\dev-pipeline-dsh` | `~/.dsh/skills/dev-pipeline-dsh` |
| 外部技能根 | `<skills-root>` | `E:\dsh-ecosystem\skills` | `~/dsh-ecosystem/skills` |

**已验证宿主**：DSH（原生）、Mavis / MiniMax Agent、Claude Code。通用降级（只认得文件+shell+对话）也支持。
完整映射表见 `runtime-adapter.md` §2。

## 与 vibe 的协作（可选）
- vibe = 治理运行时（冻结需求/计划/执行闭环）；本 skill = 项目流程纪律（阶段/门禁/制品）
- 复杂任务模式: vibe 冻结需求与计划 → dev-pipeline-dsh 执行阶段门禁 → vibe 验证 —— 制品不双轨
- vibe 通过 skill roots 可发现本技能（name: `dev-pipeline-dsh`），发现方式随宿主而定
- **vibe 不可用时**（多数宿主如此）→ 自动走**独立闭环模式**：需求/计划由 Stage 1 / Stage 4 自行产出并落盘，STATUS 标注 `mode: standalone`，流程照常走完，**不阻塞**

## 与 v2 的区别
1. **宿主可移植**：新增 `runtime-adapter.md`（12 能力槽 + 探测协议 + 降级规则 + 跨平台路径）；SKILL.md 的工具表从「DSH 工具映射」改为「能力槽映射」
2. **门禁语义加固**：新增「文本三选项降级协议」与「状态回写」流程；明确 3 条禁止项（沉默不算 approve、不得复用上一阶段 approve、不得同轮既提问又推进）
3. **工具解绑**：stage / 模板中不再出现 `pwsh` / `ask_user_question` / `job_output` / `create_goal` 等宿主专名
4. **预算修正**：v2 的 token 数字（SKILL ~260、L1 总 ~1000、L2 +200 / L3 +600）系粗估且低估 2.5~3 倍，v3 改为实测（SKILL 1945、L1 稳态 ~3600、L3 增量 +2830 起）
5. **能力探测产物**：新增 `.dev/runtime.json`，纳入压缩保留清单
6. 其余 v2 特性（goal 双轨、存量改造路径、vibe 协作边界、Stage 7 Verify 泛化）保持不变
