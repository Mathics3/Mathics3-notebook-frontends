from typing import List

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, Code, Javascript, Math, display
from mathics.core.load_builtin import import_and_load_builtins
from mathics.session import MathicsSession

from mathics3_kernel.frontend.markdown_mathics3 import MarkdownMathics3Magic

from .format import Formatter

import_and_load_builtins()


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
class Mathics3Magic(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.session = MathicsSession()
        import_and_load_builtins()
        self.formatter = JupyterFormatter()
        self.markdown = MarkdownMathics3Magic(shell)

    @line_cell_magic
    def mathics3(self, line, cell=""):
        if cell.startswith("%markdown_mathics3"):
            cell = cell[len("%markdown_mathics3") :]
            return self.markdown.markdown_mathics3(line, cell)
        expr = self.session.evaluate(line + "\n" + cell)
        return self.formatter.format_output(self.session.evaluation, expr)


def transform_cell(lines: List[str]) -> List[str]:
    return ["%%mathics3\n"] + lines


def load_ipython_extension(ipython: InteractiveShell):
    ipython.register_magics(Mathics3Magic)
    ipython.register_magics(MarkdownMathics3Magic)
    ipython.input_transformers_cleanup.append(transform_cell)
    display(
        Javascript(
            """
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://cdn.jsdelivr.net/npm/@mathicsorg/mathics-threejs-backend';
        document.head.appendChild(script);
        console.log('Loading mathics-threejs-backend');
    """
        )
    )
