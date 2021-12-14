#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>

int count = 0;
bool sit = true;
int fd;

void handl(int signal_number){
	count++;
	char buff[3000];
	if (count == 2){
		int i = 0;
		int total = 0;
		char total_s[100];
		int date;
		time_t now = time(0);
		char* dt = ctime(&now);
		strtok(dt, " ");
		strtok(NULL, " ");
		date = atoi(strtok(NULL, " "));
		sit = false;
		int p[2], d[2];
		pipe(p);
		if (fork() == 0){
			close(p[0]); //close FIFO-file (for child thread) for reading
			close(1); // close stdout
			dup(p[1]); // clone FIFO-file (for child thread) for writing to the 1st position
			system("ls -sl ../Homework_2/");
			exit(0);
		}
		else{
			wait(0);
			close(p[1]); // close FIFO-file (for parent thread) for writing
			read(p[0], buff, 3000);
			close(p[0]);
			char delim[] = " \n";
			char *p[2000] = {0};
			p[0] = strtok(buff, delim);
		
			while (p[i] != NULL) {
				i++;
				p[i] = strtok(NULL, delim);
			}
			
			int j = 2;
			while (j < i){
				if (atoi(p[j]) > 12 && (atoi(p[j+7])-date) < 5) total += atoi(p[j]);
				j += 10;
			}
			pipe(d);
			if (fork() == 0){
				close(d[0]);
				close(1);
				dup(d[1]);
				printf("%d", total);
				exit(0);
			}
			else{
				wait(0);
				close(d[1]);
				fd = d[0];
			}
		}
	}
}

int main() {
	printf("Lab 1. Var 23.\n");

	int i = 0;
	int date;
	int counter = 0;
	int count_block = 0;
	int count_date = 0;
	time_t now = time(0);
	char* dt = ctime(&now);
	printf("%s", dt);
	fflush(stdout);
	strtok(dt, " ");
	strtok(NULL, " ");
	date = atoi(strtok(NULL, " "));

	struct sigaction parent;
	parent.sa_handler = handl;
	parent.sa_flags = 0;
	sigprocmask(0, 0, &parent.sa_mask);
	sigaction(SIGINT, &parent, 0);

	int p[2];
	char buff[3000];
	pipe(p);

	if (fork() == 0){
		close(p[0]); //close FIFO-file (for child thread) for reading
		close(1); // close stdout
		dup(p[1]); // clone FIFO-file (for child thread) for writing to the 1st position
		sleep(2);
		execl("/bin/ls", "ls", "-sl", "../Homework_2/", NULL);
	}
	else {
		wait(0);
		close(p[1]); // close FIFO-file (for parent thread) for writing
		read(p[0], buff, 3000);
		close(p[0]);
		char delim[] = " \n";
		char *p[2000] = {0};
		p[0] = strtok(buff, delim);
		
		while (p[i] != NULL) {
			i++;
			p[i] = strtok(NULL, delim);
		}
	sleep(2);

	int j = 2;
	if (sit){
		printf("Selected files:\n");
		while (j < i){
			if (atoi(p[j]) > 12 && (atoi(p[j+7])-date) < 5) {
				printf("%s\n", p[j+9]);
				fflush(stdout);
			}
			j += 10;
		}
	}
	else{
		char total[100];
		read(fd, total, 100);
		printf("\nTotal size: %s\n", total);
		fflush(stdout);
		
	}

	}
	return 0;
}








