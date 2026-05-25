import re

from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import Markdown

from .format import Formatter


class MarkdownFormatter(Formatter):
    """Formatter optimized for markdown output in Jupyter."""

    def text(self, result):
        return f"```mathematica\n{result}\n```"

    def math(self, result):
        return f"$$\n{result}\n$$"

    def html(self, result):
        return result

    def svg(self, result):
        return result

    def graphics3d(self, result):
        return f"<script>drawGraphics3d(element, {result})</script>"


@magics_class
class MarkdownMathics3Magic(Magics):
    """Magic command for evaluating Mathics3 expressions within markdown cells."""

    def __init__(self, shell):
        self.formatter = MarkdownFormatter()
        self.shell = shell

    def evaluate_expression(self, expr_str: str) -> str:
        """Evaluate a single Mathics3 expression and return formatted result."""
        try:
            expr = self.session.evaluate(expr_str)
            result = self.formatter.format_output(self.session.evaluation, expr)
            return str(result) if result else "No output"
        except Exception as e:
            return f"Error: {str(e)}"

    def process_inline_expressions(self, text: str) -> str:
        """Replace inline expressions like `mathics|expr|` with results."""
        # Pattern matches `mathics|...|` or `m|...|`
        pattern = r"`(?:mathics|m)\|([^|]+)\|`"

        def replace_inline(match):
            expr_str = match.group(1).strip()
            result = self.evaluate_expression(expr_str)
            return f"${result}$"  # Wrap in single $ for inline math

        return re.sub(pattern, replace_inline, text)

    def process_block_expressions(self, text: str) -> str:
        """Replace block expressions like $$mathics ... $$ with results."""
        # Pattern matches $$mathics ... $$ blocks
        pattern = r"\$\$mathics\s*(.*?)\s*\$\$"

        def replace_block(match):
            expr_str = match.group(1).strip()
            result = self.evaluate_expression(expr_str)
            return f"$$\n{result}\n$$"  # Wrap in double $$ for block math

        return re.sub(pattern, replace_block, text, flags=re.DOTALL)

    @line_cell_magic
    def markdown_mathics3(self, line, cell=""):
        """
        Magic command to process markdown with embedded Mathics3 expressions.

        Usage:
            %%markdown_mathics3
            This is a calculation: `mathics|2 + 2|` which equals 4.

            Block calculation:
            $$mathics
            Integrate[x^2, x]
            $$
        """
        markdown_text = line + "\n" + cell

        # Process both inline and block expressions
        markdown_text = self.process_inline_expressions(markdown_text)
        markdown_text = self.process_block_expressions(markdown_text)

        # Display as rendered markdown
        return Markdown(markdown_text)
