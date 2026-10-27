# L3 规则 — Enterprise

> 继承 L2 + 加审计委员会 / 变异测试 / SAST / 合规驱动。
> 等价于 C 严格版: 必读所有 stage,必用所有 template,必填所有 gate。

## 阶段契约(进入任一阶段前必读)
- 必须先读 stages/0X-*.md 全部内容
- 必须使用 templates/ 目录中的全部现存模板；阶段模板按阶段使用，STATUS / decision-log / gate-report 全程维护
- 不可跳读、不可总结、不可我觉得差不多

## 时间盒
| 阶段 | 时限 |
|------|------|
| Spec | 60+ min + 策略即代码校验 + PM+架构+Tech Lead 共著 |
| Design | 1-2 周 + 架构评审委员会 |
| Research | 数周 + tech radar 流程 |
| Plan | 1-2 天 |
| Setup | 数天 + 完整 IaC + sealed builds + SBOM + SLSA |
| Code | 多分支 + 受保护 main + 强制他审 + 职责分离 |
| Verify | 数天 + 变异测试 + 契约测试 + 策略即代码门槛 |
| Audit | 数天 + 部分自动化 + 独立审计委员会 |
| Deploy | 数天 + CAB + 金丝雀 + 自动回滚 + 渐进交付 + 不可变基础设施 |
| Observe | SLO 驱动 + on-call + 客户级 SLO |

## 制品要求
- Spec: 系统记录(Jira/Confluence/Linear)+ 策略即代码校验
- Design: 架构评审委员会签字 + ADR 强制
- Research: tech radar + ADR
- Plan: 跨团队依赖 + 资源分配
- Setup: 完整 IaC,sealed builds,签名制品,供应链安全(SLSA)
- Code: 受保护 main,他审强制,职责分离
- Verify: 变异 + 契约 + 策略即代码门槛
- Audit: SAST + SCA + 架构合规 + 策略即代码,人审只看例外
- Deploy: CAB + 金丝雀 + SLO 违约自动回滚 + 渐进交付 + 不可变基础设施
- Observe: SLO 平台 + on-call rotation + 客户级 SLO + 业务 outcome 关联

## 评审(多角色签字)
- Spec: PM + 架构 + Tech Lead 三方
- Design: 架构评审委员会
- Audit: 独立审计委员会
- Deploy: CAB(Change Advisory Board)
- 每个 Gate Report 多角色签字

## 自动化(必须)
- CI/CD 全自动,策略即代码,自动化 SAST/SCA,签名制品,自动金丝雀 + 自动回滚
- 必须: 变异测试 + contract testing; 强烈推荐: chaos engineering

## 文档
- docs-as-code + DRI per doc + SLA,自动 staleness detection
- 服务目录 + ADR + runbook 索引,弃用策略 + 强制下架

## 安全/Docs/PDCA/Compliance
- Security: 联邦化(产品/公司/云/供应链),独立 AppSec 团队
- Docs: 联邦化,DRI + SLA
- PDCA: PMO / Engineering Excellence 团队
- Compliance: 审计跟踪 / 数据分类 / 保留策略 / 访问审查

## 门禁(所有 P0/P1 必须解决)
- P0: 阻塞上线,0 容忍; P1: 必须解决或豁免; P2: 记录到 PDCA backlog
- SAST/SCA 自动扫描必须通过; SBOM 必须生成; 凭据轮换 90 天周期

## 永不做
- 改 settings.json/.env: 永不; force-push: 永不; 跳过 audit/review/变异测试: 永不

## 切换提示
- L3 是工业级上限,没有 L4
- 如果流程过重,审视哪些 gate 可自动化而非裁剪
