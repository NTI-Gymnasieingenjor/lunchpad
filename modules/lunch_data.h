#ifndef LUNCH_DATA
#define LUNCH_DATA

#define IDENTIFIER_SIZE 10

struct lunch_table {
    char *class_id;
    int lunch_times[5];
    struct lunch_table *next;
};

typedef struct lunch_table LunchTimeTable;

void lunch_table_destroy(struct lunch_table *table);
struct lunch_table *lunch_table_read(const char *path);

#endif

