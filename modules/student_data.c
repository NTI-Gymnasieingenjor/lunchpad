#include "student_data.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

static struct student *create_student()
{
    struct student *new = malloc(sizeof(struct student));

    new->mfr = -1;
    new->class_id = malloc(IDENTIFIER_SIZE);
    memset(new->class_id, 0, IDENTIFIER_SIZE);
    new->next = NULL;

    return new;
}

void destroy_student(struct student *s)
{
    if(s->next)
        destroy_student(s);
    if(s->class_id)
        free(s->class_id);
    free(s);
}

struct student *student_read_data(const char *path)
{
    FILE *f = fopen(path, "r");
    char buffer[4096];
    int mfr;
    struct student *start = create_student();
    struct student *curr = start;
    while(!feof(f)) {
        fscanf(f, "%4095[^,], %d\n", buffer, &mfr);

        strncpy(curr->class_id, buffer, IDENTIFIER_SIZE);
        curr->mfr = mfr;

        if(!feof(f)) {
            curr->next = create_student();
            curr = curr->next;
        }
    }
    fclose(f);
    return start;
}
