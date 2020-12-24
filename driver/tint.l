%{
#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
#include <regex>

using namespace std;

vector<string> split(string str, char delimiter) { 
  vector<string> internal; 
  stringstream ss(str); // Turn the string into a stream. 
  string tok; 
 
  while(getline(ss, tok, delimiter)) { 
    internal.push_back(tok); 
  } 
 
  return internal; 
} 
%}

%option noyywrap

%%

^[^/]{2}.*realloc.*;  {
      string request = yytext ;
      cout << yytext<<endl; 
      const regex re ("^[^/]{1}(.*)=.*realloc ?\\((.*),(.*)\\).*;");
      cmatch matched;
        
      regex_search(yytext, matched, re); 
      if (matched.length() > 0) {
	      string vardef = matched[1].str();
	      int found = vardef.find('*');
	      int name_start = vardef.find_last_of(' ');
	      string size = matched[3].str();
	      string varname;
	     
              cout << found << endl;
	      cout << vardef.length() <<endl; 
	      
	      if (found < vardef.length()) {
		varname = split(vardef.substr(found+1), ' ').back();
		//cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", " << size << ");"<< endl;
	      }
	      else {
		varname = split(vardef.substr(found+1), ' ').back();
		//cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << size << ");" << endl;
	     }
             cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << size << ");" << endl;
	}
 }

^[^/]{2}.*calloc.*;  {
      string request = yytext ;
      cout << yytext<<endl; 
      const regex re ("^[^/]{1}(.*)=.*calloc ?\\((.*),(.*)\\).*;");
      cmatch matched;
        
      regex_search(yytext, matched, re); 
      if (matched.length() > 0) {
	      string vardef = matched[1].str();
	      int found = vardef.find('*');
	      int name_start = vardef.find_last_of(' ');
	      string count = matched[2].str();
	      string size = matched[3].str();
              string varname;
	      
	      if (found < vardef.length()) {
	        varname = split(vardef.substr(found+1), ' ').back();
	//	cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", (" << count << ")*(" << size << "));"<< endl;
	      }
	      else {
		varname = split(vardef.substr(found+1), ' ').back();
	//	cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", (" << count << ")*(" << size << "));" << endl;
	     }
              cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", (" << count << ")*(" << size << "));" << endl;
	}
 }

^[^/]{2}.malloc.*;  {
      string request = yytext ;
      cout << yytext<<endl; 
      const regex re ("^[^/]{2}(.*)=.*malloc\((.*)).*;");
      cmatch matched;
        
      regex_search(yytext, matched, re); 
      if (matched.length() > 0) {
	      string vardef = matched[1].str();
	      int found = vardef.find('*');
	      int name_start = vardef.find_last_of(' ');
	      string varsize = matched[2].str();
              string varname;
	      
	      if (found < vardef.length()) {
		varname = split(vardef.substr(found+1), ' ').back();
		//cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", " << varsize << ");";
	      }
	      else {
		varname = split(vardef.substr(found+1), ' ').back();
		//cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << varsize << ");" ;
	     }
	     cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << varsize << ");" ;
	}
 }


%%

int main (int argc, char ** argv) {
    cout << "#include <sys/time.h>" << endl;
    int result = yylex();
    return 0;
}

