
#include <stdint.h>
#include <stdio.h>

int main()
{
    int8_t i;

    for (i = INT8_MAX - 10; i < INT8_MAX; i++)
        printf("signed %hhd -> unsigned %hhu\n", i + 1, i + 1);

    for (i = INT8_MIN; i < (INT8_MIN + 10); i++)
        printf("signed %hhd -> unsigned %hhu\n", i, i);

    return 0;

}
