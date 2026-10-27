# dev-pipeline-dsh 加载规则 (v3.0.1)

## 何时读哪个文件
| 任务 | 文件 |
|------|------|
| 第一次激活 | 本文件 (你正在读) |
| 能力探测（首次 / 宿主变了 / 有槽缺失） | runtime-adapter.md |
| L1 默认 | maturity/L1-rules.md |
| 切 L2/L3 | maturity/L{2,3}-rules.md + maturity/README.md |
| 委托子 agent | templates/subagent-prompts.md |
| 压缩/恢复 | templates/state-preservation.md |
| 写 spec/design/plan/... | templates/<name>.md |
| Stage X 细节 | stages/0X-*.md |

**能力探测只做一次**：探测结果写进 `.dev/runtime.json`。后续会话若 `runtime.json` 里的 `host` 与当前宿主一致，直接用它，**不必再读 runtime-adapter.md**。仅当 runtime.json 缺失、宿主不匹配、或某槽 `status=missing` 时才重读 adapter。

## 门禁流程（宿主无关）
1. 阶段完成 → 写 gate-report-NN.md + 更新 STATUS.md
2. 用宿主的多选能力提问: [approve（推荐）| modify | abort]，附 Gate Report 摘要
3. 宿主无多选能力 → 文本三选项 + **显式停下等下一条回复**（runtime-adapter.md §5）
4. approve → 推进；modify → 按反馈修订后重新出报告；abort → 走 Abort 联动
5. 决策记 decision-log（含 Supersedes）

**agent 不自行 approve。** 详见 runtime-adapter.md §5 的三条禁止项。

## 主 context 必保（实测口径）

口径：中文 1 字 ≈ 1 token、ASCII 4 字符 ≈ 1 token，**保守估计**（较 cl100k 偏高 5~15%，用于预算规划偏安全）。测量脚本 `scripts/measure_tokens.py` 可复算。

| 内容 | 模板全长 | 实际读入 | 说明 |
|------|----------|----------|------|
| SKILL.md（本入口） | 1932 | 1932 | 常驻 |
| loading.md（本文件） | ~1200 | ~1200 | 首次激活常驻 |
| maturity/L1-rules.md | 376 | 376 | L1 常驻 |
| .dev/STATUS.md | 290 | ~200 | 项目实际状态（不含模板说明段） |
| .dev/decision-log.md | 672 | ~250 | **只读前 3 条**，不全量读 |
| .dev/runtime.json | ~150 | ~150 | 能力映射缓存 |
| **L1 稳态总** | — | **~4100** | 不含 adapter |
| **L1 首次激活总** | — | **~7000** | 含一次性能力探测（adapter 2893） |

**成熟度切换的边际成本**（相对 L1）：

| 切换 | 增量 | 说明 |
|---|---|---|
| L1 → L2 | +128 | 替换 L1-rules 为 L2-rules(504) |
| L1 → L3 | +2935 起 | L3-rules(874) + 11 份 stage 契约(2437) + templates 按需 |

> v2 曾标注 "L1 总 ~1000"、"L2 +200 / L3 +600"，系按字符数粗估且低估约 2.5~3 倍；v3 起改为实测值。

## 11 阶段 offload 策略
| 阶段 | 主读 | 委托子 agent 干 |
|------|------|-------------|
| 0 Inspiration | L1 rules | 素材扫描 |
| 1 Spec | L1 + spec.md | 法规/标准研究 |
| 2 Design | L1 + design.md | 候选架构 |
| 3 Research | L1 | 库/PoC 调研 |
| 4 Plan | L1 | 任务拆解 |
| 5 Setup | L1 | 环境盘点/脚手架 |
| 6 Code | L1 + spec | 模块代码 |
| 7 Verify | L1 + spec | 验收清单执行 |
| 8 Audit | L1 + spec | 安全/性能扫描 |
| 9 Deploy | L1 | CI/CD |
| 10 Observe | L1 | 监控数据 |

## 触发时机
| 触发 | 动作 |
|------|------|
| 走 dev-pipeline / 用流水线 | 读 SKILL.md → loading.md → 能力探测 |
| spec / plan / audit 等阶段词 | 读 SKILL.md + L1 rules + 当前 stage |
| 切换到 L2/L3 | 读 maturity/README.md → L{2,3}-rules.md |
| 长任务 (>3 文件) | 委托子 agent (见 subagent-prompts.md) |
| 长调研 / 并行调研 | 派多个子 agent (§VERIFIER) |
| Stage 完成 | 写 STATUS + decision-log, 清子 agent 产物 |
| context 50% | 压缩: 留 STATUS/decision-log/runtime.json, 丢子 agent 原始输出 |

## 压缩前检查 (7 项)
> 本清单 = **压缩前**的前置条件；压缩**后**的收尾动作见 templates/state-preservation.md §压缩后必做。两者不是一回事。

1. STATUS.md 已更新
2. decision-log 已追加
3. gate-report 已存档
4. 所有产物已落盘 (spec/design/plan/... **+ runtime.json** 能力映射)
5. 子 agent 输出摘要已保存（原始输出可丢）
6. 当前 stage 入口可恢复 (重启命令已记录)
7. 压缩决策已记 decision-log
