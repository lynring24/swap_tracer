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

static inline std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(),
            std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;
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
	      int pointer = vardef.find('*');
	      int bracket = vardef.find('[');
	      int name_start = vardef.find_last_of(' ');
	      string size = matched[3].str();
	      string varname;
	     
	      varname = split(vardef.substr(pointer+1), ' ').back();
	      varname = rtrim(varname);

	      if (bracket != -1) { 
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", " << size << ");"<< endl;
	     }
	      else {
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << size << ");" << endl;
	     }
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
	      int pointer = vardef.find('*');
	      int name_start = vardef.find_last_of(' ');
	      int bracket = vardef.find('[');
	      string count = matched[2].str();
	      string size = matched[3].str();
              string varname;
	      
	      varname = split(vardef.substr(pointer+1), ' ').back();
              varname = rtrim(varname);

	      if (bracket != -1) { 
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", (" << count << ")*(" << size << "));"<< endl;
	      }
	      else {
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", (" << count << ")*(" << size << "));" << endl;
	     }
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
	      int pointer = vardef.find('*');
	      int bracket = vardef.find('[');
	      int name_start = vardef.find_last_of(' ');
	      string varsize = matched[2].str();
              string varname;
	      
	      varname = split(vardef.substr(pointer+1), ' ').back();
              varname = rtrim(varname);

	      if ( bracket != -1) {
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, &"<< varname << ", " << varsize << ");";
	      }
	      else {
		cout << "\tprintf(\" %s, %s, " << varname << ", %p, %ld \\n\"," << "__FILE__, __FUNCTION__, "<< varname << ", " << varsize << ");" ;
	     }
	}
 }


%%

int main (int argc, char ** argv) {
    cout << "#include <sys/time.h>" << endl;
    int result = yylex();
    return 0;
}

