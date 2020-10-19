#ifndef STUDENT_DATA
#define STUDENT_DATA

#define IDENTIFIER_SIZE 10

struct student {
    int mfr;
    char *class_id;
    struct student *next;
};

typedef struct student StudentData;

void destroy_student(struct student *s);
struct student *student_read_data(const char *path);





#endif
