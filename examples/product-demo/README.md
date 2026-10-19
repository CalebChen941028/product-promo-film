# Worked example: a physical product, no music supplied · 实物产品示例（无音乐）

**Aurel Stoneware** is a *placeholder* brand. The images in `materials/` are drawn placeholders made by `make_placeholders.mjs`; they are not photographs of a real product.

## English
This is the "any product" path end to end:
1. `materials/` holds what a user would hand over: three cut-outs (transparent PNG), three photos, a logo and a README. There is **no music**.
2. `python3 ../../scripts/autofilm.py materials --out .` produced:
   - genre **food-beverage**, look **natural-fresh**, motion **gentle-story**, arc **sensory**;
   - a composed **warm-acoustic** underscore;
   - 8 scenes cast from the materials (cover → photo → detail → hero → feature → lineup → finale → end card);
   - `film.json` with TODO copy and `treatment.md`.
3. The crew (`references/crew.md`) wrote `treatment.md`: three concepts, chose **"One of one"** (every glaze is unique), wrote the hook, the hero moment, the tagline (每一只，都只有一只 / One of one), the script and the taste review. `check_treatment.py` passes.
4. The copy went into `film.json`; then `make_film.py film.json` ran (check → build → voice → QA 0 errors → render → finish).

Try other looks on the same material: `"style": "luxe-noir"` (quiet luxury) or `"keynote-light"`.

## 中文
这是“任何产品”路线的完整示例：
1. `materials/` 里是用户会交来的东西：三张透明底产品图、三张照片、一个 Logo 和一份 README，**没有音乐**。
2. `autofilm.py` 自动判断为**食品饮品**类，选定 **natural-fresh** 风格、**gentle-story** 动效、**感官叙事**结构，并原创 **warm-acoustic** 配乐，把素材分配到 8 个场景，写出草稿。
3. 团队（`references/crew.md`）填写了 `treatment.md`：三个概念中选定“每一只，都只有一只”（每一层釉都独一无二），写出开场、高潮、口号、旁白与品味评审，`check_treatment.py` 通过。
4. 把文案写进 `film.json`，再运行 `make_film.py` 完成全部流程（QA 0 错误）。

同一套素材可以换风格试试：`"style": "luxe-noir"`（安静的奢华感）或 `"keynote-light"`。
