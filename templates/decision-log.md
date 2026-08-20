# 决策日志

> 每门禁退出前追加一条
> 记录为什么这么做，方便后续复盘
> 决策被推翻时，新决策填 Supersedes，旧决策不删但加 SUPERSEDED 标记

## 格式
每条决策：
- **时间**:
- **阶段**:
- **决策**:
- **原因**:
- **替代方案**:
- **影响范围**:
- **Supersedes**: (可选) 链接到被推翻的旧决策条目标题和行号

## Abort 决策必须包含
- 终止阶段（Stage X）
- 已完成产物清单（spec.md/design.md/...）
- 重启入口（重新开始从哪个阶段）
- 关联 gate-report（如有）

## 覆写决策格式（Supersedes 链）
旧决策条目（在原位置加 SUPERSEDED 标记，不删）：

```markdown
- **时间**: 2026-06-15
- **阶段**: Stage 2
- **决策**: 选用 SQLite（轻量、单文件）
- **原因**: 单文件部署、零运维
- **替代方案**: PostgreSQL / MySQL
- **影响范围**: 数据访问层、迁移脚本
- **状态**: SUPERSEDED by L57 (2026-06-23 - 改 PostgreSQL)
```

新决策条目（追加到下方）：

```markdown
- **时间**: 2026-06-23
- **阶段**: Stage 6 (覆写 Stage 2 决策)
- **决策**: 改用 PostgreSQL
- **原因**: 并发测试发现 SQLite 写入锁竞争严重
- **替代方案**: 继续用 SQLite（已否决）/ SQLite WAL 模式（未验证）/ MySQL
- **影响范围**: Stage 5 Setup 安装脚本、Stage 6 Code 数据访问层、Stage 7 Verify 验证夹具；级联更新 design.md 数据库章节
- **Supersedes**: L42 "Stage 2 - 选用 SQLite"
```

## Abort 条目格式

```markdown
- **时间**: 2026-06-23
- **阶段**: Stage 2 (Design)
- **决策**: Abort 项目
- **原因**: 用户显式终止（算了不做了）
- **替代方案**: -
- **影响范围**: 终止 Stage 3+ 推进
- **已完成产物**: spec.md (Stage 1), design.md (Stage 2)
- **重启入口**: 从 Stage 1 Spec 重新启动
- **关联 gate-report**: gate-report-02.md (若存在)
- **Supersedes**: -
```

## 阶段字段填法
- 正常决策: Stage N (阶段名) 例：Stage 2 (Design)
- 覆写其他阶段决策: Stage M (覆写 Stage N 决策)
- Abort 决策: Stage N (阶段名)
- Supersedes 字段格式: L{行号} "{决策标题}" 或 L{行号} {阶段} - {决策摘要}

---

<!-- 新决策加在下方，按时间倒序 -->
