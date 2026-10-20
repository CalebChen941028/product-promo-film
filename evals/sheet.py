"""sheet2.py film.mp4 out.jpg — 20 frames at exact, evenly spaced times (labels = the true time), 4×5 grid."""
import subprocess, sys, re, io
from PIL import Image, ImageDraw
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe(); src, out = sys.argv[1], sys.argv[2]
d = float(re.search(r'Duration: (\d+):(\d+):([\d.]+)', subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr).group(3)) + \
    60 * float(re.search(r'Duration: (\d+):(\d+)', subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr).group(2))
sheet = Image.new('RGB', (1920, 1350)); dr = ImageDraw.Draw(sheet)
for i in range(20):
    t = d * i / 20
    png = subprocess.run([FF, '-v', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', 'scale=480:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    im = Image.open(io.BytesIO(png)).convert('RGB'); x, y = (i % 4) * 480, (i // 4) * 270
    sheet.paste(im, (x, y)); dr.rectangle([x + 4, y + 4, x + 92, y + 26], fill='black'); dr.text((x + 8, y + 8), f'{int(t // 60):02d}:{t % 60:05.2f}', fill='yellow')
sheet.save(out, quality=85); print('duration', round(d, 2))
