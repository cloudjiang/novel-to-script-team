---
name: hit-script-retrieval-skill
description: 爆款剧本检索技能。使用混合搜索（语义+关键词）检索最相关的爆款剧本，为生成提供参考。
---

# 爆款剧本检索技能

## 必读

1. `../../references/00-first-principles.md` — 第一性原则（可拍性、留存性、一致性）
2. `../../references/03-script-writing-standard.md` — 剧本写作标准（对话比、视觉标记、网文感）
3. `../../references/12-genre-specific-techniques.md` — 类型化技巧（男频/女频特征）

## 功能

从117部爆款短剧剧本中检索最相关的剧本，为剧本生成提供参考。

## 检索方法

使用**混合搜索**（Chroma语义搜索 + TF-IDF关键词搜索）：
- 语义搜索权重：60%（理解深层含义）
- 关键词搜索权重：40%（精确匹配）

## 使用场景

### 1. 剧本生成前检索

在生成剧本前，根据以下信息检索相关剧本：
- 剧本类型（复仇/逆袭/穿越/重生等）
- 情绪基调（愤怒/悲伤/爽感/紧张等）
- 主要情节（打脸/揭秘/对抗/和解等）
- 人物关系（主角vs反派/主角vs配角等）
- 场景类型（豪门/古代/现代/职场等）

**示例查询**：
```
"复仇女主霸总豪门打脸"
"穿越古代逆袭当皇后"
"重生复仇虐恋"
```

### 2. 检索结果使用

检索返回Top 5最相关的剧本，包含：
- 剧本文件名
- 相似度得分
- 内容预览（前200字符）
- 完整文件路径

**注入到context**：
```
参考以下爆款剧本的风格和节奏：

【参考剧本1】《封总的复仇娇妻》
- 相似度：0.892
- 特点：复仇女主、霸总、豪门恩怨、打脸爽剧
- 节奏：快节奏、高冲突密度、强情绪冲击
- 对话风格：短句、高对话比、视觉标记丰富

【参考剧本2】...
```

## 执行步骤

### Step 1: 构建检索查询

从当前剧本需求中提取关键信息：
```python
# 示例：从分集规划中提取
query_parts = []
if "类型" in episode_plan:
    query_parts.append(episode_plan["类型"])
if "情绪" in episode_plan:
    query_parts.append(episode_plan["情绪"])
if "主要情节" in episode_plan:
    query_parts.append(episode_plan["主要情节"])

query = " ".join(query_parts)
# 结果：query = "复仇 愤怒 打脸揭秘"
```

### Step 2: 执行检索

使用混合搜索引擎：
```python
from hybrid_search import HybridSearchEngine

# 初始化（只需一次）
engine = HybridSearchEngine("../../knowledge/hit-scripts-md")

# 检索Top 5
results = engine.hybrid_search(
    query=query,
    n_results=5,
    semantic_weight=0.6,
    keyword_weight=0.4
)
```

### Step 3: 读取完整内容

```python
reference_scripts = []
for result in results:
    with open(result['path'], 'r', encoding='utf-8') as f:
        content = f.read()
        reference_scripts.append({
            'filename': result['filename'],
            'score': result['score'],
            'content': content[:5000]  # 取前5000字符
        })
```

### Step 4: 注入到生成提示词

```
你是一名短剧编剧，现在需要创作第N集剧本。

【参考爆款剧本】
以下是5个最相关的爆款剧本，请参考它们的：
- 节奏：场景数、冲突密度、时长分布
- 对话：句长、对话比、视觉标记
- 情绪：情绪强度、情感极性摆动
- 框架：开局-发展-高潮-反转-结局

1. 《封总的复仇娇妻》（相似度：0.892）
[内容节选...]

2. 《...》（相似度：0.856）
[内容节选...]

...

【当前任务】
根据以上参考，创作第N集剧本...
```

## 对比分析

生成剧本后，使用相同的5个参考剧本进行对比分析：

### 1. 节奏对比

```python
# 统计生成剧本的节奏指标
generated_metrics = {
    'scene_count': 6,
    'conflict_density': 0.015,
    'avg_scene_duration': 10,
    'emotion_intensity': 0.012
}

# 统计参考剧本的平均指标
reference_metrics = {
    'scene_count': 8.5,
    'conflict_density': 0.035,
    'avg_scene_duration': 7.5,
    'emotion_intensity': 0.025
}

# 对比分析
if generated_metrics['scene_count'] < reference_metrics['scene_count']:
    feedback.append("场景数偏少，建议增加2个过渡场景")
```

### 2. 对话风格对比

```python
# 统计对话指标
generated_style = {
    'avg_sentence_length': 18,
    'dialogue_ratio': 0.45,
    'visual_markers_per_100': 1
}

reference_style = {
    'avg_sentence_length': 12,
    'dialogue_ratio': 0.72,
    'visual_markers_per_100': 4
}

# 对比分析
if generated_style['dialogue_ratio'] < reference_style['dialogue_ratio']:
    feedback.append("对话比偏低，建议增加对话，减少叙述")
```

### 3. 情绪冲击力对比

```python
# 分析情绪词汇密度
generated_emotion_density = 0.5  # 每100字0.5个情绪词
reference_emotion_density = 2.0  # 每100字2个情绪词

if generated_emotion_density < reference_emotion_density:
    feedback.append("情绪词汇偏少，建议增加情绪化表达")
```

## 复审流程

### 导演复审（review-director）

使用 `comparative-review-skill` 进行综合对比：
1. 加载生成剧本和5个参考剧本
2. 对比节奏、对话、情绪、框架
3. 给出PASS/FAIL判断
4. 提供具体改进建议（引用具体的参考剧本）

**输出示例**：
```
【综合审核】FAIL

节奏问题：
- 场景数：生成6场景，参考平均8.5场景 → 建议增加2个过渡场景
- 冲突密度：生成0.015，参考平均0.035 → 建议在第3、5场景增加对抗

对话风格问题：
- 句长：生成18字符，参考平均12字符 → 建议拆分长句
- 对话比：生成45%，参考平均72% → 建议增加对话，减少叙述

参考示例：
请参考《封总的复仇娇妻》第15集的对抗场景结构
请参考《霸总的替身新娘》第8集的对话节奏
```

### 编剧复审（script-writer）

使用 `style-analysis-skill` 分析风格：
1. 统计生成剧本的语言风格指标
2. 统计5个参考剧本的平均指标
3. 对比分析差异
4. 提供改进建议

**输出示例**：
```
【风格分析】

句长分布：
- 生成剧本：平均18字符
- 参考剧本：平均12字符
- 建议：拆分长句，增加短句比例

对话比：
- 生成剧本：45%
- 参考剧本：72%
- 建议：增加对话，减少叙述性文字

视觉标记：
- 生成剧本：1个/100字
- 参考剧本：4个/100字
- 建议：增加视觉标记（如：冷笑、嗤笑、冷哼等）
```

## 成功标准

1. **检索准确性**：检索到的5个剧本相似度 > 0.5
2. **参考有效性**：生成剧本的指标接近参考剧本（±20%）
3. **风格一致性**：网文感、节奏感、情绪冲击力达标
4. **复审通过**：导演和编剧复审均PASS

## 注意事项

1. **开源版语料**：默认不包含 `knowledge/hit-scripts-md/`，请自行放入有权使用的 `.md` 剧本语料
2. **首次使用**：首次运行需要构建索引（约60秒），索引会持久化保存到本地 `.search_index/`
3. **后续使用**：索引已保存，加载速度快（1-2秒）
4. **男女频分类**：支持按男频/女频/全部进行过滤，提高检索精准度
5. **权重调整**：可根据实际效果调整语义/关键词权重
6. **参考数量**：默认检索Top 5，可根据需要调整（3-10个）
7. **内容长度**：注入context时建议每个参考剧本取前5000字符，避免超出上下文限制

## 文件位置

- 检索引擎：`../../scripts/improved_hybrid_search.py`（推荐）或 `../../scripts/hybrid_search.py`（备选）
- 爆款剧本：`../../knowledge/hit-scripts-md/*.md`（本地自备语料，开源版默认不包含）
- 对比分析：`comparative-review-skill`
- 风格分析：`style-analysis-skill`

---

## 使用指南（Agent 集成）

### 在 script-writer 中使用

**Step 0：判断原小说类型（男频/女频/中性）**
```
根据原小说特征判断（核心判断标准：主角性别）：

男频特征：
- 【核心】主角：男性主角为中心，男主视角
- 类型：复仇、逆袭、霸道、战神、龙王、赘婿、神医
- 情节：打脸、装逼、碾压、称霸
- 示例：《赘婿之王》《战神归来》《神医下山》

女频特征：
- 【核心】主角：女性主角为中心，女主视角
- 类型：虐恋、甜宠、豪门、替身、真假千金、重生复仇
- 情节：误会、虐心、和解、宠溺、逆袭
- 示例：《豪门替身妻》《真假千金》《霸总的替身新娘》

中性/不确定：
- 双主角、群像剧、或类型不明显
- 使用 `all` 参数不限类型

判断流程：
1. 首先看主角性别：男主 → 男频，女主 → 女频
2. 其次看类型关键词：复仇/战神/赘婿 → 男频，虐恋/甜宠/替身 → 女频
3. 最后看情节特征：打脸/碾压 → 男频，误会/虐心 → 女频

判断结果：
- 男频 → 使用 `male` 参数
- 女频 → 使用 `female` 参数
- 中性 → 使用 `all` 参数
```

**Step 1：构建查询关键词**
```
根据剧本特征选择关键词：
- 核心类型：重生、穿越、复仇、逆袭、虐恋、甜宠
- 场景类型：豪门、古代、现代、职场、校园、宫廷
- 特殊元素：道门、玄幻、霸总、白莲花、打脸（可选）

示例：query = "重生 复仇 豪门"
```

**Step 2：执行检索**
```bash
# 推荐：使用改进版混合搜索（持久化索引 + 男女频分类）
python3 scripts/improved_hybrid_search.py "重生 复仇 豪门" male
# 或指定女频：python3 scripts/improved_hybrid_search.py "重生 复仇 豪门" female
# 或不限类型：python3 scripts/improved_hybrid_search.py "重生 复仇 豪门" all

# 备选：使用快速搜索（如环境不支持）
python3 scripts/quick_search.py "重生 复仇 豪门"
```

**Step 3：读取参考剧本**
```
读取检索结果的前5000字作为参考
```

**Step 4：注入到 Context**
```
将参考剧本内容注入到生成 prompt 中，参考其：
1. 对话比（约70%）
2. 视觉标记密度（3.5-4.5个/100字）
3. 网文感关键词（1.8-3.0个/100字）
4. 句长控制（10-14字符）
5. 节奏感（起承转合）
```

### 关键词选择建议

**优先级1：核心类型（必选）**
- 重生、穿越、复仇、逆袭、虐恋、甜宠

**优先级2：场景类型（必选）**
- 豪门、古代、现代、职场、校园、宫廷

**优先级3：特殊元素（可选）**
- 道门、玄幻、霸总、白莲花、打脸

**示例**：
```
✅ 好的查询："重生 复仇 豪门"（3个核心关键词）
❌ 不好的查询："重生复仇道门天师豪门虐待"（太多关键词）
```

### 匹配度阈值

- **高相关**：匹配度 ≥ 3（推荐使用）
- **中相关**：匹配度 = 2（可参考）
- **低相关**：匹配度 = 1（不推荐）

### 数量建议

- **精读**：Top 3（完整阅读前5000字）
- **略读**：Top 5（阅读前1000字）
- **浏览**：Top 10（仅看标题和简介）

### 常见问题

**Q1：为什么检索不到结果？**
- 使用更通用的关键词（如："重生 复仇"）
- 降低匹配度阈值（从3降到2）
- 增加关键词变体（如："豪门" + "富豪"）

**Q2：检索结果不相关？**
- 增加更具体的关键词
- 提高匹配度阈值（从2提到3）
- 手动筛选结果

**Q3：检索速度慢？**
- 首次初始化慢是正常的（Chroma 建立索引约60秒）
- 后续查询会很快（索引已持久化保存）
- 如需快速测试，可临时使用 quick_search.py
- 缓存检索结果供后续使用

**Q4：如何选择男频/女频？**
- 根据原小说类型选择：男频通常是复仇、逆袭、霸道；女频通常是虐恋、甜宠、豪门
- 使用 `male` 参数检索男频剧本
- 使用 `female` 参数检索女频剧本
- 使用 `all` 参数不限类型（默认）
