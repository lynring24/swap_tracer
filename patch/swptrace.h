#ifdef _LINUX_SWPTRACE_H
int SWPTRACE; 
pid_t SWPTARGET;
int is_child(pid_t child);
#else
extern int SWPTRACE;
extern pid_t SWPTARGET;
extern int is_child(pid_t child);
#endif

