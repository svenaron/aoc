#include <stdio.h>
#include <stdlib.h>

int main () {
        unsigned numbers[] = { 0,5,4,1,10,14,7 };
        unsigned *index = calloc(30000000, sizeof(unsigned));
        for (unsigned i = 0; i < 6; i++)
                index[numbers[i]] = i + 1;
        unsigned n = numbers[6];
        unsigned nn;

        for (unsigned i = 7; i < 2020; i++) {
                if (index[n])
                        nn = i - index[n];
                else
                        nn = 0;
                index[n] = i;
                n = nn;
        }
        printf("%u\n", n);

        for (unsigned i = 2020; i < 30000000; i++) {
                unsigned *l = &index[n];
                if (*l)
                        nn = i - *l;
                else
                        nn = 0;
                *l = i;
                n = nn;
        }
        printf("%u\n", n);
        return(0);
}
