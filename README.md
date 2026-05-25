# Mathics3 Extension Module for notebook frontends

This library provides helper functions via Jupyter Exntension for integrating Mathics3 into notebook environments.

Currently, it supports Jupyter, JupyterLite, marimo, and Observable.

For Jupyter, see also the Github repostitory for the [Jupyter Kernel](http://github.com/Mathics3/Mathics3-frontends-jupyter).

## Jupyter and JupyterLite

See [Mathics3 live](https://github.com/Mathics3/Mathics3-live) project a project that
uses this Python module in a live demo running under pyodidie.

Set up your Python environtment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

or using `pyenv`:
```bash
pyenv local 3.14
```

Next, start jupyter notebook:

```bash
jupyter notebook # or make run-jupyter-notebook
```

You should see a URL to connect to:

```
    To access the server, open this file in a browser:
        file:/usr/local/share/jupyter/runtime/jpserver-3279554-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/tree?token=1833fd2ac0fecd651c3f2d44931bd44c06673dd4701af3ca
        http://127.0.0.1:8888/tree?token=1833fd2ac0fecd651c3f2d44931bd44c06673dd4701af3ca
```

The URLS and file access will be different than the above. Also remove any browser connnections to the URLS, e.g.`localhost:8888` or `127.0.0.1:8888` or else you'll see errors.


Inside a standard *Python* Jupyter Kernel, run:

```
%load_ext mathics3_kernel.frontend.jupyter
```

After this entering code in a Notebook cell will be interpreted as Mathics3 input. ,
Here is a [sample notebook](examples/jupyter-notebook.ipynb)
that can be used with a local Jupyter installation.

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

It also works in marimo's pyodide-powered online environment, see https://marimo.io/p/@davidar/mathics for an example.

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
