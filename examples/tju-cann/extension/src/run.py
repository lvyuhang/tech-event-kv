import sys, json, subprocess
import formats
only = sys.argv[1] if len(sys.argv) > 1 else ''
meta = {}
for k, (fn, mm) in formats.FORMATS.items():
    if only and not k.startswith(only): continue
    d = fn(); open(f'{k}.html', 'w').write(d.html()); meta[k] = {'w': d.W, 'h': d.H, 'mm': mm}
json.dump(meta, open('meta.json', 'w'), ensure_ascii=False)
