// Placeholder — scripts/make_vo.py overwrites this with the real voice-over timing.
// Each entry: { id, s, e, zh, en } in seconds; captions are drawn from it.
const VO = [
  { id: 'demo', s: 15.1, e: 19.6, zh: '示例字幕：中文一行。', en: 'Example caption: the spoken English line.' },
];
if (typeof window !== 'undefined') window.VO = VO;
