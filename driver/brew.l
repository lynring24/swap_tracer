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
      const regex re ("[\t ]*(.*)[\t ]*=.*malloc(.*)");
      cmatch matched;

      regex_search(yytext, matched, re); 
      string info = matched[2].str();
      info.insert(info.find_first_of('(')+1 ," __FILE__, __LINE__, __FUNCTION__, \"" + matched[1].str() + "\", " );

      request = request.replace(request.find(matched[2].str()), matched[2].str().length(), info);
      cout << request << endl; 

      //[a-zA-Z0-9_] : variable name rule
      //const regex re2("((int|char|double|float|[a-zA-Z0-9_]+))?.*(\*)?.*([a-zA-Z0-9_]+).*=.*malloc.*");

        
 }

%%

int main (int argc, char ** argv) {
    // lines, libraries that should be included should be injected here
	int result = yylex();
    return 0;
}

