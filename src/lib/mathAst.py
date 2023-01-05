import lib.mathparserParser as MathParser
import lib.mathparserLexer as MathLexer
import lib.custommathparserVisitor as MathVisitor
from pade.misc.utility import display_message

class NumberNode():    
    def __init__(self, value=None):        
        self.value = value
class InfixExpressionNode():    
    def __init__(self, left=None, right=None, value=None):            
        self.value = value
        self.left = left
        self.right = right

def visitNumberExpr(self, ctx:MathParser.mathparserParser.NumberExprContext):
    value = int(str(ctx.NUM()))
    display_message('ec', f'Got number: {value})')
    nn = NumberNode(value=value)
    return nn
def visitInfixExpr(self, ctx:MathParser.mathparserParser.InfixExprContext):
    node = InfixExpressionNode()        
    if ctx.OP_ADD():            
        node.value = '+'        
    elif ctx.OP_SUB():            
        node.value = '-'
    elif ctx.OP_MUL():            
        node.value = '*'        
    elif ctx.OP_DIV():            
        node.value = '/'        
    elif ctx.OP_POW():
        node.value = '^'
    display_message('ec', f'Got infix expression: {node.value})')
    node.left = self.visit(ctx.left)        
    node.right = self.visit(ctx.right)        
    return node