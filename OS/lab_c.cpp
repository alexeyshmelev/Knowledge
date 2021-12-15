#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>

int count = 0;
bool sit = true;
char* pointer;
int fd;

char* get_data(char* buff){
	int p;

	if (fork() == 0){
		p = creat("some_file", 0777);
		close(1);
		dup(p); 
		execl("/bin/find", "find", "../Homework_2/", "-maxdepth", "1", "-size", "+24b", "-atime", "-5", "-ls", NULL);
	}
	else {
		wait(0);
		p = open("some_file", O_RDONLY);
		read(p, buff, 3000);
		close(p);
		}
	return buff;
}

void handl(int signal_number){
	count++;
	char buff[3000];
	if (count == 2){
		int i = 0;
		int total = 0;
		sit = false;
		int d;
		char delim[] = " \n";
		char *p[2000] = {0};
		p[0] = strtok(pointer, delim);
		
		while (p[i] != NULL) {
			i++;
			p[i] = strtok(NULL, delim);
		}
			
		int j = 1;
		while (j < i){
			total += atoi(p[j]);
			j += 11;
		}
		if (fork() == 0){
			d = creat("some_file", 0777);
			close(1);
			dup(d);
			printf("%d", total);
			exit(0);
		}
		else{
			wait(0);
			d = open("some_file", 0);
			fd = d;
			}
	}
}

int main() {
	printf("Lab 1. Var 23.\n");

	int i = 0;
	time_t now = time(0);
	char* dt = ctime(&now);
	printf("%s", dt);
	fflush(stdout);

	struct sigaction parent;
	parent.sa_handler = handl;
	parent.sa_flags = 0;
	sigprocmask(0, 0, &parent.sa_mask); // первый аргумент - изменять ли сигнальную маску или нет (SIG_SETMASK - если да), второй аргумент - новая сигнальная маска, третий - старая
	sigaction(SIGINT, &parent, 0); // третий аргумент - сохранение старого действия
	
	char buff[3000];
	pointer = get_data(buff);
		
		sleep(2);
		sleep(2);

		if (sit){
			printf("Selected files:\n");
			fflush(stdout);
			char delim[] = " \n";
			char *p[2000] = {0};
			p[0] = strtok(pointer, delim);
		
			while (p[i] != NULL) {
				i++;
				p[i] = strtok(NULL, delim);
			}
			
			int j = 10;
			while (j < i){
				printf("%s\n", p[j]);
				j += 11;
			}
		}
		else{
			char total[100];
			read(fd, total, 100);
			printf("\nTotal size: %s\n", total);
			fflush(stdout);
		
		}
	return 0;
}
