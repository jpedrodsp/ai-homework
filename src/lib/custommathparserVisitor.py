from antlr4 import *
if __name__ is not None and "." in __name__:
    from .mathparserParser import mathparserParser
else:
    from mathparserParser import mathparserParser

import lib.mathparserVisitor as MathVisitor
from pade.misc.utility import display_message
import lib.mathAst as MathAst

class customMathParserVisitor(MathVisitor.mathparserVisitor):
    def __init__(self) -> None:
        super().__init__()

    def visitNumberExpr(self, ctx: mathparserParser.NumberExprContext):
        """
        Retrieve value from number expression
        """
        value = float(str(ctx.NUM()))
        display_message('visitor', f'Got number: {value})')
        return MathAst.NumberNode(value=value)
    
    def visitInfixExpr(self, ctx: mathparserParser.InfixExprContext):
        """
        Retrieve value from infix expression
        """
        if ctx.OP_ADD():
            value = '+'
        elif ctx.OP_DIV():
            value = '/'
        elif ctx.OP_MUL():
            value = '*'
        elif ctx.OP_SUB():
            value = '-'
        elif ctx.OP_POW():
            value = '^'
        display_message('visitor', f'Got infix expression: {value})')
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)

        return MathAst.InfixExpressionNode(left=left, right=right, value=value)