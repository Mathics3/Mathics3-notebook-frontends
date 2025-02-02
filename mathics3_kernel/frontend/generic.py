from mathics.session import MathicsSession

from .format import Formatter


class GenericFormatter(Formatter):
    def text(self, result):
        return "code", result

    def math(self, result):
        return "math", result

    def graphics3d(self, result):
        return "json", result

    def svg(self, result):
        return self.html(result)

    def html(self, result):
        result = result.replace("<math", "<div")
        result = result.replace("<mglyph", '<img style="display: inline-block" ')
        result = result.replace("<mrow>", "")
        result = result.replace("<mo>", "")
        return "html", result


session = MathicsSession()
formatter = GenericFormatter()


def mathics3(query):
    expr = session.evaluate(query)
    return formatter.format_output(session.evaluation, expr)
