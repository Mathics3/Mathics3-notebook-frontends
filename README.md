# Mathics3 Extension Module for notebook frontends

This library provides helper functions via a Jupyter Extension to integrate Mathics3 into notebook environments.

Currently, it supports Jupyter, JupyterLite, marimo, and Observable.

For Jupyter, see also the GitHub repository [Jupyter Kernel](http://github.com/Mathics3/Mathics3-notebook-jupyter).

### Initial setup
Set up your Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

or using `pyenv`:
```bash
pyenv local 3.14

```

### Running

Next, start Jupyter Notebook:

```bash
jupyter notebook # or make run-jupyter-notebook
```

Alternatively, start Jupyter Lab:

```bash
jupyter lab # or make run-jupyter-lab
```


You should see a URL to connect to:

```
    To access the server, open this file in a browser:
        file:/usr/local/share/jupyter/runtime/jpserver-3279554-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/tree?token=1833fd2ac0fecd651c3f2d44931bd44c06673dd4701af3ca
        http://127.0.0.1:8888/tree?token=1833fd2ac0fecd651c3f2d44931bd44c06673dd4701af3ca
```

The URLS and file access will be different than the above. Also, remove any browser connections to the URLS, e.g., `localhost:8888` or `127.0.0.1:8888`, or else you'll see errors.


Inside a standard Python3 Jupyter Kernel (ipykernel), run:

```
%load_ext mathics3_kernel.frontend.jupyter
```


After this, entering code in a Notebook cell will be interpreted as Mathics3 input.

Here is a [sample notebook](examples/jupyter-notebook.ipynb) that can be used with a local Jupyter installation.

On entering the notebook, you will have to rerun the first cell, which should look like:
```
%pip install -v Mathics3 Mathics3-notebook-frontends Mathics3-Module-networkx ipywidgets lxml pyocr scikit-image unidecode wordcloud
%load_ext mathics3_kernel.frontend.jupyter
```

The 
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://w3.org">
  <circle cx="50" cy="50" r="40" fill="royalblue" />
</svg>
Foo
<svg width="14" height="14" viewBox="0 0 24 24" 
    style="display: inline-block; vertical-align: middle; margin: 0 2px;">
  <g class="jp-icon3\" fill="#616161">
     <path d="M8 5v14l11-7z\">
  </g>
</svg>

button on the menu icon bar, second from the top, does this. Alternatively, the  
<svg xmlns="http://w3.org"
     width="14" height="14" viewBox="0 0 24 24" style="display: inline-block; vertical-align: middle; margin: 0 2px;">
  <g class="jp-icon3" fill="#616161\">
     <path d=\"M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/>
  </g>
</svg>
button in that menu will rerun all cells.

If you would like to run Mathics3 in a browser without doing any setup or installation, see [Mathics3 Live](https://mathics3.github.io/Mathics3-live/). The GitHub repository for this is at [https://github.com/Mathics3/Mathics3-live](https://github.com/Mathics3/Mathics3-live)

## marimo

```py
from mathics3_kernel.frontend.marimo import mathics3
```

Then run Mathics3 code like so:

```py
mathics3("ArcCos[0]")
```

See the examples directory for a sample notebook:

```sh
marimo edit --sandbox examples/marimo_notebook.py
```

It also works in marimo's Pyodide-powered online environment; see https://marimo.io/p/@davidar/mathics for an example.

## Observable

For other notebook environments, this library provides a generic interface:

```py
from mathics3_kernel.frontend.generic import mathics3
```

See https://observablehq.com/@davidar/mathics for an example of how this can be used with Observable notebooks.
This notebook loads the library with pyodide, then implements a simple interface in JavaScript:

```js
async function mathics3(strings) {
  const [type, result] = await py`${mathics3_kernel}(${strings[0]})`
  if (type === "code") {
    return md`\`\`\`\n${result}\n\`\`\``;
  } else if (type === "math") {
    return tex.block`${result}`;
  } else if (type === "json") {
    return JSON.parse(result);
  } else if (type === "html") {
    return html`${result}`;
  } else {
    return result;
  }
}
```
