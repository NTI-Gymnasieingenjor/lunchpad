#include "application.h"
#include "student_data.h"
#include "lunch_data.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <string.h>



static struct timeval tv;
static char time_buffer[64];
static struct tm *time_info;
static time_t timet;
static int week = 0;
static int curr_time = 0;

static int parse_time(const char *str)
{
    int hours;
    int minutes;
    sscanf(str, "%d:%d", &hours, &minutes);
    return hours*60 + minutes;
}

static void update_time()
{
    gettimeofday(&tv, NULL);
    timet = tv.tv_sec;
    time_info = localtime(&timet);

    strftime(time_buffer, sizeof(time_buffer), "%H:%M\n", time_info);
    curr_time = parse_time(time_buffer);

    strftime(time_buffer, sizeof(time_buffer), "%w", time_info);
    week = atoi(time_buffer) - 1;
}

static StudentData *find_student(int mfr, StudentData *data)
{
    while(data) {
        if(data->mfr == mfr)
            return data;
        data = data->next;
    }
    return NULL;
}

static LunchTimeTable *find_time_table(const char *id, LunchTimeTable *table)
{
    while(table) {
        if(strncmp(id, table->class_id, strlen(id)) == 0)
            return table;
        table = table->next;
    }
    return NULL;
}

void application_start(const char *path_student, const char *path_lunch)
{
    StudentData *students = student_read_data(path_student);
    LunchTimeTable *lunch_table = lunch_table_read(path_lunch);
    StudentData *curr_student;
    LunchTimeTable *curr_time_table;

    char buff[1024];
    int res;
    int mfr;
    int found = 0;
    for(;;) {
        if(week < 0 || week > 4) {
            printf("It's weekend");
            break;
        }
        update_time();
        curr_student = students;
        curr_time_table = lunch_table;

        res = fscanf(stdin, "%s", buff);
        if(res != 1) {
            printf("-1\n");
            continue;
        }
        mfr = atoi(buff);

        StudentData *student = find_student(mfr, students);
        if(!student) {
            printf("0\n");
            continue;
        }

        LunchTimeTable *table = find_time_table(student->class_id, lunch_table);
        if(!table) {
            printf("-2\n");
            continue;
        }

        if(curr_time >= table->lunch_times[week] &&
            curr_time <= table->lunch_times[week] + GRACE_TIME) {
            printf("1\n");
        } else {
            printf("2\n");
        }


    }
}
