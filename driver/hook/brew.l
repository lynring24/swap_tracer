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
      string argn = yytext;
      //[a-zA-Z0-9_] : variable name rule
      const regex re(".*([a-zA-Z0-9_]+).*=.*malloc.*");
      cmatch var_matches;

      regex_search(yytext, var_matches, re);
      //cout << var_matches[1] <<endl;
      request.insert(request.rfind('(')+1, "__FILE__, __LINE__, __FUNCTION__, \""+var_matches[1].str()+"\" , ");
      cout << request << endl; 
        
 }

%%

int main (int argc, char ** argv) {
    // lines, libraries that should be included should be injected here
	cout << "# include \"hmalloc.c\" "<< endl;
	int result = yylex();
    return 0;
}

