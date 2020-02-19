%{
#include <stdio.h>
#include <iostream>
#include <string>
#include <regex>

using namespace std;
%}

%option noyywrap

%%

.*malloc.*;  {
      string request = yytext ;
      request = request.replace(request.find("malloc"), string("malloc").size(), "hmalloc"); 
      // cout << request << endl;
      //[a-zA-Z0-9_] : variable name rule
      //const regex re2("((int|char|double|float|[a-zA-Z0-9_]+))?.*(\*)?.*([a-zA-Z0-9_]+).*=.*malloc.*");

      const regex re ("[\t ]*(.*)[\t ]*=.*malloc.*");
      //const regex re ("(.*)=.*malloc.*");
      cmatch matched;

      regex_search(yytext, matched, re);
      request.insert(request.rfind('(')+1, "__FILE__, __LINE__, __FUNCTION__, \"" + matched[1].str() + "\" , ");
      cout << request << endl; 
        
 }

%%

int main (int argc, char ** argv) {
    // lines, libraries that should be included should be injected here
	cout << "# include \"hmalloc.c\" "<< endl;
	int result = yylex();
    return 0;
}

