from typing import List

from IPython.display import display, Code, HTML, Javascript, Math
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, magics_class, line_cell_magic

from mathics.session import MathicsSession

from .format import Formatter


class JupyterFormatter(Formatter):
    def text(self, result):
        return Code(result, language="mathematica")

    def math(self, result):
        return Math(result)

    def graphics3d(self, result):
        # return JSON(json.loads(result))
        return Javascript(f"drawGraphics3d(element, {result})")

    def svg(self, result):
        return self.html(result)

    def html(self, result):
        result = result.replace("<math", "<div")
        result = result.replace("<mglyph", '<img style="display: inline-block" ')
        result = result.replace("<mrow>", "")
        result = result.replace("<mo>", "")
        return HTML(result)


@magics_class
class MathicsMagic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.session = MathicsSession()
        self.formatter = JupyterFormatter()

    @line_cell_magic
    def mathics3(self, line, cell=""):
        expr = self.session.evaluate(line + "\n" + cell)
        return self.formatter.format_output(self.session.evaluation, expr)


def transform_cell(lines: List[str]) -> List[str]:
    return ["%%mathics3\n"] + lines


def load_ipython_extension(ipython: InteractiveShell):
    ipython.register_magics(MathicsMagic)
    ipython.input_transformers_cleanup.append(transform_cell)
    display(Javascript("""
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://cdn.jsdelivr.net/npm/@mathicsorg/mathics-threejs-backend';
        document.head.appendChild(script);
        console.log('Loading mathics-threejs-backend');
    """))
