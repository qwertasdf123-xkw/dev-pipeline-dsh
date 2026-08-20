---
type: gate-report
stage:
created: {{timestamp}}
status: pending
---

# Gate Report — Stage {{stage}}

> 必须等人类 approve 才能进入下一阶段

## ✅ Completed
[本阶段产出的关键成果，链接到 spec / design / code 等]

## 📊 Evidence
[产出证据：测试报告链接、git commit、截图等]

## ❓ Open questions
[本阶段未决问题 / 阻塞]

## ⏸️ Awaiting
- [ ] approve —— 进入下一阶段
- [ ] modify —— 需要修改（请指明改什么）
- [ ] abort —— 中止本工作流

## DSH 门禁提交方式（v2）
1. 本文件写入 .dev/gate-report-NN.md
2. 用 ask_user_question 提问（header: Gate Report — Stage NN），选项:
   - approve（推荐）—— 进入下一阶段
   - modify —— 需要修改（用户注明改什么）
   - abort —— 中止本工作流
3. 等待用户选择；agent 不自行 approve

## Abort 选项联动
当 gate-report 选 abort 时，必须同步：
1. STATUS.md 切 status: aborted
2. decision-log.md 追加 abort 条目，引用本 gate-report 文件名
3. 当前阶段的 spec.md/design.md frontmatter 加 status: aborted-at-stage-{N}（N 为当前阶段号）
4. fallback: 若本 gate-report 文件尚未生成（abort 发生在 stage 中途），跳过第 2 步引用，改为在 decision-log 标注 关联 gate-report: 无（中途 abort）

---

agent 不会自己 approve，必须等显式信号。
