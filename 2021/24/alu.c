#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define MAX(a,b) ((a) > (b) ? (a) : (b))
#define MIN(a,b) ((a) < (b) ? (a) : (b))

void monad(int d, long long int *regs);

typedef struct {
        long long int regs[4];
        long long int lo;
        long long int hi;
} state_t;

int
statecmp(const void *this, const void *that) {
        const state_t *a = this;
        const state_t *b = that;
        for (int i = 1; i < 4; i++) {
                // ignore regs[0], which is 'w', which is input
                if (a->regs[i] > b->regs[i])
                        return 1;
                if (a->regs[i] < b->regs[i])
                        return -1;
        }
        return 0;
}

int main(int argc, char *argv[])  {
        state_t *state = calloc(1, sizeof(state_t));
        size_t sz = 1;
        for (int d = 0; d < 14; d++) {
                qsort(state, sz, sizeof(state_t), statecmp);

                int i = 0;
                for (int j = 1; j < sz; j++) {
                        if (statecmp(&state[i], &state[j]) == 0) {
                                state[i].lo = MIN(state[i].lo, state[j].lo);
                                state[i].hi = MAX(state[i].hi, state[j].hi);
                        } else {
                                i++;
                                state[i] = state[j];
                        }
                }
                sz = i+1;

                state = realloc(state, sizeof(state_t) * sz * 9);
                for (int i = 0, j = sz; i < sz; i++) {
                        state[i].regs[0] = 1;
                        state[i].lo = state[i].lo * 10 + 1;
                        state[i].hi = state[i].hi * 10 + 1;
                        for (int d = 2; d < 10; d++) {
                                state[j] = state[i];
                                state[j].regs[0] = d;
                                state[j].lo += d - 1;
                                state[j].hi += d - 1;
                                j++;
                        }
                }
                sz *= 9;
                printf("%d digits %d states\n", d+1, sz);
                for (int s = 0; s < sz; s++) {
                        monad(d, state[s].regs);
                }
        }
        long long int min = 99999999999999;
        long long int max = 0;
        for (int i = 0; i < sz; i++) {
                if (state[i].regs[3] != 0)
                        continue;
                min = MIN(state[i].lo, min);
                max = MAX(state[i].hi, max);
        }
        printf("p1 %lld\n", max);
        printf("p2 %lld\n", min);
}
