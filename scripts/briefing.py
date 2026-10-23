#!/usr/bin/env python3
"""The briefing: before any work, show the user what this skill will do, what it will not do, what it needs from them,
and how long it takes — then wait for their confirmation (and their answers). Once per project.

  python3 briefing.py --project <project dir> [--materials <folder>] [--source <repo>] [--lang zh|en|both]
      prints the briefing (and writes <project>/briefing.md), shaped by what is already known: the materials found,
      a source repo, music. Show it to the user as it is, then WAIT.
  python3 briefing.py --project <project dir> --ack "<the user's reply, in their words>"
      records the confirmation (<project>/briefing.json); autofilm.py refuses to draft a project without it.
  python3 briefing.py --project <project dir> --ack "…" --assumed
      only when the user cannot be asked (a batch run): the report must say the briefing was not confirmed.
"""
import argparse, datetime, json, sys
from pathlib import Path

IMG = {'.png', '.jpg', '.jpeg', '.webp'}
VID = {'.mp4', '.mov', '.m4v', '.webm', '.mkv'}
AUD = {'.mp3', '.wav', '.m4a', '.aac', '.flac'}
DOC = {'.md', '.txt', '.pdf', '.docx', '.json'}


def survey(folder):
    if not folder or not Path(folder).is_dir(): return None
    c = {'images': 0, 'videos': 0, 'music': 0, 'docs': 0}
    for p in Path(folder).rglob('*'):
        if not p.is_file() or p.name.startswith(('.', '_')) or p.name.endswith('.regions.json'): continue
        e = p.suffix.lower()
        k = 'images' if e in IMG else 'videos' if e in VID else 'music' if e in AUD else 'docs' if e in DOC else 'other'
        c[k] = c.get(k, 0) + 1
    return c


def text(a, sv):
    zh, en = [], []
    have_zh = (f'已找到素材：图片 {sv["images"]}、视频 {sv["videos"]}、音乐 {sv["music"]}、文档 {sv["docs"]}。' if sv else '还没有素材文件夹：可以给我截图、照片、视频、Logo、说明文档，或已安装的应用 / 网址，我来采集真实界面。')
    have_en = (f'Materials found: {sv["images"]} images, {sv["videos"]} videos, {sv["music"]} music, {sv["docs"]} documents.' if sv else 'No materials folder yet: give me screenshots, photos, clips, a logo, docs — or the installed app / a URL, and I capture the real UI.')
    src = bool(a.source)
    zh += ['# 宣传片制作 · 开工前说明', '',
           '请花一分钟看完，回复确认（并回答末尾的问题）后我再开始。', '',
           '## 我会怎么做',
           '1. 读懂产品与素材（' + have_zh + '）',
           '2. 导演给出 2–3 套方向（风格、动效、节奏、配色），每套附真实素材渲染的预览，**由你选择或修改**。',
           '3. 团队写创意方案与中英文案，配音（Kokoro 合成）、配乐（你的曲子或原创）、字幕、自动质检，渲染 1080p 成片、封面、字幕文件。',
           '4. 汇报：文件位置、哪些是演示 / 占位 / 原创，以及你还需要补什么。', '',
           '## 我不会做的（限制）',
           '- 不画假界面、不伪造产品冒充真实；只用真实素材。按源码重绘的界面只在你同意后使用，并在画面上标注“界面示意”。',
           '- 数字、规格、医疗 / 金融 / 隐私类说法必须能在你的文档里查到；查不到就不说。版本限制（如专业版、内测）会如实标注。',
           '- 不从网上找音乐、图片或视频；不用真人肖像；不使用未授权的引言。',
           '- 不替你填写 API Key、密码；不进入设置、授权、支付、删除等界面（除非你要求）。',
           '- 不结束你正在使用的程序；' + ('运行产品源码录制真实界面前会单独征得你同意（沙盒、演示数据、只访问本机）。' if src else '未经同意不运行产品源码。'),
           '- 下载任何模型或音色前先征得同意。', '',
           '## 你需要知道的',
           '- 你提供的素材、音乐、Logo、文档的使用权由你负责；片中的演示数据、AI 生成的配音与配乐会注明。',
           '- 我听不到混音效果，声音请你亲自检查；成片请你审核后再对外发布。',
           '- 时间：采集素材约 15 分钟，方案与文案约 20–40 分钟，渲染约 5–20 分钟（视时长而定）。', '',
           '## 请回复（能答多少答多少，没答的我按默认处理并在汇报中说明）',
           '1. 确认以上说明。',
           '2. 想要的感觉，用你自己的话（如：大气商业 / 温暖人文 / 简洁克制 / 严谨学术 / 年轻活泼）。',
           '3. 时长与画幅（默认横屏 1–3 分钟）；面向谁、在哪里播放。',
           '4. 音乐：用你的曲子（给文件）还是原创配乐；配音语言（中文 / 英文 / 双语字幕）。',
           '5. 结尾联系方式与行动号召（如官网、邮箱、“参与内测”）。',
           '6. 必须出现或必须避免的内容。'] + (['7. 是否允许我在沙盒里运行源码录制真实界面；是否可以按源码重绘无法录制的流程（会标注“界面示意”）。'] if src else []) + ['']
    en += ['# Promo film · before we start', '',
           'Please read this (one minute) and reply to confirm — with your answers to the questions at the end — before I begin.', '',
           '## What I will do',
           '1. Understand the product and the materials (' + have_en + ')',
           '2. The director proposes 2–3 directions (look, motion, pace, colour), each with a preview rendered from your real materials — **you choose or change**.',
           '3. The crew writes the treatment and bilingual copy; voice-over (Kokoro), music (your track or an original score), captions, automatic QA; render a 1080p film, poster and subtitles.',
           '4. Report: where the files are, what is demo / placeholder / composed, and what you still need to supply.', '',
           '## What I will not do (limits)',
           '- No fake UI and no fake product passed off as real; real material only. A UI redrawn from the source is used only with your yes, and labelled "Illustrative UI" on screen.',
           '- Numbers, specs, health / finance / privacy claims must be found in your docs, or they are not said. Edition limits (Pro, beta) are stated.',
           '- No music, images or video from the web; no real people; no quotes you have not approved.',
           '- I never type your API keys or passwords, and stay out of settings, licence, payment and delete screens unless you ask.',
           '- I never close programs you are using; ' + ('running the product from its source to record its real UI needs your separate yes (sandbox, demo data, localhost only).' if src else 'I do not run the product\'s source code without your yes.'),
           '- I ask before downloading any model or voice.', '',
           '## Good to know',
           '- You are responsible for the rights to the materials, music, logo and documents you give me; demo data and the AI voice and music are labelled.',
           '- I cannot hear the mix: please listen; please review the film before you publish it.',
           '- Time: capture about 15 min, proposals and copy 20–40 min, rendering 5–20 min.', '',
           '## Please reply (answer what you can; what you skip I set by default and say so in the report)',
           '1. Confirm the above.',
           '2. The feel, in your own words (big and cinematic / warm and human / clean and calm / rigorous / young and playful).',
           '3. Length and format (default: landscape, 1–3 min); who it is for and where it plays.',
           '4. Music: your track (the file) or an original score; voice-over language (Chinese / English / bilingual captions).',
           '5. End card contacts and call to action (site, email, "join the beta").',
           '6. Anything that must appear, or must not.'] + (['7. May I run the source in a sandbox to record the real UI; may I redraw flows that cannot be recorded (labelled "Illustrative UI")?'] if src else []) + ['']
    return '\n'.join(zh if a.lang == 'zh' else en if a.lang == 'en' else zh + ['---', ''] + en)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--project', required=True); ap.add_argument('--materials'); ap.add_argument('--source')
    ap.add_argument('--lang', choices=['zh', 'en', 'both'], default='both')
    ap.add_argument('--ack'); ap.add_argument('--assumed', action='store_true')
    a = ap.parse_args()
    proj = Path(a.project).resolve(); proj.mkdir(parents=True, exist_ok=True)
    if a.ack is not None:
        if not a.ack.strip(): sys.exit('ERROR --ack needs the user\'s reply in their words')
        rec = {'confirmed': True, 'by': 'assumed' if a.assumed else 'user', 'reply': a.ack.strip(), 'at': datetime.datetime.now().isoformat(timespec='minutes')}
        json.dump(rec, open(proj / 'briefing.json', 'w'), ensure_ascii=False, indent=2)
        print(f'briefing confirmed ({rec["by"]}) → {proj / "briefing.json"}. Use the answers in the reply (feel → autofilm --mood, music, voice, contacts).')
        return
    t = text(a, survey(a.materials))
    (proj / 'briefing.md').write_text(t)
    print(t)
    print(f'\n(written to {proj / "briefing.md"}) — show this to the user as it is, then WAIT for their reply; record it with --ack "<their words>".')


if __name__ == '__main__':
    main()
