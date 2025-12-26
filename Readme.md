# Explainable AI Manim Presentation

## Installation
1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Presentation
1. Render the scenes:
```bash
bash run.sh --render
```

2. Set configs for `manim-slides`:
```bash
bash run.sh --slides-config
```

3. Present using default window or html:
```bash
bash run.sh --show
# or
bash run.sh --show-html
```

4. [OPTIONAL] if you need mouse button support for the presentation, run this command:
```bash
python input.py
```