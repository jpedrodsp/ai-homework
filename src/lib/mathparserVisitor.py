# Generated from /home/jpedro/workspace/personal/ai-homework/src/lib/mathparser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .mathparserParser import mathparserParser
else:
    from mathparserParser import mathparserParser

# This class defines a complete generic visitor for a parse tree produced by mathparserParser.

class mathparserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by mathparserParser#compileUnit.
    def visitCompileUnit(self, ctx:mathparserParser.CompileUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathparserParser#infixExpr.
    def visitInfixExpr(self, ctx:mathparserParser.InfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathparserParser#numberExpr.
    def visitNumberExpr(self, ctx:mathparserParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by mathparserParser#parensExpr.
    def visitParensExpr(self, ctx:mathparserParser.ParensExprContext):
        return self.visitChildren(ctx)



del mathparserParser