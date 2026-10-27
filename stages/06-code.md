# Stage 06: Code 编码

> 阶段目标: 按 Plan 实现代码，单元测试同步写

## 触发
`开工 / 编码`

## agent 做
1. 按 plan.md 任务图执行
2. 每完成一个子任务: commit + 跑测试，并用宿主步骤清单能力（C8 槽）更新进度
3. 写单测（与实现同步）
4. 每 90 分钟一个 Build 周期，强制 break + 状态汇报
5. **Security 线程**: 每子门禁做威胁建模
6. **Docs 线程**: 行为变更处内联更新文档

## 人类做
1. Code review（自然在子门禁处看）
2. 解 P1 阻塞
3. 调整任务顺序（如有需要）

## Done 标准
- 所有任务完成
- 保存/提交时自动化测试全绿
- Security 签 + Docs 内联更新
- decision-log 已追加
- Gate Report 等 approve

## 时间盒
- L1: 每 90 分钟一个 Build 周期
- L2: 配合 PR review 节奏（PR SLA 24h）
- L3: 多分支 + 受保护 main + 强制他审

## 退出条件
`Gate Report approve → Stage 7 Verify`

## 安全边界
**agent 永不做**:
- git push（除非显式要求）
- force-push
- 删文件
- 改 .env / 密钥文件
- 升级依赖主版本（需先确认）
