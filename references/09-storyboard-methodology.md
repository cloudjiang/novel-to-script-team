# 09. Storyboard Methodology

## Overview

This reference consolidates storyboard design principles and methodologies for converting scripts into visual sequences. It covers beat breakdown methodology, 9-grid Beat Board structure, 4-grid Sequence Board structure, and visual storytelling principles for dynamic comic and short drama production.

---

## Core Positioning

Storyboarding is the critical bridge between script and production. For dynamic comic scripts, while the primary output is the script itself, understanding storyboard thinking helps writers consider shot feasibility during writing.

**Core Principles**:
- Script is the treasure map, storyboard is digging for treasure—not retelling the map
- 90% of storyboard value lies in "supplementary shot" imagination
- Best storyboards are "silent"—core story understandable with sound off
- Always leave space in visuals for sound design
- **Non-Translation Principle**: Don't simply translate script actions into frames—transform them into "shot functions"
- **Cognition-Driven**: Create new shots only when audience's understanding shifts, not just when physical actions change
- **Subtraction Principle**: Fewer shots are better—pursue narrative precision

---

## First Principles

### Clarity (清晰)
Every storyboard frame must answer at a glance:
- Who is the focus?
- What is happening?
- What information/emotion does the audience receive?

All visual elements (setting, effects, atmosphere) must serve narrative, not overshadow it. Characters are always the focal point.

### Simplicity (简洁)
**One Frame, One Idea / Keyframe Principle**:
- Default: One shot or one story beat = one keyframe
- Only split into multiple frames (A/B/C) when shot choreography is complex or action must be tracked step-by-step
- Economy: If one frame tells it clearly, don't repeat the same information point
- Every shot must have clear narrative purpose; purposeless shots should be deleted

### Continuity (连贯)
Continuity trumps fancy tricks. Keep audience oriented:
- Stable spatial relationships (axis/left-right relations)
- Stable screen direction (facing/movement direction)
- Stable eyeline direction (dialogue/confrontation)
- Natural action connection (cut mid-action)
- Avoid jump cuts (insufficient angle and shot size variation)

**Axis Rules (轴线规则)**:
- **180° Rule**: Imaginary axis line between two characters/subjects; camera should stay on one side to maintain spatial consistency
- **When Axis-Crossing is Allowed**:
  1. **Higher Priority Content**: When content, rhythm, perspective, or composition cannot be balanced with axis maintenance, sacrifice axis
  2. **Better Composition**: When maintaining axis results in poor background/composition (e.g., wall vs. corridor)
  3. **Creating Effects**: Use axis-crossing to create confusion, tension, speed, or emotional shifts
  4. **Face-to-Face (对脸)**: When both characters face slightly toward each other in frame, creates acceptable shot-reverse-shot even with axis-crossing
- **Axis-Crossing Techniques**:
  - Insert neutral/cutaway shot between axis-crossing shots
  - Use character movement to naturally cross the axis
  - Employ camera movement to reestablish new axis

### Progressive Refinement (分层/渐进式优先)
Preferred workflow: Beat Breakdown → Beat Board (9-grid overview) → Sequence Board (4-grid expansion)
- Beat Board's role: "Select points and anchor"
- After generation, Beat Board serves as reference images for Sequence Board
- When generating 4-grid, use corresponding 9-grid frame as reference to ensure character and scene consistency

---

## Core Concepts & Terminology

### Story Beat (节拍)
- Minimum narrative unit: what happened + what audience gets (information/emotion/suspense)
- Beat intensity can be marked: low/medium/high (for rhythm design)
- Beat breakdown phase identifies all key beats, selecting 9 as anchors for 9-grid

### Shot (镜头)
- Basic unit of film/animation editing
- Storyboard "shot" must answer: what to shoot, how to shoot, why shoot this way
- **Shot Function**: Transform script actions into cognitive shifts, not just physical movements
- **Cognition-Driven Shot Splitting Rules**:
  - Create new shot only when:
    - Character's inner state or realization changes
    - Audience's understanding of background environment shifts
    - Spatial relationships redefine the narrative
  - Ignore physical actions if they don't change meaning or cognition
  - Rhythm controlled by pauses, not just action-driven

### Beat Board (九宫格总览板)
- 9 keyframes covering "narrative curve key turning points"
- Purpose: Clear narrative overview + unified visual anchors (characters/costumes/scene elements/light-color atmosphere)
- Engineering use: After generation, serves as reference images for Sequence Board
- Quantity relationship: Fixed 9 frames, corresponding to 9 key narrative turning points

### Sequence Board (四宫格/可变格展开板)
- Expands around one frame from the 9-grid, detailing continuous action/causal progression within a segment
- Default 4-frame structure: Setup—Development—Turn—Resolution (起—承—转—合)
- Frame count variable: 2/4/6 (determined by complexity)
- Generated using corresponding 9-grid frame as reference image, inheriting character/scene/light-color descriptions
- Quantity relationship: Each 9-grid cell can expand into one 4-grid set, maximum 9 sets

### Reference Image / Base Image (参考图片/垫图)
- Reference image input during AI image generation to maintain visual consistency
- In this workflow: One frame from 9-grid → serves as base image for that frame's corresponding 4-grid
- Purpose: Ensure 4-grid inherits 9-grid's character appearance, costume, scene, light-color
- Technical implementation: Input base image as image reference or style reference during AI generation

### Continuity (连贯性)
- Set of spatial and action continuation rules between shots (direction/axis/eyeline/props/action/edit points)

### Coverage (覆盖)
- Providing different shot sizes/angles for same beat/segment
- Common: Wide/establishing shot → medium shot for interaction/action → close-up/extreme close-up for emotion and detail

### Visual Style (视觉风格)
- Overall aesthetic style tendency of frames
- Common types: live-action realism, animation style, illustration style, cyberpunk, vintage film, etc.
- Default in this workflow: live-action realism (can be overridden by user)
- Once determined, must maintain style consistency throughout workflow (9-grid + 4-grid)

---

## Beat Breakdown Methodology

### Step 1: Script Analysis & Beat Breakdown

**Core Task**: Break down script using "emotional beat" as minimum unit

**Process**:
- Read through script, distill core dramatic purpose of each paragraph in one sentence
- Use "emotional beat" as minimum breakdown unit, strictly avoid vague "scene" units
- Mark all emotional turning points, information explosion points, atmosphere transition points
- Identify each character's core personality and relationship dynamics
- Judge script's genre type (action/dialogue/atmosphere/mixed) to predict overall rhythm baseline

**Key Metrics**:
- 1-2 minute finished product → typically produces 60-120 shots
- 500-word script ≈ 1.5 minutes duration
- Action/battle-heavy scripts lean toward upper limit, dialogue/atmosphere scripts toward lower limit

### Step 2: Beat Selection for 9-Grid

From all identified beats, select 9 key narrative turning points:

**Selection Criteria**:
1. **Opening Hook** (Frame 1): Establishes world tone, immediate visual impact
2. **Inciting Incident** (Frame 2): Core conflict trigger
3. **First Turning Point** (Frame 3): Protagonist's initial response/decision
4. **Rising Action Peak** (Frame 4): Conflict escalation
5. **Midpoint Reversal** (Frame 5): Major plot twist or revelation
6. **Crisis Deepening** (Frame 6): Situation worsens
7. **Darkest Moment** (Frame 7): Protagonist at lowest point
8. **Climax** (Frame 8): Ultimate confrontation/resolution
9. **Resolution/Hook** (Frame 9): Ending + potential sequel hook

**Balance Principle**:
- Ensure 9 frames cover complete narrative arc
- Avoid clustering too many frames in one segment
- Each frame should represent significant narrative progression

### Step 3: Beat Intensity Marking

Mark each beat's intensity (1-10 scale) for rhythm design:

| Intensity | Type | Characteristics |
|-----------|------|-----------------|
| 9-10 | 💥Explosion | Major reversal, identity reveal, ultimate face-slapping |
| 7-8 | 🔥Climax | Strong conflict, satisfaction release, emotional burst |
| 5-6 | ⚡Development | Conflict escalation, suspense building |
| 3-4 | 🔨Pressure | Setback, humiliation, crisis accumulation |
| 1-2 | 🌊Calm | Transition, setup |

---

## 9-Grid Beat Board Structure

### Purpose & Function

**Primary Functions**:
1. **Narrative Overview**: Visualize complete story arc at a glance
2. **Visual Anchoring**: Establish consistent character designs, costumes, scene elements, lighting, and color palette
3. **Reference Foundation**: Each frame serves as base image for corresponding 4-grid expansion

### Frame Composition Requirements

Each of the 9 frames must include:

**Visual Elements**:
- **Character Design**: Clear character appearance, costume, distinctive features
- **Scene Setting**: Location, environment, key props
- **Lighting & Color**: Mood-appropriate lighting scheme and color palette
- **Composition**: Clear focal point, visual hierarchy
- **Emotional Tone**: Visual representation of beat's emotional content

**Descriptive Elements** (for AI generation):
- Shot size (wide/full/medium/close-up/extreme close-up)
- Camera angle (eye-level/low-angle/high-angle/Dutch angle)
- Composition technique (rule of thirds/leading lines/frame within frame)
- Lighting quality (soft/hard/dramatic/natural)
- Color palette (warm/cool/desaturated/vibrant)
- Atmosphere keywords (tense/peaceful/ominous/hopeful)

### 9-Grid Layout Template

```
┌─────────┬─────────┬─────────┐
│ Frame 1 │ Frame 2 │ Frame 3 │
│ Opening │ Inciting│ First   │
│ Hook    │ Incident│ Turn    │
├─────────┼─────────┼─────────┤
│ Frame 4 │ Frame 5 │ Frame 6 │
│ Rising  │ Midpoint│ Crisis  │
│ Action  │ Reversal│ Deepens │
├─────────┼─────────┼─────────┤
│ Frame 7 │ Frame 8 │ Frame 9 │
│ Darkest │ Climax  │ Resolut-│
│ Moment  │         │ ion/Hook│
└─────────┴─────────┴─────────┘
```

### Consistency Maintenance

**Critical Consistency Points**:
- Character appearance must remain identical across all 9 frames
- Costume changes only if narratively justified
- Scene elements maintain spatial logic
- Lighting/color palette shifts only for dramatic effect
- Visual style remains uniform

---

## 4-Grid Sequence Board Structure

### Purpose & Function

**Primary Functions**:
1. **Action Expansion**: Detail continuous action/causal progression within a segment
2. **Shot Choreography**: Plan specific shot sequences for production
3. **Rhythm Control**: Fine-tune pacing through shot duration and cutting frequency

### Default 4-Frame Structure (起承转合)

**Frame A - Setup (起)**:
- Establish spatial context
- Introduce characters/objects in play
- Set emotional baseline
- Typical shot: Wide or establishing shot

**Frame B - Development (承)**:
- Action begins or dialogue progresses
- Conflict builds
- Information revealed
- Typical shot: Medium shot for interaction

**Frame C - Turn (转)**:
- Climax of the sequence
- Key action/revelation/emotional peak
- Highest intensity moment
- Typical shot: Close-up or dynamic angle

**Frame D - Resolution (合)**:
- Immediate aftermath/reaction
- Transition to next sequence
- Often includes hook for continuity
- Typical shot: Reaction shot or transitional shot

### Variable Frame Count

**2-Frame Sequence**: Simple action or quick exchange
- Setup → Payoff
- Question → Answer

**4-Frame Sequence** (Default): Standard narrative progression
- Setup → Development → Turn → Resolution

**6-Frame Sequence**: Complex action or extended dialogue
- Setup → Development A → Development B → Turn → Aftermath → Resolution

### Expansion Guidelines

**When to Expand from 9-Grid to 4-Grid**:
- Complex action sequences requiring choreography breakdown
- Important dialogue scenes needing reaction shots
- Key emotional moments requiring detailed coverage
- Climactic confrontations

**When to Keep Minimal**:
- Simple transitions
- Quick information delivery
- Establishing shots without action
- Montage sequences

---

## 7-Step Storyboard Execution Process

### Step 1: Script Analysis & Beat Breakdown
(Covered in Beat Breakdown Methodology section above)

### Step 2: Pre-Construction (Opening Introduction)

**Core Task**: Add visual introduction shots to establish world tone

Add 5-15 dialogue-free visual introduction shots based on genre:
- Action/epic genres lean toward more, comedy/daily life toward fewer
- First shot defines world tone (oppressive/grand/eerie/romantic)
- Default: avoid mundane wide shot opening, prioritize close-up details then reveal full view
- Camera movement ceremonial: slow, smooth, guiding audience into world
- Weather, lighting, dynamic elements (wind/light-shadow changes) used to extreme
- Plant "visual symbols" related to core conflict
- Protagonist entrance setup: subjective POV → traces left behind → others' reactions
- Final frame must be strong suspense hook

### Step 3: Character Establishment

**Core Task**: Design "character-defining shots" for each major character

- Each major character gets dedicated "personality shot" (doesn't advance plot, only defines character)
- Externalize core personality through signature "habitual actions"
- When no dialogue or action, must be in "parallel reaction chain," strictly avoid standing idle
- Each major character gets at least one "eye close-up shot"

### Step 4: Shot-by-Shot Storyboard Creation

**Core Task**: Transform script into specific shot sequence

**Shot Size Control**:
- Beware unconscious shot size repetition
- Three or more consecutive same-size shots require clear rhythm or emotional purpose
- Comprehensively use multiple sizes, angles, compositions

**Action Breakdown**:
- Break action into "wind-up → process → impact → reaction" four-shot chain
- Single action cannot be covered in one shot, must be broken down

**Dialogue Handling**:
- Dialogue defaults to shot breakdown
- When emotional continuity or character tension requires, can keep long take for complete presentation (e.g., monologue, declaration)
- Single line shot chain (default): speaker wind-up → listener reaction → speaker climax → post-line reaction
- Character speaking should have simultaneous "parallel task" (action/expression/environment interaction), avoid standing recitation
- Listener reaction more important than speaker's words
- Each dialogue segment gradually introduces, gradually exits, avoid flash in/out

### Step 5: Transition Logic Design

**Core Task**: Design transition logic between shots

- Each shot cut should be tagged with transition logic label
- Scene/emotion jumps must be tagged with **[Primary Logic + Secondary Logic]** compound tags
- Continuous shots with natural transitions allow single tags
- Same-frame transition priority: in character interaction scenes, prioritize pan/focus shift/character blocking transitions
- Hard cut is legitimate basic editing language, but needs rhythm or emotional motivation
- Skillfully use J-Cut (sound leads) or L-Cut (picture leads) to enhance emotional connection between scenes
- Action Match is one of the most powerful editing techniques

**Available Transition Tags**:
Action Match | Emotional Causality | Eyeline Guide | Dialogue Drive | Sound Bridge | Same-Frame Transition | Focus Shift | Character Blocking | Match Cut | J-Cut | L-Cut | Logical Causality | Contrast | Rhythm Hard Cut

### Step 6: Rhythm Control

**Core Task**: Control rhythm through shot duration and cutting frequency

- Fast rhythm (action/explosion/intense) → dense beat editing
- Slow rhythm (brewing/display/atmosphere) → extended single frames, long takes
- Goal: tension and release, guide audience emotional flow

### Step 7: Quality Self-Check

Complete storyboard, check each item:

1. Does each shot serve at least two of "narrative, character, emotion"?
2. Are there unconscious consecutive same-size shots? (Deliberate repetition excepted)
3. Do scene/emotion jumps all have compound transition logic tags?
4. Have dialogue shots been properly broken down? (Complete presentations have clear creative motivation?)
5. Does total shot count match genre rhythm? (Not mechanical padding, nor lazy reduction)
6. With sound off, can at least 60% of story and emotion be understood? (Action/visual narrative target 80%, dialogue-driven target 60%)

---

## Advanced Storyboard Rules

### Module A: Character Depth Shaping

**Dynamic Charisma Principle**:
- Charisma must be dynamic: one moment's micro-movement > ten seconds static close-up
- Design "signature posture shot" for each major character showcasing core temperament (from character personality, not gender)

**Emotional Moment Capture**:

**Vulnerable Moments**:
- Capture most unguarded details in body language
- Examples: trembling fingertips, unfocused eyes, unconscious self-soothing actions

**Resolute Moments**:
- Backlit/sidelit silhouette lines
- Emphasize power in posture

**Emotional Overflow**:
- Close-up captures physical trajectory of emotion
- Examples: tear rolling path, clenched fist knuckles whitening, uncontrolled mouth twitch

**Antagonist Shaping**:
- Entrance accompanied by "environmental imbalance": light darkens / sound disappears / composition tilts
- Design unsettling repetitive "pathological micro-actions"
- Laughter must have layers: contempt / cruelty / self-mockery / madness
- Oppression comes from psychological pressure on other characters when "not moving"

### Module B: Advanced Camera Language

**Angle Selection**:
- Eye-level is neutral default perspective
- Low-angle for oppression or power dynamics
- High-angle for smallness or helplessness

**Cinematic Composition Principles (电影化构图原则)**:
- **Character Presentation Diversity**:
  - **Size Variation**: Dramatic use of character's screen proportion across extreme close-up/close-up/medium/full/wide shots
  - **Position Variation**: Centered/off-center/corner/background/absent—each carries narrative meaning
  - **Angle Variation**: Eye-level/low-angle/high-angle/profile—each expresses different emotion
- **Environment as Narrative Participant**:
  - **Background Evolution**: How environment changes with plot progression
  - **Atmosphere Creation**: Light, weather, architecture serving emotional expression
  - **Spatial Relationships**: Character-to-environment proportion ratio conveys narrative meaning
- **Avoid Template Composition**:
  - Don't center characters in every shot
  - Use character size variation to express emotion and narrative focus
  - Fully utilize environmental elements to tell story
  - Composition serves dramatic rhythm and emotional expression
  - Pursue cinematic expressiveness in shot language

**Special Composition**:
- Character inner unease → Dutch angle (tilted composition)
- Use "foreground framing" to add depth and voyeuristic feel

**Over-the-Shoulder (OTS)**:
- Shoulder distance and focus in OTS shots express character relationships

**Focal Length Application**:
- Deep focus shows character relationships
- Shallow focus highlights inner world

**Close-up Principle**:
- Giving object close-up = declaring "it's important," cannot be overused

**Eyeline Guide**:
- Character eyeline direction is core means of controlling audience attention

**Movement Space**:
- Moving objects must leave more space in frame for movement direction

### Module C: Precision Action Breakdown

**Four-Shot Chain Extended Rules**:

**Wind-up Shot**:
- "Wind-up" shot must clearly convey character "intent"

**Impact Shot**:
- "Impact" shot must include physical feedback: dust/vibration/shattering

**Injury Reaction**:
- First reaction to injury should be determined by character personality
- Examples: soldier grits teeth / child screams / villain laughs / ordinary person instinctive spasm
- Avoid cookie-cutter responses

**Death Design**:
- Character death = design a "visual symbol" carrying character's life force, make it disappear or change at death
- Examples: object slipping from hand is just one option, can also be light extinguishing, rhythm stopping, frame color draining, etc.

### Module D: Dialogue Breakdown Refinement

**Dialogue Breathing**:
- Break down with surgical precision based on comma pauses, tone intervals, single-word information density, speech feel, and emotional layers

**Comma Opportunities**:
- Commas in dialogue = opportunity to insert "listener micro-expression" shot

**Pause Utilization**:
- Pauses in dialogue = insert information-rich environment/detail shot

**Emotional Aftertaste**:
- After dialogue ends, hold "half a beat" before cutting away, leave emotional aftertaste space

**Shot-Reverse-Shot Advanced**:
- Shot-reverse-shot continuously varies in angle, shot size, focal length, avoid mechanical repetition

**Subtext Technique**:
- Character A speaks, camera gives Character B's reaction close-up

**Three-Shot Principle**:
- One complete line defaults to three shots: speaker, listener, silent air

---

## Relationship to Script Writing

While dynamic comic scripts' primary output is script not storyboard, understanding storyboard thinking helps:

1. **Consider Shot Feasibility While Writing**: Avoid writing scenes difficult to shoot
2. **Enhance Visual Sense**: Scene descriptions in script more specific, more shot-conscious
3. **Optimize Dialogue Design**: Understanding dialogue needs breakdown, consider reaction shot space while writing
4. **Improve Rhythm Control**: Understanding shot cutting rhythm, control emotional beats while writing

### For Dynamic Comic Script Work

- **Writing Script**: Don't need detailed storyboard, but need "shot awareness"
- **First Episode Text**: Can appropriately mark key shots (e.g., "Close-up: Li Zhe's shocked expression"), help reviewers understand visuals
- **Self-Check Phase**: Use "can story be understood with sound off" standard to check script's visual narrative ability
- **Advanced Needs**: If client requires storyboard script output, can use these rules for secondary creation

---

## Output Format

Output as table with 8 columns:

| Shot # | Script Reference | Size/Angle/Composition | Visual Description | Emotion & Rhythm | Sound Design | Transition Logic | Camera Movement |
|--------|------------------|------------------------|-------------------|------------------|--------------|------------------|-----------------|
| S001 | Original quote or "Supplementary Shot" | e.g., Extreme Wide/Low Angle/Golden Ratio | Detailed frame content: character action, expression, environment detail, light-shadow, dynamic elements | e.g., Oppressive→Tense, Slow Rhythm | Ambient sound/SFX/music/silence | [Primary+Secondary] or [Single Tag] | Slow push/pan/static etc. |

**Output Rules**:
- Must output completely from start to finish, strictly no omission, summarization, abbreviation
- If length limited, output in batches of 30-40 shots, mark "【Continued】" at end of current batch
- Maintain continuous shot numbering across batches

---

## Quality Checkpoints

### Pre-Production Checklist

Before starting storyboard:
- [ ] Beat breakdown completed
- [ ] 9 key narrative turning points identified
- [ ] Visual style determined
- [ ] Target aspect ratio confirmed (16:9 or 9:16)
- [ ] Character designs established

### Per-Frame Checklist (9-Grid)

For each Beat Board frame:
- [ ] Clear focal point (who/what)
- [ ] Narrative purpose明确 (information/emotion delivered)
- [ ] Visual consistency with other frames (character/costume/style)
- [ ] Appropriate shot size and angle
- [ ] Lighting and color support emotional tone
- [ ] Composition guides viewer's eye effectively

### Per-Sequence Checklist (4-Grid)

For each Sequence Board:
- [ ] Inherits visual consistency from corresponding 9-grid frame
- [ ] 起承转合 structure complete
- [ ] Shot sizes vary appropriately
- [ ] Transition logic clear
- [ ] Action/dialogue properly broken down
- [ ] Rhythm appropriate for content

### Final Review Checklist

Before delivery:
- [ ] All shots serve narrative/character/emotion (at least 2 of 3)
- [ ] No unconscious shot size repetition
- [ ] Transition logic tagged appropriately
- [ ] Dialogue properly broken down with reaction shots
- [ ] Total shot count matches genre rhythm
- [ ] Story 60%+ understandable with sound off

---

## Common Mistakes

### Over-Design
- Not every character needs signature posture shot
- Not every dialogue needs three-shot principle
- Not every action needs four-shot chain

### Ignoring Rhythm
- Advanced rules cannot break overall rhythm
- Refinement ≠ dragging
- Detail cannot affect fluidity

### Form Over Content
- Technique must serve story
- Don't use technique for technique's sake
- Audience feeling more important than technical perfection

---

## Reference Cross-Links

- See **08-camera-and-cinematography.md** for detailed camera techniques
- See **10a-action-dialogue-scenes.md**, **10b-atmosphere-fantasy.md**, **10c-suspense-montage.md** for scene-specific storyboard approaches
- See **02-episode-architecture.md** for episode-level rhythm and pacing
- See **06-storyboard-handoff.md** for production handoff procedures

---

## Supplementary: Movement & Momentum (运动与动势)

### Understanding Movement Through Momentum (动势)

**Momentum (动势)**: Directional movement—understanding complex motion as a color block moving up/down/left/right/forward/backward within the frame

**How to Judge Momentum**:
- Squint your eyes (blur vision) when watching a shot sequence
- The directional movement of the main subject's color block within the frame = the shot's momentum

### Applications

**1. Smooth Transitions**:
- For smooth shot connections, adjacent shots should have momentum in the same direction
- Left connects to left, right connects to right
- Change momentum only within a single shot, not between shots
- Momentum continuity works even when subjects differ between shots

**2. Simplify Creative Process**:
- When designing complex movement, first imagine subject as simple color block
- Design the color block's momentum
- Then add specific actions
- Creating in two layers reduces difficulty

**3. Rhythm Control**:
- Smooth, same-direction momentum = one rhythm
- Adjacent shots with opposite momentum = different rhythm (conveys faster pace)
- Design different rhythms for different segments to create rhythm variation
- Rhythm variation creates dramatic peaks and valleys, preventing flat storyboards

---

---

## Beat 作为叙事-镜头桥梁（皮克斯方法论）

> 来源：154-动态漫工业流程定位、155-叙事单元粒度（2026-03-12 收编）

### 动态漫在工业流程中的定位

当前 AI 漫/动态漫 ≈ 传统动画工业的 Step 4（Animatic/动态分镜），即"让分镜图动起来"。完整动画工业流程10步中，动态漫停在前4步：

1. 剧本与概念 → 2. 故事板 → 3. 配音录制 → **4. 动态分镜（≈ 当前AI漫）** → 5-10. 资产/布局/动画/特效/渲染/合成

### 三种粒度单位

| 单位 | 角色 | 决定什么 |
|------|------|---------|
| Beat（叙事节拍） | 叙事生产单位 | 旁白与镜头的对齐锚点 |
| Layout（场景） | 视觉资产单位 | 布景、材质、光照、资产复用 |
| Shot（镜头） | 视觉生成单位 | 交给视频模型的最小单元 |

**关键**：一个 Beat 可以有旁白也可以纯画面；一个 Beat 内的镜头共享同一段旁白；Beat 是时间轴的最小可控单元。

### "先让听觉成立"原则

皮克斯/流媒体团队的核心方法：
1. 先把"听得懂、听得顺"的版本做出来（旁白+临时音频）
2. 再决定需要多少画面去支撑它
3. 如果"像广播剧一样只听声音都不成立"，后面一定会出问题

### Beat Board 工作流

1. 先用 Beat Boards 当占位（比正式分镜更粗，几张关键插画）
2. 配旁白，让团队先看懂"这一段在讲什么"
3. 在 Story Reel 阶段反复锤节奏
4. 确认后再展开成正式镜头（Shot）

---

**Last Updated**: 2026-03-12
**Source Priority**: A-priority (consolidated from sources/new-reference-skills/, references/04-镜头与分镜/, and pending-knowledge/split/)
**Maintenance**: Update when new storyboard methodologies are validated