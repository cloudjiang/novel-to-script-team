---
name: comparative-review-skill
description: 对比审核技能。对比生成剧本与爆款剧本的节奏、对话、情绪、框架，给出PASS/FAIL判断和改进建议。
---

# 对比审核技能

## 必读

1. `../../references/00-first-principles.md` — 第一性原则（可拍性、留存性、一致性、可验证性）
2. `../../references/03-script-writing-standard.md` — 剧本写作标准（对话比、视觉标记、网文感、节奏控制）
3. `../../references/04-review-gates.md` — 审核门槛（PASS/FAIL标准、回改流程）

## 功能

对比生成剧本与参考的爆款剧本，从多个维度进行分析，防止AI味，确保剧本质量。

## 对比维度

### 1. 节奏对比

**统计指标**：
- 场景数（scene_count）
- 冲突密度（conflict_density）= 冲突次数 / 总字数
- 平均场景时长（avg_scene_duration）
- 时长方差（duration_variance）
- 情绪强度（emotion_intensity）

**对比方法**：
```python
# 统计生成剧本
generated = analyze_rhythm(generated_script)

# 统计参考剧本（5个的平均值）
reference = average([analyze_rhythm(ref) for ref in reference_scripts])

# 对比
rhythm_score = compare_metrics(generated, reference)
```

**判断标准**：
- 场景数：±2个场景内为PASS
- 冲突密度：±0.01内为PASS
- 情绪强度：±0.01内为PASS

### 2. 对话风格对比

**统计指标**：
- 平均句长（avg_sentence_length）
- 对话比（dialogue_ratio）= 对话字数 / 总字数
- 视觉标记密度（visual_markers_per_100）
- 短句比例（short_sentence_ratio）< 10字符的句子占比
- 网文感关键词密度（wanwen_keywords_per_100）

**网文感关键词**：
```python
wanwen_keywords = [
    '冷笑', '嗤笑', '冷哼', '冷声', '冷冷',
    '眼神一冷', '眸光一沉', '嘴角勾起',
    '不屑', '轻蔑', '讥讽', '嘲讽',
    '霸气', '强势', '凌厉', '锐利'
]
```

**判断标准**：
- 句长：12±3字符为PASS
- 对话比：70%±10%为PASS
- 视觉标记：3-5个/100字为PASS

### 3. 情绪冲击力对比

**统计指标**：
- 情绪词汇密度（emotion_word_density）
- 情感极性摆动（emotion_polarity_swing）
- 高潮点数量（climax_count）
- 悬念设置（suspense_count）

**情绪词汇**：
```python
emotion_words = {
    '愤怒': ['愤怒', '暴怒', '怒火', '气愤', '恼怒'],
    '悲伤': ['悲伤', '难过', '伤心', '痛苦', '绝望'],
    '惊讶': ['惊讶', '震惊', '惊愕', '愕然', '惊呆'],
    '恐惧': ['恐惧', '害怕', '惊恐', '畏惧', '胆寒'],
    '喜悦': ['喜悦', '高兴', '欣喜', '愉悦', '兴奋']
}
```

**判断标准**：
- 情绪词汇：1.5-2.5个/100字为PASS
- 情感摆动：至少2次明显摆动为PASS
- 高潮点：至少1个为PASS

### 4. 框架结构对比

**结构要素**：
- 开局（hook）：前10%是否有强钩子
- 发展（development）：中间60%是否有持续冲突
- 高潮（climax）：是否有明显高潮点
- 反转（twist）：是否有意外反转
- 结局（ending）：是否有强悬念/钩子

**判断标准**：
- 5个要素至少满足4个为PASS

### 5. 跨集内容重复检查

**检查对象**：当前集与前一集的内容对比

**检查项**：
- 场景重复：当前集与前一集是否有相同的场景
- 剧情点重复：当前集与前一集是否有相同的剧情点
- 对话重复：当前集与前一集是否有相似的对话
- 事件重复：当前集与前一集是否是同一个事件

**判断标准**：
- 发现任何重复内容，必须 FAIL
- 必须指出具体的重复位置
- 必须要求删除或重写重复内容

**示例**：
```python
# 检查场景重复
ep01_scenes = extract_scenes(ep01_script)
ep02_scenes = extract_scenes(ep02_script)
duplicate_scenes = find_duplicates(ep01_scenes, ep02_scenes)

if duplicate_scenes:
    feedback.append({
        'dimension': '跨集内容重复',
        'issue': '发现重复场景',
        'location': f'第{N}集与第{N-1}集',
        'duplicates': duplicate_scenes,
        'suggestion': '删除重复场景，或改为新的场景'
    })
```

### 6. 事件完整性检查

**检查对象**：当前集的事件结构

**检查项**：
- 事件完整性：当前集是否是一个完整的事件（有开始、发展、结束）
- 剧情线完整性：当前集是否有未完成的剧情线
- 逻辑连贯性：当前集与下一集的规划是否有逻辑断层

**判断标准**：
- 事件不完整（如只有开始没有结束），必须 FAIL
- 有未完成的剧情线，必须 FAIL
- 与下一集的规划有逻辑断层，必须 FAIL

**示例**：
```python
# 检查事件完整性
event_structure = analyze_event_structure(script)

if not event_structure['has_beginning']:
    feedback.append({
        'dimension': '事件完整性',
        'issue': '事件缺少开始',
        'suggestion': '添加事件的触发点'
    })

if not event_structure['has_ending']:
    feedback.append({
        'dimension': '事件完整性',
        'issue': '事件缺少结束',
        'suggestion': '添加事件的结果或转折'
    })
```

## 执行流程

### Step 1: 加载剧本

```python
# 加载生成剧本
with open(generated_script_path, 'r') as f:
    generated_script = f.read()

# 加载参考剧本（之前检索的Top 5）
reference_scripts = []
for ref_path in reference_paths:
    with open(ref_path, 'r') as f:
        reference_scripts.append(f.read())
```

### Step 2: 统计指标

```python
# 生成剧本指标
gen_rhythm = analyze_rhythm(generated_script)
gen_style = analyze_style(generated_script)
gen_emotion = analyze_emotion(generated_script)
gen_structure = analyze_structure(generated_script)

# 参考剧本平均指标
ref_rhythm = average([analyze_rhythm(ref) for ref in reference_scripts])
ref_style = average([analyze_style(ref) for ref in reference_scripts])
ref_emotion = average([analyze_emotion(ref) for ref in reference_scripts])
ref_structure = average([analyze_structure(ref) for ref in reference_scripts])
```

### Step 3: 对比分析

```python
feedback = []

# 节奏对比
if abs(gen_rhythm['scene_count'] - ref_rhythm['scene_count']) > 2:
    feedback.append({
        'dimension': '节奏',
        'issue': f"场景数偏{'少' if gen_rhythm['scene_count'] < ref_rhythm['scene_count'] else '多'}",
        'generated': gen_rhythm['scene_count'],
        'reference': ref_rhythm['scene_count'],
        'suggestion': f"建议调整为{ref_rhythm['scene_count']}个场景"
    })

# 对话风格对比
if gen_style['dialogue_ratio'] < 0.6:
    feedback.append({
        'dimension': '对话风格',
        'issue': '对话比偏低',
        'generated': f"{gen_style['dialogue_ratio']:.1%}",
        'reference': f"{ref_style['dialogue_ratio']:.1%}",
        'suggestion': '增加对话，减少叙述性文字'
    })

# 跨集内容重复检查
if previous_script:
    duplicate_scenes = find_duplicate_scenes(generated_script, previous_script)
    if duplicate_scenes:
        feedback.append({
            'dimension': '跨集内容重复',
            'issue': '发现重复场景',
            'location': f'第{N}集与第{N-1}集',
            'duplicates': duplicate_scenes,
            'suggestion': '删除重复场景，或改为新的场景',
            'severity': 'CRITICAL'  # 必须修复
        })

# 事件完整性检查
event_structure = analyze_event_structure(generated_script)
if not event_structure['is_complete']:
    feedback.append({
        'dimension': '事件完整性',
        'issue': event_structure['issue'],
        'suggestion': event_structure['suggestion'],
        'severity': 'CRITICAL'  # 必须修复
    })

# ... 其他维度对比
```

### Step 4: 生成审核报告

```python
report = {
    'verdict': 'PASS' if len(feedback) == 0 else 'FAIL',
    'overall_score': calculate_overall_score(gen, ref),
    'dimensions': {
        'rhythm': rhythm_score,
        'style': style_score,
        'emotion': emotion_score,
        'structure': structure_score
    },
    'feedback': feedback,
    'reference_examples': find_best_examples(feedback, reference_scripts)
}
```

## 输出格式

```markdown
【综合审核报告】

判定：FAIL
综合得分：72/100

## 维度得分
- 节奏：65/100 ⚠️
- 对话风格：70/100 ⚠️
- 情绪冲击力：80/100 ✓
- 框架结构：85/100 ✓
- 跨集内容重复：FAIL ❌
- 事件完整性：FAIL ❌

## 详细反馈

### 跨集内容重复问题（CRITICAL）
1. 发现重复场景
   - 位置：第2集与第1集
   - 重复内容：搜身 + 签字 + 离开
   - 建议：删除第2集的重复内容，改为新的场景（如拍卖会、修炼等）

### 事件完整性问题（CRITICAL）
1. 事件不完整
   - 位置：第2集
   - 问题：第2集重复了第1集的事件，没有新的完整事件
   - 建议：第2集应该是一个新的完整事件，如"拍卖会展示实力"（入场 → 竞拍 → 展示 → 震惊）

### 节奏问题
1. 场景数偏少
   - 生成剧本：6个场景
   - 参考平均：8.5个场景
   - 建议：增加2个过渡场景，建议在第3场景后和第5场景后各增加一个

2. 冲突密度偏低
   - 生成剧本：0.015
   - 参考平均：0.035
   - 建议：在第3、5场景增加对抗情节

### 对话风格问题
1. 对话比偏低
   - 生成剧本：45%
   - 参考平均：72%
   - 建议：增加对话，减少叙述。将叙述性文字改为对话形式

2. 句长偏长
   - 生成剧本：18字符
   - 参考平均：12字符
   - 建议：拆分长句，增加短句比例

3. 视觉标记不足
   - 生成剧本：1个/100字
   - 参考平均：4个/100字
   - 建议：增加视觉标记（冷笑、嗤笑、冷哼等）

## 参考示例

请参考以下爆款剧本的处理方式：

1. 《封总的复仇娇妻》第15集
   - 对抗场景结构：先铺垫→冲突爆发→反转→钩子
   - 对话节奏：短句+高密度+情绪化

2. 《霸总的替身新娘》第8集
   - 打脸场景：层层递进，每次打脸都有新信息
   - 视觉标记：冷笑、嗤笑、眼神一冷等高频使用

## 修改建议

优先级1（必须修改 - CRITICAL）：
- **删除第2集的重复内容，改为新的完整事件**
- **确保每集是一个独立的故事单元**

优先级2（必须修改）：
- 增加2个过渡场景
- 提高对话比到70%以上

优先级3（建议修改）：
- 拆分长句
- 增加视觉标记

优先级4（可选优化）：
- 增强情绪词汇密度
- 优化悬念设置
```

## 成功标准

- 综合得分 ≥ 80分为PASS
- 4个维度得分均 ≥ 70分
- 无优先级1的问题
- **跨集内容重复检查：PASS（无重复内容）**
- **事件完整性检查：PASS（事件完整、无逻辑断层）**

## 注意事项

1. **对比基准**：使用检索到的Top 5爆款剧本作为基准
2. **动态调整**：根据实际效果调整判断标准
3. **具体建议**：必须引用具体的参考剧本示例
4. **可操作性**：建议必须具体、可执行
