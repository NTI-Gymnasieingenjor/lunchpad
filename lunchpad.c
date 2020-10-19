#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>

#define ID_SIZE 9
#define GRACE_TIME 20

struct identifier {
    int mfr;
    char *id;
    struct identifier *next;
};

struct lunch_table {
    char *id;
    int start_time[5];
    struct lunch_table *next;
};

struct identifier *create_identifier()
{
    struct identifier *new = malloc(sizeof(struct identifier));
    new->mfr = -1;
    new->id = malloc(ID_SIZE+1);
    memset(new->id, 1, 10);
    new->next = NULL;

    return new;
}

struct lunch_table *create_table()
{
    struct lunch_table *new = malloc(sizeof(struct lunch_table));
    new->id = malloc(ID_SIZE+1);
    memset(new->id, 1, 10);
    new->next = NULL;
    return new;
}

void destroy_indentifier(struct identifier *id)
{
    if(id && id->id) free(id->id);
    if(id && id->next) destroy_indentifier(id->next);
    if(id) free(id);
}
void destroy_table(struct lunch_table *table) {
    if(table && table->id) free(table->id);
    if(table && table->next) destroy_table(table->next);
    if(table) free(table);
}

struct identifier *read_identifier(const char *path)
{
    FILE *f = fopen(path, "r");
    char buffer[4096];
    int mfr = -1;
    struct identifier *start = create_identifier();
    struct identifier *node = start;
    while(!feof(f)) {
        fscanf(f, "%4095[^,],%d\n", buffer, &mfr);

        strncpy(node->id, buffer, strlen(buffer)+1);
        node->mfr = mfr;
        if(!feof(f)) {
            node->next = create_identifier();
            node = node->next;
        }
    }
    fclose(f);
    return start;
}
int parse_time(const char *str) {
    int hours;
    int minutes;
    sscanf(str, "%d:%d", &hours, &minutes);
    return hours*60+minutes;

}
struct lunch_table *read_table(const char *path)
{
    FILE *f = fopen(path, "r");
    char buffer[4096];
    char id[10];
    struct lunch_table *start= create_table();
    struct lunch_table *node = start;
    while(!feof(f)) {
        fscanf(f, "%9[^,],%s\n", id, buffer);
        strncpy(node->id, id, strlen(id)+1);
        char *tok = strtok(buffer, ",");
        int i = 0;
        while(tok != NULL) {
            node->start_time[i] = parse_time(tok);
            i++;
            tok = strtok(NULL, ",");
        }
        if(!feof(f)) {
            node->next = create_table();
            node = node->next;
        }
    }
    fclose(f);
    return start;
}


int main(int argc, const char **argv)
{

    struct identifier *ids = read_identifier("id.csv");
    struct lunch_table *table = read_table("tider.csv");
    struct timeval tv;
    time_t t;
    struct tm *info;
    char time_buffer[64];
    char week_buffer[64];
    int week = 0;
    int curr_time = -1;
    for(;;) {
        gettimeofday(&tv, NULL);
        t = tv.tv_sec;
        info = localtime(&t);
        strftime(time_buffer, sizeof time_buffer, "%H:%M\n", info);
        strftime(week_buffer, sizeof week_buffer, "%w", info);
        week = atoi(week_buffer) - 1;
        if(week < 0 || week > 4) {
            printf("It's weekend\n");
            break;
        }
        curr_time = parse_time(time_buffer);
        struct identifier *curr = ids;
        struct lunch_table *curr_table = table;
        int buff = -1;
        fscanf(stdin, "%d", &buff);
        int found = 0;
        while(curr && curr->next) {
            if(buff == curr->mfr) {
                found = 1;
                while(curr_table) {
                    //printf("comparing: %5s %5s\n", curr->id, curr_table->id);
                    if(strncmp(curr_table->id, curr->id, strlen(curr->id)) == 0) {
                        if(curr_time >= curr_table->start_time[week] && curr_time <= curr_table->start_time[week]+GRACE_TIME) {
                            printf("du äta\n");
                        } else {
                            printf("du ej äta\n");
                        }
                        break;
                        printf("%d:%s:%d", curr->mfr, curr->id, curr_table->start_time[0]);
                    }
                    curr_table = curr_table->next;
                }
                curr_table = table;
                //printf("Klass: %s\n", curr->id);
            }
            curr = curr->next;
        }
        if(!found) {
            printf("MFR not found\n");
        }
        curr = NULL;
        found = 0;
    }
    destroy_indentifier(ids);
    destroy_table(table);
    return 0;
}
