import json

import marimo as mo

from mathics.session import MathicsSession

from .format import Formatter


class MarimoFormatter(Formatter):
    def text(self, result):
        return result

    def math(self, result):
        return mo.md(r"\[" + result + r"\]")

    def graphics3d(self, result):
        return json.loads(result)

    def svg(self, result):
        return self.html(result)

    def html(self, result):
        result = result.replace("<math", "<div")
        result = result.replace("<mglyph", '<img style="display: inline-block" ')
        result = result.replace("<mrow>", "")
        result = result.replace("<mo>", "")
        return mo.Html(result)


session = MathicsSession()
formatter = MarimoFormatter()


def mathics3(query):
    expr = session.evaluate(query)
    return formatter.format_output(session.evaluation, expr)
