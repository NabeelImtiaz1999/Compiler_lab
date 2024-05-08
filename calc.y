%{
void yyerror (char *s);
int yylex();
#include <stdio.h>     /* C declarations used in actions */
#include <stdlib.h>
#include <ctype.h>
%}

%union {int num; char id;}         /* Yacc definitions */
%start line
%token print
%token exit_command
%token <num> number
%token <id> startingParanthesis
%token <id> endingParanthesis
%token <id> AddOp
%token <id> MinOp
%token <id> MulOp
%token <id> DivOp
%token <id> Comment
%type <num> line exp
%type <num> term
%type <num> factor
%type <num> primary

%%
line    : exit_command ';'		{exit(EXIT_SUCCESS);}
		| exp ';'			{printf("Result: %d\n", $1);}
		| line exp ';'	{printf("Printing %d\n", $2);}
		| line exit_command ';'	{exit(EXIT_SUCCESS);}
		| exp exit_command ';'	{printf("Result: %d\n", $1); exit(EXIT_SUCCESS);}
        ;

exp    	: term                    {$$ = $1;}
       	| exp AddOp term          {$$ = $1 + $3;}
       	| exp MinOp term          {$$ = $1 - $3;}
       	;

term   	: factor                {$$ = $1;}
		| factor MulOp term		{$$ = $1 * $3;}
		| factor DivOp term		{$$ = $1 / $3;}
        ;

factor  : primary               {$$ = $1;}
        ;

primary : number                {$$ = $1;}
		| startingParanthesis exp endingParanthesis			{$$ = $2;}
        ;

%%

int main (void) {
	printf("Calc: ");
	return yyparse();
}

void yyerror (char *s) {fprintf (stderr, "%s\n", s);} 

