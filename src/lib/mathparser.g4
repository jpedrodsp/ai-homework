grammar mathparser;
compileUnit
    :   expr
    ;
expr
   :   '(' expr ')'                         # parensExpr
   |   left=expr op='^' right=expr          # infixExpr
   |   left=expr op=('*'|'/') right=expr    # infixExpr
   |   left=expr op=('+'|'-') right=expr    # infixExpr
   |   value=NUM                            # numberExpr
   ;

OP_ADD: '+';
OP_SUB: '-';
OP_MUL: '*';
OP_DIV: '/';
OP_POW: '^';

NUM :   [0-9]+ ('.' [0-9][eE][+-]?[0-9]+)? ;
WS  :   [ \t\r\n] -> channel(HIDDEN);
