#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

char banner[] = "Are you ready for another heap challenge?";
char menu[] = "Space %d/10\n1. New\n2. Delete\n3. Exit\n1337. Realloc\n> ";
char input_buf[100];
int space = 0;

char* arr[10];

int do_malloc(){
    int idx, sz;
    printf("idx: ");
    scanf("%d", &idx);
    getchar();
    printf("sz: ");
    scanf("%d", &sz);
    getchar();

    
    if ((space < 10) & (idx < 10) & (idx >= 0)){
        arr[idx] = (char *) malloc(sz);
        printf("data: ");
        read(0, arr[idx], sz);
        space++;
        puts("Created");

    } 
    else
    {

        puts("Fuck you!");
    }
    
}

int do_free(){
    int idx, sz;
    printf("idx: ");
    scanf("%d", &idx);
    getchar();

    if ((space < 10) & (idx < 10) & (idx >= 0)){
        free(arr[idx]);
        space--;
        puts("Deleted");

    } 
    else
    {
        puts("Fuck you!");
    }
    
}

int do_realloc(){
    int idx, sz;
    printf("idx: ");
    scanf("%d", &idx);
    getchar();
    printf("sz: ");
    scanf("%d", &sz);
    getchar();
        
    if ((space < 10) & (idx < 10) & (idx >= 0)){
        arr[idx] = realloc(arr[idx], sz);
        printf("data: ");
        read(0, arr[idx], sz);
        space++;
        puts("Created");

    } 
    else
    {

        puts("Fuck you!");
    }
}

int main(){
    int choice;
    setvbuf(stdin, NULL, _IONBF, 1);
    setvbuf(stdout, NULL, _IONBF, 1);
    puts(banner);
    
    while (1) {
        printf(menu, space);
        scanf("%d", &choice);
        getchar();

        switch (choice)
        {
        case 1:
            do_malloc();
            break;
        
        case 2:
            do_free();
            break;

        case 3:
            exit(0);
            break;

        case 1337:
            do_realloc();
            break;

        default:
            break;
        }
    }
}