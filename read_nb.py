import json

with open('notebooks/01_modelagem.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        print(f"--- Cell {i} ---")
        print(source)
