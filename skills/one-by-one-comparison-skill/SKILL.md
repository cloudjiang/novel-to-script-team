---
name: one-by-one-comparison-skill
description: 逐一对比技能。将生成剧本与每个参考剧本逐一对比，按照剧本评价标准给出详细批判和改进建议。
---

# 逐一对比技能

## 必读
1. `../../references/00-first-principles.md`
2. `../../references/03-script-writing-standard.md`
3. `../../references/04-review-gates.md`

## 技能说明

将生成剧本与检索到的Top 5参考剧本逐一对比，每次对比都按照统一的评价标准进行深度分析，给出具体的批判和改进建议。

## 评价标准（100分制）

### 1. 节奏控制（20分）

**评分细则**：
- 场景数量（5分）：与参考剧本相差±2个场景内得满分
- 场景时长分配（5分）：时长分布合理，有快有慢
- 冲突密度（5分）：冲突次数/总字数 ≥ 0.03
- 节奏变化（5分）：有明显的节奏起伏

**对比方法**：
```python
# 统计生成剧本
gen_scenes = count_scenes(generated_script)
gen_conflicts = count_conflicts(generated_script)
gen_conflict_density = gen_conflicts / len(generated_script)

# 统计参考剧本
ref_scenes = count_scenes(reference_script)
ref_conflicts = count_conflicts(reference_script)
ref_conflict_density = ref_conflicts / len(reference_script)

# 评分
scene_score = 5 if abs(gen_scenes - ref_scenes) <= 2 else max(0, 5 - abs(gen_scenes - ref_scenes))
conflict_score = 5 if gen_conflict_density >= 0.03 else gen_conflict_density / 0.03 * 5
```

### 2. 对话风格（25分）

**评分细则**：
- 对话比例（10分）：70%+ 得满分，每低5%扣2分
- 句长控制（8分）：平均10-14字符得满分
- 短句比例（4分）：30-40%得满分
- 对话自然度（3分）：人物区分度、口语化程度

**对比方法**：
```python
# 对话比例
gen_dialogue_ratio = calculate_dialogue_ratio(generated_script)
ref_dialogue_ratio = calculate_dialogue_ratio(reference_script)

dialogue_score = 10 if gen_dialogue_ratio >= 0.7 else gen_dialogue_ratio / 0.7 * 10

# 句长
gen_avg_length = calculate_avg_sentence_length(generated_script)
ref_avg_length = calculate_avg_sentence_length(reference_script)

if 10 <= gen_avg_length <= 14:
    length_score = 8
else:
    length_score = max(0, 8 - abs(gen_avg_length - 12) * 0.5)
```

### 3. 视觉化表达（20分）

**评分细则**：
- 视觉标记密度（10分）：3-5个/100字得满分
- 表情描写（4分）：冷笑、嗤笑、冷哼等
- 眼神描写（3分）：眼神一冷、眸光一沉等
- 动作描写（3分）：嘴角勾起、挑眉、转身等

**对比方法**：
```python
visual_markers = ['冷笑', '嗤笑', '冷哼', '眼神一冷', '眸光一沉', '嘴角勾起', '挑眉', '转身']

gen_marker_density = count_markers(generated_script, visual_markers) / (len(generated_script) / 100)
ref_marker_density = count_markers(reference_script, visual_markers) / (len(reference_script) / 100)

if 3 <= gen_marker_density <= 5:
    marker_score = 10
else:
    marker_score = max(0, 10 - abs(gen_marker_density - 4) * 2)
```

### 4. 网文感（20分）

**评分细则**：
- 网文感关键词密度（10分）：1.5-2.5个/100字得满分
- 情绪强化词（4分）：冷笑、嗤笑、冷哼、冷声等
- 态度词（3分）：不屑、轻蔑、讥讽、嘲讽等
- 打脸节奏（3分）：打脸场景数量和质量

**对比方法**：
```python
wanwen_keywords = {
    '情绪强化': ['冷笑', '嗤笑', '冷哼', '冷声', '冷冷地'],
    '态度词': ['不屑', '轻蔑', '讥讽', '嘲讽', '鄙夷'],
    '气场词': ['霸气', '强势', '凌厉', '锐利', '凛然'],
    '打脸词': ['啪啪打脸', '狠狠打脸', '当场打脸', '脸色一变']
}

gen_keyword_density = count_all_keywords(generated_script, wanwen_keywords) / (len(generated_script) / 100)
ref_keyword_density = count_all_keywords(reference_script, wanwen_keywords) / (len(reference_script) / 100)

if 1.5 <= gen_keyword_density <= 2.5:
    keyword_score = 10
else:
    keyword_score = max(0, 10 - abs(gen_keyword_density - 2) * 3)
```

### 5. 结构完整性（15分）

**评分细则**：
- 开局钩子（3分）：前10%是否有强冲突
- 中段冲突（4分）：中间60%是否持续有冲突
- 高潮设计（3分）：是否有明显高潮点
- 反转设置（3分）：是否有意外反转
- 结尾悬念（2分）：是否有强钩子

**对比方法**：
```python
structure_elements = {
    'hook': check_opening_hook(script),  # True/False
    'development': check_continuous_conflict(script),
    'climax': check_climax(script),
    'twist': check_twist(script),
    'ending': check_ending_hook(script)
}

structure_score = sum([
    3 if structure_elements['hook'] else 0,
    4 if structure_elements['development'] else 0,
    3 if structure_elements['climax'] else 0,
    3 if structure_elements['twist'] else 0,
    2 if structure_elements['ending'] else 0
])
```

## 执行流程

### Step 1: 加载剧本

```python
# 加载生成剧本
with open(f'outputs/{剧本名}/scripts/ep{N}.md', 'r') as f:
    generated_script = f.read()

# 加载参考剧本列表（从检索结果或style-analysis报告中获取）
reference_files = [
    'knowledge/hit-scripts-md/参考剧本1.md',
    'knowledge/hit-scripts-md/参考剧本2.md',
    'knowledge/hit-scripts-md/参考剧本3.md',
    'knowledge/hit-scripts-md/参考剧本4.md',
    'knowledge/hit-scripts-md/参考剧本5.md'
]

reference_scripts = []
for ref_file in reference_files:
    with open(ref_file, 'r') as f:
        reference_scripts.append({
            'filename': os.path.basename(ref_file),
            'content': f.read()
        })
```

### Step 2: 逐个对比

```python
comparison_results = []

for i, ref in enumerate(reference_scripts, 1):
    print(f"\n{'='*80}")
    print(f"对比 {i}/5: 生成剧本 vs {ref['filename']}")
    print(f"{'='*80}\n")

    # 五大维度评分
    rhythm_score = compare_rhythm(generated_script, ref['content'])
    dialogue_score = compare_dialogue(generated_script, ref['content'])
    visual_score = compare_visual(generated_script, ref['content'])
    wanwen_score = compare_wanwen(generated_script, ref['content'])
    structure_score = compare_structure(generated_script, ref['content'])

    total_score = rhythm_score + dialogue_score + visual_score + wanwen_score + structure_score

    # 识别具体问题
    issues = identify_issues(generated_script, ref['content'])

    # 提取参考示例
    examples = extract_examples(ref['content'], issues)

    # 生成改进建议
    suggestions = generate_suggestions(issues, examples)

    comparison_results.append({
        'reference': ref['filename'],
        'scores': {
            'rhythm': rhythm_score,
            'dialogue': dialogue_score,
            'visual': visual_score,
            'wanwen': wanwen_score,
            'structure': structure_score,
            'total': total_score
        },
        'issues': issues,
        'examples': examples,
        'suggestions': suggestions
    })
```

### Step 3: 综合分析

```python
# 汇总共同问题
common_issues = find_common_issues(comparison_results)

# 计算平均得分
avg_scores = calculate_average_scores(comparison_results)

# 识别最弱维度
weakest_dimensions = identify_weakest_dimensions(avg_scores)

# 生成优先级建议
priority_suggestions = prioritize_suggestions(common_issues, weakest_dimensions)
```

### Step 4: 生成报告

```markdown
# 第{N}集逐一对比分析报告

## 一、综合评分

| 维度 | 平均得分 | 评级 |
|------|---------|------|
| 节奏控制 | 15/20 | B |
| 对话风格 | 18/25 | B+ |
| 视觉化表达 | 12/20 | C+ |
| 网文感 | 10/20 | C |
| 结构完整性 | 13/15 | A- |
| **总分** | **68/100** | **C+** |

**判定**：❌ FAIL（需达到80分以上）

---

## 二、逐一对比详情

### 对比1：生成剧本 vs 《天降多宝后，渣过妈咪的人都后悔了》第1集

#### 评分详情
- 节奏控制：14/20 ⚠️
- 对话风格：16/25 ⚠️
- 视觉化表达：10/20 ⚠️
- 网文感：8/20 ⚠️
- 结构完整性：12/15 ✓
- **小计：60/100**

#### 具体问题

**1. 对话比偏低（优先级：高）**
- **生成剧本**：对话比45%
- **参考剧本**：对话比75%
- **差距**：-30%
- **位置**：场景2（萧家客厅）叙述过多

**参考示例**（《天降多宝后》第1集，场景2）：
```
【参考剧本片段】
萧万擎冷笑："你以为你是谁？我萧家的养子？"
沈倾城咬牙："我为这个家付出了十年！"
"付出？"萧万擎嗤笑，"你配吗？"
林秀雪冷冷道："搜她的包。"
```

**改进建议**：
- 将叙述改为对话
- 原文："她很生气，觉得他们太过分了。"
- 改为："你们太过分了！"她愤怒地说。

---

**2. 视觉标记不足（优先级：高）**
- **生成剧本**：1.2个/100字
- **参考剧本**：4.5个/100字
- **差距**：-3.3个/100字
- **位置**：全文缺乏表情和眼神描写

**参考示例**（《天降多宝后》第1集）：
```
【参考剧本片段】
萧万擎冷笑一声，眼神一冷："把她的东西都搜出来。"
林秀雪嘴角勾起一抹讥讽："还装什么清高？"
沈倾城眸光一沉，冷冷地看着他们。
```

**改进建议**：
- 在对话后增加表情描写（冷笑、嗤笑、冷哼）
- 在冲突场景增加眼神描写（眼神一冷、眸光一沉）
- 在转折处增加动作描写（嘴角勾起、转身离开）

---

**3. 网文感关键词缺失（优先级：中）**
- **生成剧本**：0.8个/100字
- **参考剧本**：2.3个/100字
- **差距**：-1.5个/100字
- **位置**：缺乏情绪强化词和态度词

**参考示例**（《天降多宝后》第1集）：
```
【参考剧本片段】
"不屑"、"轻蔑"、"讥讽"、"冷笑"、"嗤笑"、"冷哼"
这些词汇高频出现，营造强烈的情绪冲击
```

**改进建议**：
- 增加情绪强化词：冷笑、嗤笑、冷哼、冷声
- 增加态度词：不屑、轻蔑、讥讽、嘲讽
- 增加气场词：霸气、强势、凌厉

---

### 对比2：生成剧本 vs 《豪门弃女逆袭记》第1集

#### 评分详情
- 节奏控制：16/20 ✓
- 对话风格：18/25 ⚠️
- 视觉化表达：12/20 ⚠️
- 网文感：10/20 ⚠️
- 结构完整性：14/15 ✓
- **小计：70/100**

#### 具体问题

**1. 句长偏长（优先级：中）**
- **生成剧本**：平均18字符
- **参考剧本**：平均11字符
- **差距**：+7字符
- **位置**：场景1和场景3的对话

**参考示例**（《豪门弃女逆袭记》第1集）：
```
【参考剧本片段】
"你算什么东西？"（7字）
"滚出去。"（4字）
"我不走。"（4字）
"那就别怪我不客气。"（9字）
```

**改进建议**：
- 将长句拆分为2-3个短句
- 原文："她看着他，心中涌起一股复杂的情绪，既有愤怒也有不甘。"（26字）
- 改为："她看着他。心中涌起复杂情绪。既愤怒，也不甘。"（3句，平均8字）

---

**2. 打脸节奏不够密集（优先级：中）**
- **生成剧本**：3次打脸/1集
- **参考剧本**：5次打脸/1集
- **差距**：-2次
- **位置**：场景2和场景3可增加打脸

**参考示例**（《豪门弃女逆袭记》第1集）：
```
【参考剧本片段】
打脸1：搜身无果
打脸2：项链在别人身上
打脸3：揭露真相
打脸4：反击成功
打脸5：预言应验
```

**改进建议**：
- 在场景2增加一次小打脸（如：萧家人的谎言被揭穿）
- 在场景3增加一次打脸（如：张家人的能力展示）

---

### 对比3：生成剧本 vs 《爱在焚心成焰时》第1集

（类似格式，继续对比...）

---

### 对比4：生成剧本 vs 《顾总千金有点毒》第1集

（类似格式，继续对比...）

---

### 对比5：生成剧本 vs 《锦衣卫的第二人生》第1集

（类似格式，继续对比...）

---

## 三、共同问题汇总

### 问题1：对话比偏低（出现频率：5/5）

**5个参考剧本的对话比**：
1. 《天降多宝后》：75%
2. 《豪门弃女逆袭记》：72%
3. 《爱在焚心成焰时》：78%
4. 《顾总千金有点毒》：70%
5. 《锦衣卫的第二人生》：73%
**平均**：73.6%

**生成剧本的对话比**：45%

**差距**：-28.6%

**影响**：严重影响节奏感和可读性，AI味较重

**改进建议**：
1. 将所有叙述性文字改为对话形式
2. 增加人物互动和对话场景
3. 目标：将对话比提升到70%以上

---

### 问题2：视觉标记不足（出现频率：5/5）

**5个参考剧本的视觉标记密度**：
1. 《天降多宝后》：4.5个/100字
2. 《豪门弃女逆袭记》：4.2个/100字
3. 《爱在焚心成焰时》：5.1个/100字
4. 《顾总千金有点毒》：3.8个/100字
5. 《锦衣卫的第二人生》：4.0个/100字
**平均**：4.3个/100字

**生成剧本的视觉标记密度**：1.2个/100字

**差距**：-3.1个/100字

**影响**：画面感不足，情绪表达不够强烈

**改进建议**：
1. 在每句对话后增加表情描写（冷笑、嗤笑、冷哼）
2. 在冲突场景增加眼神描写（眼神一冷、眸光一沉）
3. 在转折处增加动作描写（嘴角勾起、转身离开）
4. 目标：将视觉标记密度提升到4个/100字以上

---

### 问题3：网文感关键词缺失（出现频率：5/5）

**5个参考剧本的网文感关键词密度**：
1. 《天降多宝后》：2.3个/100字
2. 《豪门弃女逆袭记》：2.0个/100字
3. 《爱在焚心成焰时》：2.5个/100字
4. 《顾总千金有点毒》：1.8个/100字
5. 《锦衣卫的第二人生》：2.1个/100字
**平均**：2.1个/100字

**生成剧本的网文感关键词密度**：0.8个/100字

**差距**：-1.3个/100字

**影响**：网文感不足，AI味较重

**改进建议**：
1. 增加情绪强化词：冷笑、嗤笑、冷哼、冷声、冷冷地
2. 增加态度词：不屑、轻蔑、讥讽、嘲讽、鄙夷
3. 增加气场词：霸气、强势、凌厉、锐利、凛然
4. 目标：将网文感关键词密度提升到2个/100字以上

---

## 四、优先级改进建议

### 优先级1（必须立即修改）

1. **提高对话比（45% → 70%+）**
   - 影响：最严重，直接影响可读性和节奏感
   - 工作量：大（需要重写大部分叙述）
   - 预期效果：+15分

2. **增加视觉标记（1.2 → 4个/100字）**
   - 影响：严重，影响画面感和情绪表达
   - 工作量：中（在现有对话后增加描写）
   - 预期效果：+8分

### 优先级2（强烈建议修改）

3. **增加网文感关键词（0.8 → 2个/100字）**
   - 影响：中等，影响网文感和爽点
   - 工作量：中（替换部分词汇）
   - 预期效果：+10分

4. **拆分长句（18字符 → 11字符）**
   - 影响：中等，影响节奏感
   - 工作量：中（拆分长句）
   - 预期效果：+7分

### 优先级3（建议优化）

5. **增加打脸密度（3次 → 5次）**
   - 影响：较小，影响爽点密度
   - 工作量：小（增加2个打脸场景）
   - 预期效果：+3分

---

## 五、修改后预期得分

**当前得分**：68/100（C+）

**修改后预期得分**：
- 完成优先级1：68 + 15 + 8 = 91/100（A）
- 完成优先级1+2：91 + 10 + 7 = 108/100（满分100，实际95+）
- 完成全部：95+ /100（A+）

**建议**：
- 至少完成优先级1，确保达到80分以上（PASS标准）
- 建议完成优先级1+2，确保达到90分以上（优秀标准）

---

## 六、具体修改示例

### 示例1：提高对话比

**原文**（场景2，叙述过多）：
```
张逸臣看着萧家人，心中涌起一股复杂的情绪。他想起了过去十年的种种委屈和不公，觉得这些人太过分了。他决定不再忍受，要离开这个冷漠的家。
```

**修改后**（改为对话）：
```
张逸臣看着萧家人，眼神一冷。

"十年了。"他冷冷地说。

"十年的委屈，十年的不公。"

萧万擎冷笑："你还想怎样？"

"我不想怎样。"张逸臣转身，"我只想离开这个冷漠的家。"
```

**改进效果**：
- 对话比：从0%提升到80%
- 增加了视觉标记（眼神一冷、冷冷地、冷笑、转身）
- 增加了网文感关键词（冷冷地、冷笑、冷漠）
- 句长更短，节奏更快

---

### 示例2：增加视觉标记

**原文**（场景1，缺乏视觉标记）：
```
"把车钥匙交出来。"萧万擎说。
"我从来没有车。"张逸臣说。
"搜他的包。"林秀雪说。
```

**修改后**（增加视觉标记）：
```
"把车钥匙交出来。"萧万擎冷声道，眼神凌厉。
"我从来没有车。"张逸臣冷笑一声，眸光一沉。
"搜他的包。"林秀雪嘴角勾起一抹讥讽，不屑地挥手。
```

**改进效果**：
- 视觉标记：从0个增加到6个（冷声、眼神凌厉、冷笑、眸光一沉、嘴角勾起、不屑）
- 增加了网文感关键词（冷声、冷笑、讥讽、不屑）
- 画面感更强，情绪表达更充分

---

### 示例3：增加网文感关键词

**原文**（场景3，网文感不足）：
```
"你们会后悔的。"张逸臣说完，转身离开。
```

**修改后**（增加网文感关键词）：
```
"你们会后悔的。"张逸臣冷笑一声，眼神一冷，霸气地转身离开。

萧万擎嗤笑："狂妄。"

林秀雪不屑："不过是个养子。"

但他们没想到，这个被他们轻蔑的养子，竟然会成为他们的噩梦。
```

**改进效果**：
- 网文感关键词：从0个增加到7个（冷笑、眼神一冷、霸气、嗤笑、不屑、轻蔑、竟然）
- 增加了反转预告（没想到、竟然）
- 增加了悬念（噩梦）

---

## 七、总结

**核心问题**：
1. 对话比严重偏低（-28.6%）
2. 视觉标记严重不足（-3.1个/100字）
3. 网文感关键词缺失（-1.3个/100字）

**改进方向**：
1. 将叙述改为对话，提高对话比到70%+
2. 在对话后增加视觉标记，提升到4个/100字
3. 增加网文感关键词，提升到2个/100字

**预期效果**：
- 完成优先级1修改后，得分可从68分提升到91分
- 完成优先级1+2修改后，得分可达到95分以上

**下一步**：
1. 按照优先级1的建议修改剧本
2. 重新提交审核
3. 如果仍未达标，继续按照优先级2的建议修改
```

## 输出

输出到 `outputs/{剧本名}/review/one-by-one-comparison-ep<N>.md`

## 成功标准

1. 必须完成5次完整对比
2. 每次对比必须包含：评分、问题、示例、建议
3. 必须汇总共同问题
4. 必须给出优先级排序的改进建议
5. 必须提供具体的修改示例

## 注意事项

1. **逐个对比**：不要平均化，每个参考剧本都要单独对比
2. **具体引用**：必须引用参考剧本的具体片段
3. **可操作性**：建议必须具体、可执行，提供修改示例
4. **优先级**：按影响程度和工作量排序
5. **预期效果**：说明修改后的预期得分提升
