# Copy bank · 文案范例库

English first, 中文在后。For the copywriter and the creative director. Learn the moves here, then write **your** product's lines from **your** docs. Never paste a line from this page: `check_treatment.py` checks that every proof line carries a fact from your own README or brief.

Full films that use these moves: `templates/golden/<arc>.json` (one per story arc, every scene with a `_why`) and `examples/product-demo/` (built and rendered).

## English

### 1. Write the three anchor lines first
A film is remembered by three lines. Write them before anything else, and make each one say the chosen concept in a different way:

| Anchor | Where | Job | Example (golden films) |
| --- | --- | --- | --- |
| **Hook** | cover, 0–3 s | a true tension, a question, or a physical detail, before the product | "The translation took a week. The invoice took the evening." |
| **Hero** | finale, ~65 % | the proposition in ≤ 6 words, with the name | "Halden. Light that keeps the time." |
| **Last** | end card | a callback: echo a word or image of the hook, and land on the viewer | "The translation takes a week. The invoice takes a minute." |

Then every other line is proof: one fact from the docs per line, said as what it means for the viewer.

### 2. Rewrites: what mid-sized models write, and what a top copywriter writes
| Weak (the patterns seen in tests) | Why it is weak | Strong (golden films) |
| --- | --- | --- |
| "Word counts for DOCX, PDF and XLIFF, 31 currencies, reminders and CSV export." | a spec list read aloud | "Drop in the source file. Margin counts the words and prices them at your rate." |
| "Hand-raked, oak-smoked, harvested April to September, in a 120 g tin." | four facts, no picture | "Raked by hand. Smoked over oak for forty-eight hours." |
| "Open weekdays until 9 pm. Book online or by phone." (last line) | logistics as the ending | "Come after five. We're here until nine." — the booking details go in the contacts |
| "Discover a new way to season your food." | could sell any product | "Add it last. A pinch is enough." |
| "Fair prices. Faster invoices. Happier clients." (tagline) | three ideas in one tagline | "Finish the work. Not the paperwork." |
| "Experience perfect light, all day." | vague words (lint flags them) | "Clear white at noon. Amber after sunset." |
| "Powerful, easy, fast." | adjectives | a verb and a noun: "Drop the file. Get the price." |
| "Machined aluminium, 9 W, CRI 97, two finishes." | an attribute list (`lint_copy` flags it) | one benefit: "Arm and base, turned from one bar of aluminium." — the rest goes to points or the end card |
| a film whose chosen concept appears only in the treatment | the idea never reaches the screen | the concept's key image or word is in the hook, the hero line and the last line |

### 3. Moves that work (pick one per beat)
- **Contrast in two sentences:** "X took a week. Y took the evening."
- **The number with its unit and its source:** "On 200 real bugs, the median repro was three files."
- **Place and time:** "In one bay on the Yorkshire coast, April to September."
- **A verb the viewer does:** "Drop in the file." "Add it last."
- **Silence:** a scene with no voice (detail, lineup) right after two lines of facts.
- **The callback:** the last line reuses a word of the first.

### 4. By genre: tone, and where the facts usually are
| Genre | Tone | Facts to look for in the docs | Avoid |
| --- | --- | --- | --- |
| software-saas, finance-fintech | calm competence | minutes saved, steps removed, file types, integrations, price | "streamline", "all-in-one", dashboards with no story |
| science-data | precise, reviewer-proof | methods by name, what can be reproduced, export formats, DPI | reading a methods list aloud |
| developer-ai | dry, exact, a little wit | commands, benchmarks with sample size, what runs locally, licence | "AI-powered", hype verbs |
| mobile-consumer-app | light, personal | the moment in a day, taps, what you get | "fun", "amazing" |
| consumer-electronics, mobility-industrial | engineered, quiet | materials, tolerances, units (K, mm, h), where it is made | "premium build", "stunning" |
| fashion-beauty-luxury | sensory, sparse | fibre, origin, hand steps, number made | "luxury", "elegant" |
| food-beverage | appetite and origin | place, season, time (hours smoked), size of the batch | "delicious", "artisanal" with no facts |
| travel-hospitality-living | atmosphere, invitation | distance, what is NOT there, season, how many guests | "getaway", "paradise", "escape" |
| health-wellness | warm, careful, honest | hours, minutes, who you see, how to book; health claims only from a source | promises of cure |
| education-learning, kids-family | warm, human | minutes per day, ages, what the learner does | "unlock potential" |
| brand-mission | conviction | what the organisation actually did, with numbers | "making the world a better place" |

### 5. Chinese captions
Write natural Chinese, not a translation. Shorter than the English (≤ 30 字 per caption, ≤ 12 字 per label); keep the numbers. Two pairs: "Raked by hand. Smoked over oak for forty-eight hours." → 手工耙取，橡木烟熏 48 小时。 "Finish the work. Not the paperwork." → 收尾的事，交给 Margin。

## 中文

### 1. 先写三句“锚点”
观众记住一部片子靠三句话，先写它们，每句都用不同方式说出选定的创意：
- **开场钩子**（封面，0–3 秒）：一个真实的矛盾、一个问题或一个具体细节，产品先不出现。
- **高潮句**（finale，约 65% 处）：≤ 6 个词的主张，带上品牌名。
- **收尾句**（结尾页）：首尾呼应，重复开场的一个词或画面，并落在观众身上。

其余每句都是证据：每句一个文档里的事实，讲成对观众意味着什么。

### 2. 改写：中型模型常写的 vs. 顶级文案会写的
见上方英文表格：规格清单式旁白、几个事实堆在一句、用营业时间结尾、“探索全新方式”式空话、一个口号塞三个意思、形容词堆砌、选定的创意没有出现在片子里——各有改法。

### 3. 好用的手法（每个拍点选一个）
两句对比；带单位和来源的数字；地点与时间；观众会做的动作；静默（连续两句事实后给一个无旁白的场景）；首尾呼应。

### 4. 按类型：语气与事实来源
见上方英文表格：每类产品的语气、文档里通常能找到的具体事实、以及要避免的空话。

### 5. 中文字幕
写自然的中文，不要逐字翻译；比英文更短（字幕 ≤ 30 字，标签 ≤ 12 字），保留数字。
