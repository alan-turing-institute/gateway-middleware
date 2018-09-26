from pathlib import Path

for i in Path('.').rglob('*'):
    print(i.suffix, i.stem)
