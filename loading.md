# dev-pipeline-dsh 加载规则 (v2)

## 何时读哪个文件
| 任务 | 文件 |
|------|------|
| 第一次激活 | 本文件 (你正在读) |
| L1 默认 | maturity/L1-rules.md |
| 切 L2/L3 | maturity/L{2,3}-rules.md + maturity/README.md |
| 调 sub-agent | templates/subagent-prompts.md |
| 压缩/恢复 | templates/state-preservation.md |
| 写 spec/design/plan/... | templates/<name>.md |
| Stage X 细节 | stages/0X-*.md |

## 门禁流程（ask_user_question 版）
1. 阶段完成 → 写 gate-report-NN.md + 更新 STATUS.md
2. ask_user_question 提问: [approve（推荐）| modify | abort]，附 Gate Report 摘要
3. approve → 推进；modify → 按反馈修订后重新出报告；abort → 走 Abort 联动
4. 决策记 decision-log（含 Supersedes）

## 主 context 必保 (按 token 计)
| 内容 | tokens |
|------|--------|
| SKILL.md (本入口) | ~260 |
| loading.md (首次) | ~320 |
| maturity/L1-rules.md | ~200 |
| STATUS.md (项目) | ~120 |
| decision-log (前 3 条) | ~100 |
| **L1 项目启动总** | **~1000** |

L2 +200, L3 +600 (按需,不同时加载)。

## 11 阶段 offload 策略
| 阶段 | 主读 | subagent 干 |
|------|------|-------------|
| 0 Inspiration | L1 rules | 素材扫描 |
| 1 Spec | L1 + spec.md | 法规/标准研究 |
| 2 Design | L1 + design.md | 候选架构 |
| 3 Research | L1 | 库/PoC 调研 |
| 4 Plan | L1 | 任务拆解 |
| 5 Setup | L1 | 环境盘点/脚手架 |
| 6 Code | L1 + spec | 模块代码 |
| 7 Verify | L1 | 验收清单执行 |
| 8 Audit | L1 + spec | 安全/性能扫描 |
| 9 Deploy | L1 | CI/CD |
| 10 Observe | L1 | 监控数据 |

## 触发时机
| 触发 | 动作 |
|------|------|
| 走 dev-pipeline / 用流水线 | 读 SKILL.md → loading.md |
| spec / plan / audit 等阶段词 | 读 SKILL.md + L1 rules + 当前 stage |
| 切换到 L2/L3 | 读 maturity/README.md → L{2,3}-rules.md |
| 长任务 (>3 文件) | 调 subagent (看 subagent-prompts.md) |
| 长调研 / 并行调研 | 派多个 subagent (§VERIFIER) |
| Stage 完成 | 写 STATUS + decision-log, 清 subagent |
| context 50% | 压缩: 留 STATUS/decision-log, 丢 subagent output |

## 压缩前检查 (7 项)
1. STATUS.md 已更新
2. decision-log 已追加
3. gate-report 已存档
4. 所有产物已落盘 (spec/design/plan/...)
5. subagent output 摘要已保存
6. 当前 stage 入口可恢复 (重启命令已记录)
7. 压缩决策已记 decision-log
