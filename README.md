# Mathics3 notebook frontends

This library provides helper functions for integrating Mathics3 into notebook environments.
Currently, it supports Jupyter(Lite), marimo, and Observable.

## Jupyter and JupyterLite

See the [Mathics3 live](https://github.com/Mathics3/Mathics3-live) project for a live demo.

```
%load_ext mathics3_kernel.frontend.jupyter
```

Usage is as simple as executing the above code in a notebook cell,
and then Mathics3 code can be directly run in all subsequent cells.
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
