#include "lunch_data.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static struct lunch_table *lunch_table_create()
{
    struct lunch_table *new = malloc(sizeof(struct lunch_table));
    new->class_id = malloc(IDENTIFIER_SIZE);
    new->next = NULL;
    return new;
}

static int parse_time(const char *str)
{
    int hours;
    int minutes;
    sscanf(str, "%d:%d", &hours, &minutes);
    return hours*60 + minutes;
}

void lunch_table_destroy(struct lunch_table *table)
{
    if(table->next)
        lunch_table_destroy(table->next);
    if(table->class_id)
        free(table->class_id);
    free(table);
}

struct lunch_table *lunch_table_read(const char *path)
{
    FILE *f = fopen(path, "r");
    char buffer[4096];
    char id[IDENTIFIER_SIZE];

    struct lunch_table *start = lunch_table_create();
    struct lunch_table *curr = start;

    while(!feof(f)) {
        fscanf(f, "%9[^,], %s\n", id, buffer);
        strncpy(curr->class_id, id, IDENTIFIER_SIZE);
        char *tok = strtok(buffer, ",");
        for(int i = 0; tok; i++) {
            curr->lunch_times[i] = parse_time(tok);
            tok = strtok(NULL, ",");
        }
        if(!feof(f)) {
            curr->next = lunch_table_create();
            curr = curr->next;
        }
    }
    fclose(f);
    return start;
}
