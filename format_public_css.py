from pathlib import Path
import re

path = Path('mysite/static/new_index/style/public.css')
text = path.read_text(encoding='utf-8')
text = text.replace('\r\n', '\n').replace('\r', '\n')
text = '\n'.join(line.rstrip() for line in text.split('\n'))

out_lines = []
indent_level = 0
i = 0
n = len(text)
current = ''

def flush_current():
    global current
    if current.strip():
        out_lines.append('    ' * indent_level + current.strip())
    current = ''

while i < n:
    ch = text[i]
    if ch == '/' and i + 1 < n and text[i+1] == '*':
        flush_current()
        end = text.find('*/', i+2)
        if end == -1:
            comment = text[i:]
            i = n
        else:
            comment = text[i:end+2]
            i = end + 2
        comment_lines = comment.split('\n')
        for line in comment_lines:
            line = line.strip()
            if line:
                out_lines.append('    ' * indent_level + line)
            else:
                out_lines.append('')
        continue
    if ch == '{':
        selector = current.strip()
        out_lines.append('    ' * indent_level + selector + ' {')
        current = ''
        indent_level += 1
        i += 1
        while i < n and text[i] in ' \t\n\r':
            i += 1
        continue
    if ch == '}':
        flush_current()
        indent_level = max(indent_level - 1, 0)
        out_lines.append('    ' * indent_level + '}')
        current = ''
        i += 1
        while i < n and text[i] in ' \t\n\r':
            i += 1
        continue
    if ch == ';':
        current += ';'
        flush_current()
        current = ''
        i += 1
        while i < n and text[i] in ' \t\n\r':
            i += 1
        continue
    if ch == '\n':
        current += ' '
    else:
        current += ch
    i += 1

if current.strip():
    out_lines.append('    ' * indent_level + current.strip())

clean = []
prev_blank = False
for line in out_lines:
    if not line.strip():
        if not prev_blank:
            clean.append('')
        prev_blank = True
    else:
        clean.append(line)
        prev_blank = False

out_path = path.with_name('public.cleaned.css')
out_path.write_text('\n'.join(clean) + '\n', encoding='utf-8')
print('Wrote', out_path)
