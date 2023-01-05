# Generated from /home/jpedro/workspace/personal/ai-homework/src/lib/mathparser.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .mathparserParser import mathparserParser
else:
    from mathparserParser import mathparserParser

# This class defines a complete listener for a parse tree produced by mathparserParser.
class mathparserListener(ParseTreeListener):

    # Enter a parse tree produced by mathparserParser#compileUnit.
    def enterCompileUnit(self, ctx:mathparserParser.CompileUnitContext):
        pass

    # Exit a parse tree produced by mathparserParser#compileUnit.
    def exitCompileUnit(self, ctx:mathparserParser.CompileUnitContext):
        pass


    # Enter a parse tree produced by mathparserParser#infixExpr.
    def enterInfixExpr(self, ctx:mathparserParser.InfixExprContext):
        pass

    # Exit a parse tree produced by mathparserParser#infixExpr.
    def exitInfixExpr(self, ctx:mathparserParser.InfixExprContext):
        pass


    # Enter a parse tree produced by mathparserParser#numberExpr.
    def enterNumberExpr(self, ctx:mathparserParser.NumberExprContext):
        pass

    # Exit a parse tree produced by mathparserParser#numberExpr.
    def exitNumberExpr(self, ctx:mathparserParser.NumberExprContext):
        pass


    # Enter a parse tree produced by mathparserParser#parensExpr.
    def enterParensExpr(self, ctx:mathparserParser.ParensExprContext):
        pass

    # Exit a parse tree produced by mathparserParser#parensExpr.
    def exitParensExpr(self, ctx:mathparserParser.ParensExprContext):
        pass



del mathparserParser