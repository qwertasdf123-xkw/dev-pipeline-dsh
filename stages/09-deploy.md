# Stage 09: Deploy 部署

> 阶段目标: 按 runbook 部署，可回滚

## 触发
`上线 / 部署`

## agent 做
1. 写/更新 runbook
2. 执行部署（按用户授权）
3. 验证上线后健康

## 人类做
1. 授权部署动作

## Done 标准
- 部署完成且健康
- runbook 存在
- 回滚方案就绪

## 时间盒
- L1: 15 min；L2: +变更工单+灰度

## 退出条件
`Gate Report approve → Stage 10 Observe`

## 安全边界
- AI 永不做: 未授权部署/生产环境凭据操作
