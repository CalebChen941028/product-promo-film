// Scripted local "model" with an OpenAI-compatible API, for filming AI features without a cloud key.
// Point the app at it as a local provider (Ollama default base URL http://localhost:11434/v1).
// Usage: DELAY=45 node mock_llm.mjs [port=11434] [replies.json]
//
// replies.json: [{ "match": "<regex>", "reply": "<markdown>" }, …] — the FIRST entry whose regex matches the
// whole conversation text wins, so put specific matches first and a "." catch-all last.
// Honesty: write replies from the product's REAL results for the same demo data, and tell the user the AI
// text in the film came from this mock. Every request is appended to mock_requests.log for inspection.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const port = Number(process.argv[2] || 11434);
const repliesPath = path.resolve(process.argv[3] || 'replies.json');
const delay = Number(process.env.DELAY || 45); // ms per 4-character chunk; raise it to slow the on-screen stream
const pick = (msgs) => {
  const replies = JSON.parse(fs.readFileSync(repliesPath, 'utf8'));
  const text = msgs.map((m) => (typeof m.content === 'string' ? m.content : JSON.stringify(m.content))).join('\n');
  fs.appendFileSync('mock_requests.log', `--- ${new Date().toISOString()}\n${text.slice(-4000)}\n`);
  return (replies.find((r) => new RegExp(r.match, 's').test(text)) || replies.at(-1)).reply;
};
http.createServer((req, res) => {
  if (req.method === 'GET') { // /v1/models and Ollama /api/tags
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ object: 'list', data: [{ id: 'local-model', object: 'model' }], models: [{ name: 'local-model' }] }));
    return;
  }
  let body = '';
  req.on('data', (c) => (body += c));
  req.on('end', async () => {
    let j = {}; try { j = JSON.parse(body); } catch {}
    const reply = pick(j.messages || [{ content: j.input || '' }]);
    if (!j.stream) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ id: 'mock', object: 'chat.completion', model: j.model, choices: [{ index: 0, message: { role: 'assistant', content: reply }, finish_reason: 'stop' }], usage: { prompt_tokens: 1, completion_tokens: 1, total_tokens: 2 } }));
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' });
    for (const c of reply.match(/[\s\S]{1,4}/g) || []) {
      res.write(`data: ${JSON.stringify({ id: 'mock', object: 'chat.completion.chunk', model: j.model, choices: [{ index: 0, delta: { content: c }, finish_reason: null }] })}\n\n`);
      await new Promise((r) => setTimeout(r, delay));
    }
    res.write(`data: ${JSON.stringify({ id: 'mock', object: 'chat.completion.chunk', choices: [{ index: 0, delta: {}, finish_reason: 'stop' }] })}\n\n`);
    res.end('data: [DONE]\n\n');
  });
}).listen(port, '127.0.0.1', () => console.log('mock llm on', port, 'replies', repliesPath));
