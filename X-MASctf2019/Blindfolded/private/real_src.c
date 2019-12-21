#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_CHUNKS 10
int count = 0;
struct chunk {
    unsigned int size;
    unsigned char *ptr;
};
struct chunk chunks[MAX_CHUNKS];

void menu() {
    printf("Space %d/%d\n", count, MAX_CHUNKS);
    printf("1. New\n");
    printf("2. Delete\n");
    printf("3. Exit\n");
    printf("1337. Realloc\n");
}

void create() {
    if (count >= MAX_CHUNKS) {
        printf("Full\n");
        return ;
    }

    unsigned int idx, sz;
    printf("idx: ");
    scanf("%u", &idx);
    printf("sz: ");
    scanf("%u", &sz);

    if (idx >= MAX_CHUNKS) {
        printf("Out of bounds\n");
        return ;
    }

    if (sz >= 0x200) {
        printf("Too big\n");
        return ;
    }

    if (chunks[idx].size != 0) {
        printf("Slot is not empty\n");
        return ;
    }

    count++;
    chunks[idx].size = sz;
    chunks[idx].ptr  = malloc(sz);
    printf("data: ");
    read(0, chunks[idx].ptr, chunks[idx].size);
    printf("Created\n");
}

void delete() {
    printf("idx: ");
    unsigned int idx;
    scanf("%u", &idx);


    if (idx >= MAX_CHUNKS) {
        printf("Out of bounds\n");
        return ;
    }

    count--;
    chunks[idx].size = 0;
    free(chunks[idx].ptr);
    printf("Deleted\n");
}

int used = 0;
void forbidden() {
    if (used) {
        printf("No, no, no. I told you that's forbidden and I already made an exception once.\n");
        return ;
    }
    
    used = 1;
    printf("Ummmm... But that's forbidden... I could let you... I have a bad feeling about this...\n");
    printf("I'll give you only one chance... But first, let me clean the stack a little bit... Done!\n");
    //printf("With this, the exploit should be straightforward.\n");
    //printf("Running: memset(alloca(0x100), 0, 0x100)\n\n");
    char *buf = alloca(0x100);
    memset(buf, 0, 0x100);

    unsigned int idx, sz;
    printf("idx: ");
    scanf("%u", &idx);
    printf("sz: ");
    scanf("%u", &sz);

    if (idx >= MAX_CHUNKS) {
        printf("Out of bounds\n");
        return ;
    }

    if (sz >= 0x200) {
        printf("Too big\n");
        return ;
    }

    chunks[idx].size = sz;
    chunks[idx].ptr  = realloc(chunks[idx].ptr, sz);
    printf("data: ");
    read(0, chunks[idx].ptr, chunks[idx].size);
    printf("Reallocated\n");
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("Are you ready for another heap challenge?\n");
    while (1) {
        menu();
        printf("> ");
        int choice;
        scanf("%d", &choice);

        if (choice == 1) {
            create();
        } else if (choice == 2) {
            delete();
        } else if (choice == 3) {
            break;
        } else if (choice == 1337) {
            forbidden();
        }
    }

    return 0;
}

