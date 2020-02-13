%{
#include <stdio.h>
#include <iostream>
#include <string.h>

using namespace std;

%}
%option noyywrap
%%

.*malloc.*;  {
      string request = yytext ;
	  request = request.replace(request.find("malloc"), string("malloc").size(), "hmalloc"); 
	  cout << request << endl;
 }

%%

int main (int argc, char ** argv) {
    // lines, libraries that should be included should be injected here
	cout << "# include \"hmalloc.c\" "<< endl;
	int result = yylex();
    return 0;
}

