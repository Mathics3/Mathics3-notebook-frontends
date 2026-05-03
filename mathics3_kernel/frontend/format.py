from typing import Callable, Dict, Final

from mathics.core.atoms import SymbolString
from mathics.core.expression import BoxError, Expression
from mathics.core.symbols import Symbol
from mathics.core.systemsymbols import (
    SymbolAborted,
    SymbolCompiledFunction,
    SymbolFailed,
    SymbolFullForm,
    SymbolGraphics,
    SymbolGraphics3D,
    SymbolInputForm,
    SymbolMathMLForm,
    SymbolOutputForm,
    SymbolStandardForm,
    SymbolTeXForm,
)
from mathics.session import get_settings_value

# Maps a Form to a kind of html format.
# text is the usual text-kind of output.
# LaTeX is handled by MathJaX display mode $$ $$
# MathML could be tagged differently too.
FORM_TO_HTML_TAG_FORMAT: Final[Dict[str, str]] = {
    "System`FullForm": "text",
    "System`InputForm": "text",
    # "System`MathMLForm": "MathML",
    "System`OutputForm": "text",
    "System`TeXForm": "LaTeX",
    "System`String": "text",
}


class Formatter:
    def format_output(self, evaluation, expr, html_tag_format: str = "unformatted"):
        """
        evaluation.py format_output() from which this was derived is similar but
        it can't make use of a front-ends specific capabilities.
        """

        def eval_boxes(result, fn: Callable, evaluation, **options):
            options["evaluation"] = evaluation
            try:
                boxes = fn(**options)
            except BoxError:
                boxes = None
                if not hasattr(evaluation, "seen_box_error"):
                    evaluation.seen_box_error = True
                    evaluation.message(
                        "General",
                        "notboxes",
                        Expression(SymbolFullForm, result).evaluate(evaluation),
                    )
            return boxes

        if isinstance(html_tag_format, dict):
            return dict(
                (k, self.format_output(evaluation, expr, f))
                for k, f in html_tag_format.items()
            )

        if expr is SymbolAborted:
            return "$Aborted"
        elif expr is SymbolFailed:
            return "$Failed"

        # For some expressions, we want formatting to be different.
        # In particular for FullForm output, we don't want MathML, we want
        # plain-ol' text so we can cut and paste that.

        expr_type = expr.get_head_name()
        expr_head = expr.get_head()
        if expr_head in (SymbolMathMLForm, SymbolTeXForm):
            # For these forms, we strip off the outer "Form" part
            html_tag_format = FORM_TO_HTML_TAG_FORMAT[expr_type]
            elements = expr.get_elements()
            if len(elements) == 1:
                expr = elements[0]

        if expr_head in (SymbolFullForm, SymbolOutputForm):
            result = expr.elements[0].format(evaluation, expr_type)
            return self.text(result.boxes_to_text())
        # elif expr_head is SymbolGraphics:
        #     result = Expression(SymbolStandardForm, expr).format(
        #         evaluation, SymbolMathMLForm
        #     )

        # This part was derived from and the same as evaluation.py format_output.

        use_quotes = get_settings_value(
            evaluation.definitions, "Settings`$QuotedStrings"
        )

        if html_tag_format == "text":
            boxed = expr.format(evaluation, SymbolOutputForm)
            result = eval_boxes(boxed, boxed.boxes_to_text, evaluation)

            if use_quotes:
                result = '"' + result + '"'

            return self.text(result)
        elif html_tag_format == "xml":
            result = Expression(SymbolStandardForm, expr).format(
                evaluation, SymbolMathMLForm
            )
            return self.html(eval_boxes(result, result.boxes_to_text, evaluation))
        elif html_tag_format == "tex":
            result = Expression(SymbolStandardForm, expr).format(
                evaluation, SymbolTeXForm
            )
            return self.math(eval_boxes(result, result.boxes_to_text, evaluation))
        elif expr_head is Symbol("Pymathics`Graph") and hasattr(expr, "G"):
            from .graph import format_graph

            return self.svg(format_graph(expr.G))
        elif expr_head is SymbolCompiledFunction:
            result = expr.format(evaluation, SymbolOutputForm)
            return self.text(eval_boxes(result, result.boxes_to_text, evaluation))
        elif expr_head is SymbolString:
            result = expr.format(evaluation, SymbolInputForm)
            result = result.boxes_to_text()

            if not use_quotes:
                # Substring without the quotes
                result = result[1:-1]

            return self.text(result)
        elif expr_head is SymbolGraphics3D:
            form_expr = Expression(SymbolStandardForm, expr)
            result = form_expr.format(evaluation, SymbolStandardForm)
            return self.graphics3d(eval_boxes(result, result.boxes_to_json, evaluation))
        elif expr_head is SymbolGraphics:
            form_expr = Expression(SymbolStandardForm, expr)
            result = form_expr.format(evaluation, SymbolStandardForm)
            return self.svg(eval_boxes(result, result.boxes_to_svg, evaluation))
        else:
            result = Expression(SymbolStandardForm, expr).format(
                evaluation, SymbolTeXForm
            )
            return self.math(eval_boxes(result, result.boxes_to_text, evaluation))
