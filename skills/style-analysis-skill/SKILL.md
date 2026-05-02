---
name: style-analysis-skill
description: 风格分析技能。分析生成剧本的语言风格，对比爆款剧本，确保网文感和可读性。
---

# 风格分析技能

## 必读

1. `../../references/00-first-principles.md` — 第一性原则（可拍性、留存性）
2. `../../references/03-script-writing-standard.md` — 剧本写作标准（句长、对话比、视觉标记、网文感关键词）
3. `../../references/12-genre-specific-techniques.md` — 类型化技巧（男频/女频风格差异）

## 功能

深度分析剧本的语言风格，确保生成的剧本具有网文感、节奏感和可读性。

## 分析维度

### 1. 句长分析

**统计方法**：
```python
import re

def analyze_sentence_length(script):
    # 按句号、问号、感叹号分句
    sentences = re.split(r'[。！？]', script)
    sentences = [s.strip() for s in sentences if s.strip()]

    lengths = [len(s) for s in sentences]

    return {
        'avg_length': sum(lengths) / len(lengths),
        'short_ratio': len([l for l in lengths if l < 10]) / len(lengths),
        'medium_ratio': len([l for l in lengths if 10 <= l < 20]) / len(lengths),
        'long_ratio': len([l for l in lengths if l >= 20]) / len(lengths)
    }
```

**理想指标**：
- 平均句长：10-14字符
- 短句比例（<10字符）：30-40%
- 中句比例（10-20字符）：50-60%
- 长句比例（≥20字符）：<10%

### 2. 对话比分析

**统计方法**：
```python
def analyze_dialogue_ratio(script):
    # 识别对话（引号内的内容）
    dialogues = re.findall(r'[「『""]([^」』""]+)[」』""]', script)
    dialogue_chars = sum(len(d) for d in dialogues)
    total_chars = len(script)

    return {
        'dialogue_ratio': dialogue_chars / total_chars,
        'dialogue_count': len(dialogues),
        'avg_dialogue_length': dialogue_chars / len(dialogues) if dialogues else 0
    }
```

**理想指标**：
- 对话比：70-80%
- 对话数量：每1000字15-25条
- 平均对话长度：20-40字符

### 3. 视觉标记分析

**视觉标记列表**：
```python
visual_markers = {
    '表情': ['冷笑', '嗤笑', '冷哼', '微笑', '狞笑', '苦笑'],
    '眼神': ['眼神一冷', '眸光一沉', '目光如炬', '眼中闪过', '瞳孔一缩'],
    '动作': ['嘴角勾起', '挑眉', '皱眉', '咬牙', '握拳', '转身'],
    '气场': ['气势汹汹', '霸气侧漏', '冷气逼人', '杀气腾腾']
}
```

**统计方法**：
```python
def analyze_visual_markers(script):
    all_markers = []
    for category, markers in visual_markers.items():
        all_markers.extend(markers)

    marker_count = sum(script.count(marker) for marker in all_markers)
    chars_per_100 = len(script) / 100

    return {
        'markers_per_100': marker_count / chars_per_100,
        'marker_distribution': {
            category: sum(script.count(m) for m in markers)
            for category, markers in visual_markers.items()
        }
    }
```

**理想指标**：
- 视觉标记密度：3-5个/100字
- 分布均衡：各类标记都有使用

### 4. 网文感关键词分析

**网文感关键词**：
```python
wanwen_keywords = {
    '情绪强化': ['冷笑', '嗤笑', '冷哼', '冷声', '冷冷地'],
    '态度词': ['不屑', '轻蔑', '讥讽', '嘲讽', '鄙夷'],
    '气场词': ['霸气', '强势', '凌厉', '锐利', '凛然'],
    '反转词': ['没想到', '竟然', '居然', '原来', '突然'],
    '打脸词': ['啪啪打脸', '狠狠打脸', '当场打脸', '脸色一变']
}
```

**统计方法**：
```python
def analyze_wanwen_keywords(script):
    all_keywords = []
    for category, keywords in wanwen_keywords.items():
        all_keywords.extend(keywords)

    keyword_count = sum(script.count(kw) for kw in all_keywords)
    chars_per_100 = len(script) / 100

    return {
        'keywords_per_100': keyword_count / chars_per_100,
        'keyword_distribution': {
            category: sum(script.count(kw) for kw in keywords)
            for category, keywords in wanwen_keywords.items()
        }
    }
```

**理想指标**：
- 网文感关键词：1.5-2.5个/100字
- 分布：情绪强化词最多，其他均衡

### 5. 节奏感分析

**统计方法**：
```python
def analyze_rhythm(script):
    # 按场景分割
    scenes = re.split(r'场景\d+|第\d+场', script)

    scene_lengths = [len(s) for s in scenes if s.strip()]

    return {
        'scene_count': len(scene_lengths),
        'avg_scene_length': sum(scene_lengths) / len(scene_lengths),
        'length_variance': calculate_variance(scene_lengths),
        'rhythm_score': calculate_rhythm_score(scene_lengths)
    }
```

**理想指标**：
- 场景数：7-10个/集
- 平均场景长度：100-150字
- 长度方差：适中（有变化但不极端）

## 对比分析

### Step 1: 统计生成剧本

```python
generated_style = {
    'sentence': analyze_sentence_length(generated_script),
    'dialogue': analyze_dialogue_ratio(generated_script),
    'visual': analyze_visual_markers(generated_script),
    'wanwen': analyze_wanwen_keywords(generated_script),
    'rhythm': analyze_rhythm(generated_script)
}
```

### Step 2: 统计参考剧本

```python
reference_styles = [
    {
        'sentence': analyze_sentence_length(ref),
        'dialogue': analyze_dialogue_ratio(ref),
        'visual': analyze_visual_markers(ref),
        'wanwen': analyze_wanwen_keywords(ref),
        'rhythm': analyze_rhythm(ref)
    }
    for ref in reference_scripts
]

# 计算平均值
reference_avg = average(reference_styles)
```

### Step 3: 对比并生成报告

```python
report = {
    'sentence_analysis': compare_sentence(generated_style, reference_avg),
    'dialogue_analysis': compare_dialogue(generated_style, reference_avg),
    'visual_analysis': compare_visual(generated_style, reference_avg),
    'wanwen_analysis': compare_wanwen(generated_style, reference_avg),
    'rhythm_analysis': compare_rhythm(generated_style, reference_avg)
}
```

## 输出格式

```markdown
【风格分析报告】

## 1. 句长分析

生成剧本：
- 平均句长：18字符 ⚠️
- 短句比例：20% ⚠️
- 中句比例：60% ✓
- 长句比例：20% ⚠️

参考剧本：
- 平均句长：12字符
- 短句比例：35%
- 中句比例：55%
- 长句比例：10%

问题：
- 句子偏长，缺乏短句
- 长句比例过高

建议：
- 将长句拆分为2-3个短句
- 增加短句比例到30%以上
- 示例：
  原：她看着他，心中涌起一股复杂的情绪，既有愤怒也有不甘。
  改：她看着他。心中涌起复杂情绪。既愤怒，也不甘。

## 2. 对话比分析

生成剧本：
- 对话比：45% ⚠️
- 对话数量：12条/1000字 ⚠️
- 平均对话长度：35字符 ✓

参考剧本：
- 对话比：72%
- 对话数量：20条/1000字
- 平均对话长度：30字符

问题：
- 对话比严重偏低
- 叙述性文字过多

建议：
- 将叙述改为对话
- 增加人物互动
- 示例：
  原：她很生气，觉得他太过分了。
  改："你太过分了！"她愤怒地说。

## 3. 视觉标记分析

生成剧本：
- 视觉标记：1个/100字 ⚠️
- 分布：表情(0.5), 眼神(0.3), 动作(0.2), 气场(0)

参考剧本：
- 视觉标记：4个/100字
- 分布：表情(1.5), 眼神(1.0), 动作(1.0), 气场(0.5)

问题：
- 视觉标记严重不足
- 缺乏气场描写

建议：
- 增加表情描写（冷笑、嗤笑等）
- 增加眼神描写（眼神一冷、眸光一沉等）
- 增加气场描写（霸气、强势等）
- 示例：
  原："你算什么东西？"他说。
  改："你算什么东西？"他冷笑一声，眼神一冷。

## 4. 网文感关键词分析

生成剧本：
- 网文感关键词：0.5个/100字 ⚠️
- 分布：情绪强化(0.2), 态度词(0.1), 气场词(0.1), 反转词(0.1), 打脸词(0)

参考剧本：
- 网文感关键词：2个/100字
- 分布：情绪强化(0.8), 态度词(0.4), 气场词(0.3), 反转词(0.3), 打脸词(0.2)

问题：
- 网文感严重不足
- AI味较重

建议：
- 增加情绪强化词（冷笑、嗤笑、冷哼等）
- 增加态度词（不屑、轻蔑、讥讽等）
- 增加反转词（没想到、竟然、居然等）

## 5. 节奏感分析

生成剧本：
- 场景数：6个 ⚠️
- 平均场景长度：180字 ⚠️
- 长度方差：低 ⚠️

参考剧本：
- 场景数：8.5个
- 平均场景长度：120字
- 长度方差：中等

问题：
- 场景数偏少
- 场景过长
- 节奏单调

建议：
- 增加2个过渡场景
- 缩短场景长度
- 增加节奏变化

## 综合评分

- 句长：60/100 ⚠️
- 对话比：50/100 ⚠️
- 视觉标记：25/100 ⚠️
- 网文感：30/100 ⚠️
- 节奏感：65/100 ⚠️

**总分：46/100 FAIL**

## 优先修改建议

1. 提高对话比（45% → 70%）
2. 增加视觉标记（1个/100字 → 4个/100字）
3. 增加网文感关键词（0.5个/100字 → 2个/100字）
4. 拆分长句，增加短句比例
5. 增加场景数，优化节奏
```

## 成功标准

- 总分 ≥ 80分
- 5个维度得分均 ≥ 70分
- 对话比 ≥ 70%
- 视觉标记 ≥ 3个/100字
- 网文感关键词 ≥ 1.5个/100字

## 注意事项

1. **基准对比**：使用检索到的Top 5爆款剧本作为基准
2. **具体示例**：必须提供具体的修改示例
3. **可操作性**：建议必须具体、可执行
4. **优先级**：按影响程度排序修改建议
