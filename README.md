# dev-pipeline-dsh 使用说明 (v2)

## 30 秒上手
1. agent 在项目根目录创建 .dev/STATUS.md（首次自动引导）
2. 用触发短语启动流程
3. 每阶段结束 agent 用 ask_user_question 给出门禁报告，选 approve 才进下一步

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
- 重新开始 → 当前项目改名为 .archived-{date}/，新建 STATUS
- 我想改回之前的决定 → 决策推翻流程（Supersedes），并追问 spec/design/plan 是否级联更新
- 长调研 / 并行调研 → 派多个 sub-agent（见 templates/subagent-prompts.md）

## 切换成熟度
- 切换到 L1 / 切换到 L2 / 切换到 L3

## 与 vibe 的协作
- vibe 冻结需求/计划，本技能执行阶段门禁，vibe 验证 —— 制品不双轨
- vibe 通过 skill roots（E:\dsh-ecosystem\skills）可发现本技能（name: dev-pipeline-dsh）
- DSH 用户级安装位置：C:\Users\Administrator\.dsh\skills\dev-pipeline-dsh（所有项目/会话可见）

## 与 v1（dev-pipeline）的区别
1. frontmatter 改为 DSH 原生字段（name/description/whenToUse/metadata），自定义字段全部收入 metadata，vibe 兼容信息同步保留
2. 门禁改 ask_user_question 双轨（对话 + 文件）
3. 新增 goal 双轨、存量改造路径、vibe 协作边界
4. Stage 7 Test → Verify（验收清单泛化）
