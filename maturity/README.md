# dev-pipeline Maturity 切换说明

> 动态加载机制：当前 maturity 决定加载哪份规则集。

## 当前 maturity 在哪看?
读 .dev/STATUS.md 的 Maturity 字段。没设置则用默认 L1。

## 切换方式(3 种)
### 1. 显式命令
- 切换到 L1  # 最小仪式,单人
- 切换到 L2  # 小组,加 PR review
- 切换到 L3  # 企业,加审计委员会

### 2. 隐式自动
agent 在 Step 0 检测：我一个人做 → L1；我们 5 人团队 → L2(需 confirm)；50 人企业有合规要求 → L3(需 confirm)。

### 3. 单阶段覆盖
项目默认 L1，但 Audit 阶段按 L3 严格审计 → 该阶段用 L3 规则，完成后切回默认并记决策。

## 切换流程
1. 读 maturity/L<新>-rules.md 拿新规则
2. 改 .dev/STATUS.md 的 Maturity 字段
3. 追加决策到 .dev/decision-log.md（原因 + 影响）
4. 告知用户切换完成

## 规则文件
- L1-rules.md (~376 tokens) - 单人/单兵
- L2-rules.md (~504 tokens) - 小组 2-10 人
- L3-rules.md (~874 tokens) - 企业 10+ 人,等效 C 严格版

> 口径: 中文 1 字 ≈ 1 token, ASCII 4 字符 ≈ 1 token, 保守估计(较 cl100k 偏高 5~15%)。
> v2 标注的 100/150/300 系字符粗估, 低估约 3 倍; v3 起改为实测值。

## L3 = C 效果?
是。L3 强制：必读所有 stage 契约、必用所有 template、必填所有 gate-report、必走 peer review、必跑变异测试、必开审计委员会。
唯一差别: 加载时机(L3 按需,C 启动即全塞)。L1/L2 项目大幅省 token。
