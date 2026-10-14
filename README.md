# SimpleStart

Build interactive web apps with pure Python — a reactive UI framework without HTML, CSS or JavaScript.

SimpleStart turns plain Python scripts into reactive web applications. Import `simplestart`, call `ss.*` APIs, and a modern Vuetify-powered UI renders in your browser — no frontend code required.

## Features

- **Pure Python** — no HTML, CSS, JavaScript or template files
- **Reactive UI** — state changes update the page automatically
- **60+ built-in components** — forms, tables, charts (ECharts), dialogs, tabs, layout and more
- **Cython-accelerated core** — compiled for performance
- **Zero configuration** — built-in web server: run your script, open the browser

## Installation

```bash
pip install simplestart
```

## Quick Start

Create `app.py`:

```python
import simplestart as ss

def on_click():
    ss.message("Hello from SimpleStart!")

ss.write("## My First App")
ss.text("This page is 100% Python.")
ss.button("Click me", type="primary", onclick=on_click)

ss.run()
```

Run it:

```bash
python app.py
```

Then open http://localhost:8000 — that's the whole workflow.

## Documentation

Live demos and full API documentation: **http://www.simplestart.cc**

## Requirements

- Python 3.10 – 3.13
- Works on Linux, macOS and Windows

## License

SimpleStart is proprietary software. You may build applications with it — including commercial ones — and distribute your applications freely (e.g. bundled with PyInstaller or Docker). Redistribution of the framework itself as a standalone package is not permitted. See [LICENSE.txt](LICENSE.txt) for details.

Copyright (c) 2026 readever. All rights reserved.