# .agent-state.json 使用指南

## 概述

`.agent-state.json` 是 Resumable Subagents 机制的状态记录文件，用于在同一集内保持 agent 的上下文连续性。

**重要变更**：从项目全局配置改为剧本级别配置，每个剧本有独立的 agent state 文件。

## 文件位置

```
project/
└── outputs/
    ├── {剧本名1}/
    │   ├── .agent-state.json    # 剧本1的 agent state
    │   ├── analysis/
    │   ├── scripts/
    │   └── ...
    └── {剧本名2}/
        ├── .agent-state.json    # 剧本2的 agent state
        ├── analysis/
        ├── scripts/
        └── ...
```

**优势**：
- 不同剧本之间的 agent 上下文完全隔离
- 可以并行处理多个剧本
- 每个剧本有独立的 session 管理
- 避免剧本之间的上下文混淆

## 文件格式

```json
{
  "knowledge-curator": "",
  "novel-analyzer": "",
  "episode-architect": "",
  "script-writer": "",
  "review-director": "",
  "continuity-recorder": "",
  "storyboard-director": "",
  "storyboard-artist": "",
  "art-designer": "",
  "animator": ""
}
```

## 工作原理

### 目的

确保每个 subagent 的上下文连续，避免重复理解和丢失信息。

### 作用域

- **同一集内有效**：在处理同一集（如 ep01）时，agent ID 保持不变
- **跨集重置**：进入新一集（如 ep02）时，清空所有 agentId

### 为什么需要这个机制？

**问题**：
- 每次调用 agent 都创建新实例，会丢失之前的上下文
- Agent 需要重新理解剧本、重新分析需求
- 浪费 token，降低效率

**解决方案**：
- 首次调用 agent 时，记录返回的 agentId
- 后续调用同一个 agent 时，使用 resume 参数恢复
- Agent 继续之前对话的完整上下文

## 使用流程

### 场景 1：处理第 1 集（ep01）

#### 步骤 1：首次调用 agent

```bash
# 用户执行
~write 1
```

**Orchestrator 行为**：
1. 检查 `outputs/{剧本名}/.agent-state.json` 中 `script-writer` 的值
2. 发现为空字符串（首次调用）或文件不存在
3. 正常调用 agent：
   ```
   Use the script-writer agent to write episode 1
   ```
4. Agent 返回 agentId：`"abc123"`
5. 更新 `outputs/{剧本名}/.agent-state.json`：
   ```json
   {
     "script-writer": "abc123",
     ...
   }
   ```

#### 步骤 2：审核失败，需要修改

```bash
# 审核返回 FAIL
```

**Orchestrator 行为**：
1. 检查 `outputs/{剧本名}/.agent-state.json` 中 `script-writer` 的值
2. 发现有值：`"abc123"`（之前调用过）
3. 使用 resume 参数恢复 agent：
   ```
   Resume agent abc123 and revise the script based on review feedback
   ```
4. Agent 继续之前的上下文，知道之前写了什么
5. agentId 保持不变：`"abc123"`

#### 步骤 3：继续处理同一集的其他任务

```bash
# 用户执行
~storyboard-film 1
```

**Orchestrator 行为**：
1. 首次调用 `storyboard-artist`：记录 agentId
2. 调用 `storyboard-director` 审核：记录 agentId
3. 如果审核 FAIL，resume `storyboard-artist` 修改
4. 所有 agent 在同一集内保持上下文连续

### 场景 2：跨集处理（从 ep01 到 ep02）

#### 步骤 1：完成 ep01

```json
// outputs/{剧本名}/.agent-state.json 当前状态
{
  "script-writer": "abc123",
  "storyboard-artist": "def456",
  "storyboard-director": "ghi789",
  ...
}
```

#### 步骤 2：开始 ep02

```bash
# 用户执行
~write 2
```

**Orchestrator 行为**：
1. 检测到跨集（从 ep01 到 ep02）
2. **清空 `outputs/{剧本名}/.agent-state.json`**：
   ```json
   {
     "script-writer": "",
     "storyboard-artist": "",
     "storyboard-director": "",
     ...
   }
   ```
3. 所有 agent 重新创建，不再 resume ep01 的上下文
4. 避免多集累积导致上下文窗口溢出

#### 步骤 3：处理 ep02

```bash
# 首次调用 script-writer for ep02
```

**Orchestrator 行为**：
1. 发现 `script-writer` 为空（已重置）
2. 正常调用 agent（不 resume）
3. 记录新的 agentId：`"xyz999"`
4. 后续在 ep02 内继续 resume `"xyz999"`

## 调用规则总结

| 场景 | 行为 | 说明 |
|------|------|------|
| 同一集内首次调用 | 正常调用 agent | 记录返回的 agentId |
| 同一集内后续调用 | Resume agent <agentId> | 继续之前的上下文 |
| 跨集时 | 清空所有 agentId | 避免上下文窗口溢出 |

## 实现示例

### Orchestrator 伪代码

```python
def call_agent(agent_name, task, episode_number, script_name):
    # 确定 agent state 文件路径
    agent_state_path = f"outputs/{script_name}/.agent-state.json"

    # 检查是否跨集
    if current_episode != episode_number:
        reset_agent_state(script_name)
        current_episode = episode_number

    # 读取 agent state
    agent_state = read_json(agent_state_path)
    agent_id = agent_state.get(agent_name, "")

    if agent_id:
        # Resume 已有 agent
        result = resume_agent(agent_id, task)
    else:
        # 首次调用，创建新 agent
        result = create_agent(agent_name, task)
        agent_id = result.agent_id

        # 记录 agentId
        agent_state[agent_name] = agent_id
        write_json(agent_state_path, agent_state)

    return result

def reset_agent_state(script_name):
    """跨集时重置所有 agent state"""
    agent_state_path = f"outputs/{script_name}/.agent-state.json"
    agent_state = {
        "knowledge-curator": "",
        "novel-analyzer": "",
        "episode-architect": "",
        "script-writer": "",
        "review-director": "",
        "continuity-recorder": "",
        "storyboard-director": "",
        "storyboard-artist": "",
        "art-designer": "",
        "animator": ""
    }
    write_json(agent_state_path, agent_state)
```

## 优势

### 1. 上下文连续性

**没有 resume 机制**：
```
调用 1: "写 ep01"
  → Agent A 创建，写剧本

调用 2: "修改 ep01"
  → Agent B 创建（新实例）
  → 不知道之前写了什么
  → 需要重新读取剧本
  → 浪费 token
```

**有 resume 机制**：
```
调用 1: "写 ep01"
  → Agent A 创建，写剧本
  → 记录 agentId: "abc123"

调用 2: "修改 ep01"
  → Resume Agent A (abc123)
  → 知道之前写了什么
  → 直接修改
  → 节省 token
```

### 2. 避免上下文窗口溢出

**跨集重置**：
- ep01 的上下文不会累积到 ep02
- 每集都是新的开始
- 避免上下文窗口溢出

### 3. 提高效率

- 减少重复理解
- 减少重复读取文件
- 减少 token 消耗
- 提高响应速度

## 注意事项

### 1. 手动清空

如果需要手动清空 agent state（如重新开始某一集）：

```bash
# 编辑 outputs/{剧本名}/.agent-state.json
# 将对应 agent 的值改为空字符串
{
  "script-writer": "",  # 清空后，下次调用会创建新 agent
  ...
}
```

### 2. 跨集检测

Orchestrator 需要实现跨集检测逻辑：
- 记录当前处理的集数
- 当集数变化时，自动清空 `.agent-state.json`

### 3. 错误处理

如果 resume 失败（如 agentId 无效）：
- 回退到正常调用（创建新 agent）
- 更新 `.agent-state.json` 为新的 agentId

## 相关文档

- `references/06-storyboard-handoff.md` — Resumable Subagents 机制详细说明
- `skills/novel-to-script-orchestrator-skill/SKILL.md` — Orchestrator 实现

## 常见问题

### Q1: 为什么改为剧本级别配置？

**A**:
1. **隔离性**：不同剧本之间的 agent 上下文完全隔离，避免混淆
2. **并行处理**：可以同时处理多个剧本，互不干扰
3. **独立管理**：每个剧本有独立的 session 管理，更清晰
4. **避免冲突**：多个剧本不会共享同一个 agent state，避免状态冲突

### Q2: 如果我想重新生成某一集怎么办？

**A**: 手动清空对应 agent 的 agentId：
```json
// outputs/{剧本名}/.agent-state.json
{
  "script-writer": "",  // 清空后，下次调用会创建新 agent
  ...
}
```

### Q3: 这个机制只用于分镜阶段吗？

**A**: 不是。所有 agents 都可以使用这个机制：
- `script-writer`：写集时保持上下文
- `review-director`：审核时保持上下文
- `storyboard-artist`：分镜时保持上下文
- 等等

### Q4: 如果我删除了某个剧本的 .agent-state.json 会怎样？

**A**: Orchestrator 会重新创建该文件，该剧本的所有 agent 都会从头开始（不 resume）。其他剧本不受影响。

### Q5: 不同剧本可以并行处理吗？

**A**: 可以。每个剧本有独立的 `.agent-state.json`，可以同时处理多个剧本，互不干扰。

---

**最后更新**：2026-03-11
**维护者**：team-lead
**版本**：2.0（剧本级别配置）
