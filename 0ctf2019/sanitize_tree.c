#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char   undefined;

typedef unsigned char    byte;
typedef unsigned char    dwfenc;
typedef unsigned int    dword;
typedef unsigned long    qword;
typedef unsigned int    uint;
typedef unsigned long    ulong;
typedef unsigned char    undefined1;
typedef unsigned short    undefined2;
typedef unsigned int    undefined4;
typedef unsigned long    undefined8;
typedef unsigned short    ushort;
typedef unsigned short    word;
typedef struct eh_frame_hdr eh_frame_hdr, *Peh_frame_hdr;

struct eh_frame_hdr {
    byte eh_frame_hdr_version; // Exception Handler Frame Header Version
    dwfenc eh_frame_pointer_encoding; // Exception Handler Frame Pointer Encoding
    dwfenc eh_frame_desc_entry_count_encoding; // Encoding of # of Exception Handler FDEs
    dwfenc eh_frame_table_encoding; // Exception Handler Table Encoding
};

typedef struct fde_table_entry fde_table_entry, *Pfde_table_entry;

struct fde_table_entry {
    dword initial_loc; // Initial Location
    dword data_loc; // Data location
};

typedef long int64_t;

typedef struct tree_node tree_node, *Ptree_node;

void _exit(int no) {
  exit(no);
} 

struct tree_node {
    char input_byte;
    undefined field_0x1;
    undefined field_0x2;
    undefined field_0x3;
    uint height_maybe;
    struct tree_node * parent;
    struct tree_node * tree_right;
    struct tree_node * next_or_left;
};


void increment(int *incme)
{
  *incme = *incme + 1;
}

int enter_new_tree;
int leave_new_tree;

tree_node ** new_tree_ptr(void)

{
  tree_node *char8ptr;
  
  increment(&enter_new_tree);
  char8ptr = (tree_node *)malloc(8);
  if (char8ptr == (tree_node *)0x0) {
                    // WARNING: Subroutine does not return
    _exit(-3);
  }
  increment(&leave_new_tree);
  *(undefined8 *)char8ptr = 0;
  return (tree_node **)char8ptr;
}

int enter_free_linked_list_rek;
int free_linked_list_rek_null;
int free_tree_rek_loop;
int leave_free_linked_list_rek;

void free_tree_rek(tree_node *node)

{
  tree_node *current;
  tree_node *paVar1;
  
  increment(&enter_free_linked_list_rek);
  current = node;
  if (node == (tree_node *)0x0) {
    increment(&free_linked_list_rek_null);
  }
  else {
    while (current != (tree_node *)0x0) {
      increment(&free_tree_rek_loop);
      free_tree_rek(current->tree_right);
      current->input_byte = 0;
      current->height_maybe = 0;
      current->parent = (tree_node *)0x0;
      current->tree_right = (tree_node *)0x0;
      paVar1 = current->next_or_left;
      current->next_or_left = (tree_node *)0x0;
      free(current);
      current = paVar1;
    }
    increment(&leave_free_linked_list_rek);
  }
  return;
}

int free_tree_func_enter;
int free_tree_func_loop;
int free_tree_func_leave;

void free_tree(tree_node *head)

{
  tree_node *current;
  tree_node *next_left;
  
  increment(&free_tree_func_enter);
  current = *(tree_node **)head;
  while (current != (tree_node *)0x0) {
    increment(&free_tree_func_loop);
    free_tree_rek(current->tree_right);
    next_left = current->next_or_left;
    current->tree_right = (tree_node *)0x0;
    current->parent = (tree_node *)0x0;
    current->next_or_left = (tree_node *)0x0;
    current->height_maybe = 0;
    current->input_byte = 0;
    free(current);
    current = next_left;
  }
  increment(&free_tree_func_leave);
  *(undefined8 *)head = 0;
  free(head);
  return;
}


// returns 0 if any input is 0
int a_t_r_enter;
int a_t_r_recursion_null;
int a_t_r_current_null;
int a_t_r_current_nonnull;
int a_t_r_created_new;
int a_t_r_created_not_new;
int a_t_r_created_branch1;
int INT_0060310c;
int INT_00603110;
int INT_00603114;
int INT_00603118;
int INT_0060311c;
int INT_00603120;
int INT_00603124;
int INT_00603128;
int INT_0060312c;
int INT_00603130;
int a_t_r_exit;

tree_node ** append_tree_rek(tree_node **old_head,tree_node **new_part)

{
  tree_node **new_head_maybe;
  tree_node *created_el;
  tree_node *new;
  tree_node *current;
  tree_node *current_next;
  
  increment(&a_t_r_enter);
  if (old_head == (tree_node **)0x0) {
    increment(&a_t_r_recursion_null);
  }
  else {
    if (new_part != (tree_node **)0x0) {
      current = *old_head;
      new = *new_part;
      new_head_maybe = new_tree_ptr();
      created_el = *new_head_maybe;
      while( true ) {
        if (current != (tree_node *)0x0) {
          increment(&a_t_r_current_null);
        }
        else {
          increment(&a_t_r_current_nonnull);
        }
        if (current == (tree_node *)0x0 || new == (tree_node *)0x0) break;
        if (current->height_maybe <= new->height_maybe) {
          if (*new_head_maybe == (tree_node *)0x0) {
                    // will be called for the first time
            increment(&a_t_r_created_new);
            *new_head_maybe = current;
          }
          else {
            increment(&a_t_r_created_not_new);
            created_el->next_or_left = current;
          }
          created_el = current;
          current_next = current->next_or_left;
          current->next_or_left = (tree_node *)0x0;
          increment(&a_t_r_created_branch1);
          current = current_next;
        }
        else {
          if (*new_head_maybe == (tree_node *)0x0) {
            increment(&INT_0060310c);
            *new_head_maybe = new;
          }
          else {
            increment(&INT_00603110);
            created_el->next_or_left = new;
          }
          created_el = new;
          current_next = new->next_or_left;
          new->next_or_left = (tree_node *)0x0;
          increment(&INT_00603114);
          new = current_next;
        }
      }
      while (current != (tree_node *)0x0) {
        if (*new_head_maybe == (tree_node *)0x0) {
          increment(&INT_00603118);
          *new_head_maybe = current;
        }
        else {
          increment(&INT_0060311c);
          created_el->next_or_left = current;
        }
        created_el = current;
        current_next = current->next_or_left;
        current->next_or_left = (tree_node *)0x0;
        increment(&INT_00603120);
        current = current_next;
      }
      while (new != (tree_node *)0x0) {
        if (*new_head_maybe == (tree_node *)0x0) {
          increment(&INT_00603124);
          *new_head_maybe = new;
        }
        else {
          increment(&INT_00603128);
          created_el->next_or_left = new;
        }
        created_el = new;
        current_next = new->next_or_left;
        new->next_or_left = (tree_node *)0x0;
        increment(&INT_0060312c);
        new = current_next;
      }
      increment(&INT_00603130);
      *old_head = (tree_node *)0x0;
      *new_part = (tree_node *)0x0;
      free_tree((tree_node *)old_head);
      free_tree((tree_node *)new_part);
      return new_head_maybe;
    }
    increment(&a_t_r_exit);
  }
  return (tree_node **)0x0;
}

// if old_head would be 0: Returns 0
int a_t_start;
int a_t_rek_null_return;
int a_t_no_next;
int a_t_height_equals;
int a_t_height_not_equal;
int a_t_smaller_input_null;
int a_t_smaller_input_byte;
int a_t_smaller_input_impossible;
int a_t_smaller_input_byte;
int a_t_next_equals_current;
int a_t_next_not_equals_current;
int a_t_height_differs;
int a_t_end;


tree_node ** append_tree(tree_node **old_head,tree_node **new_node)

{
  tree_node **new_head_ret;
  tree_node *next;
  tree_node *current;
  tree_node *prev;
  
  increment(&a_t_start);
  new_head_ret = append_tree_rek(old_head,new_node);
  if (*new_head_ret == (tree_node *)0x0) {
    increment(&a_t_rek_null_return);
  }
  else {
    prev = (tree_node *)0x0;
    current = *new_head_ret;
    next = current->next_or_left;
    while (next != (tree_node *)0x0) {
      if (current->height_maybe == next->height_maybe) {
        if (next->next_or_left == (tree_node *)0x0) {
          increment(&a_t_no_next);
        }
        else {
          if (next->next_or_left->height_maybe == current->height_maybe) {
            increment(&a_t_height_equals);
            goto APPEND_CONTINUE;
          }
          increment(&a_t_height_not_equal);
        }
        if ((byte)next->input_byte < (byte)current->input_byte) {
          if (prev == (tree_node *)0x0) {
            increment(&a_t_smaller_input_null);
            *new_head_ret = next;
          }
          else {
            increment((int *)&a_t_smaller_input_byte);
            prev->next_or_left = next;
          }
          if (current == next) {
                    // ptr->input_byte ==, ptr != -> impossible
            increment((int *)&a_t_smaller_input_impossible);
          }
          else {
            increment((int *)&a_t_smaller_input_byte);
            current->parent = next;
            current->next_or_left = next->tree_right;
            next->tree_right = current;
            next->height_maybe = next->height_maybe + 1;
          }
          current = next;
        }
        else {
          current->next_or_left = next->next_or_left;
          if (next == current) {
            increment(&a_t_next_equals_current);
          }
          else {
            increment(&a_t_next_not_equals_current);
            next->parent = current;
            next->next_or_left = current->tree_right;
            current->tree_right = next;
            current->height_maybe = current->height_maybe + 1;
          }
        }
      }
      else {
        increment(&a_t_height_differs);
APPEND_CONTINUE:
        prev = current;
        current = next;
      }
      next = current->next_or_left;
    }
    increment(&a_t_end);
  }
  return new_head_ret;
}

int add_tree_node_enter;
int add_tree_node_after_malloc;

void add_tree_node(tree_node **head_ptr,char input_byte)

{
  tree_node *new_tree_node;
  tree_node **new_tree_p;
  tree_node **local_RAX_204;
  tree_node **head_cpy;
  
  increment(&add_tree_node_enter);
  head_cpy = (tree_node **)*head_ptr;
  new_tree_node = (tree_node *)malloc(0x20);
  if (new_tree_node == (tree_node *)0x0) {
                    // WARNING: Subroutine does not return
    _exit(-3);
  }
  increment(&add_tree_node_after_malloc);
  new_tree_node->parent = (tree_node *)0x0;
  new_tree_node->next_or_left = (tree_node *)0x0;
  new_tree_node->tree_right = (tree_node *)0x0;
  new_tree_node->height_maybe = 0;
  new_tree_node->input_byte = input_byte;
  new_tree_p = new_tree_ptr();
  *new_tree_p = new_tree_node;
  local_RAX_204 = append_tree(head_cpy,new_tree_p);
  *(tree_node ***)head_ptr = local_RAX_204;
  return;
}

int *won_output_maybe;
int *won_output_end_val;
int *won_output_end_maybe;

void write_won_output_maybe(int *won_output_val,int *won_output_end_val)

{
  int *local_20;
  
  if ((won_output_val != won_output_end_val) && (local_20 = won_output_val, *won_output_val == 0)) {
    while (won_output_maybe = won_output_val, won_output_end_maybe = won_output_end_val,
          local_20 < won_output_end_val) {
      *local_20 = 0;
      local_20 = local_20 + 1;
    }
  }
  return;
}


// void deconstructor(void)

// {
//   byte *won_output_ptr;
  
//   increment(&deconstructor_started);
//   if (won_output_maybe == (byte *)0x0) {
//     increment(&won_output_is_0);
//   }
//   else {
//     if (won_output_end_maybe == (byte *)0x0) {
//       increment((int *)&won_output_end_null);
//     }
//     else {
//       if (won_output_maybe < won_output_end_maybe) {
//         won_output_ptr = won_output_maybe;
//         while (won_output_ptr < won_output_end_maybe) {
//           increment(&won_output_outputed);
//           printf("%02x",(ulong)*won_output_ptr);
//           won_output_ptr = won_output_ptr + 1;
//         }
//         increment(&won_output_ended);
//         puts("");
//       }
//       else {
//         increment(&won_output_failed);
//       }
//     }
//   }
//   return;
// }



// // returns length

// ulong read_input(char *buf)

// {
//   char *pcVar1;
//   size_t input_len;
//   ulong i;
  
//   increment(&read_input_started);
//   pcVar1 = fgets(buf,0x20,stdin);
//   if (pcVar1 == (char *)0x0) {
//                     // WARNING: Subroutine does not return
//     _exit(-1);
//   }
//   input_len = strlen(buf);
//   if (input_len < 4) {
//                     // WARNING: Subroutine does not return
//     _exit(-1);
//   }
//   if (buf[input_len - 1] == '\n') {
//     increment(&ends_with_newline);
//     buf[input_len - 1] = 0;
//     input_len = input_len - 1;
//   }
//   else {
//     increment(&ends_not_with_newline);
//   }
//   i = 0;
//   while( true ) {
//     if (input_len <= i) {
//       increment(&valid_string_read);
//       return input_len;
//     }
//     if ((byte)buf[i] < 0x20) break;
//     if (0x7e < (byte)buf[i]) {
//       increment(&non_ascii_found);
//       goto INVALID_CHAR;
//     }
//     increment(&valid_input_chars);
//     i = i + 1;
//   }
//   increment(&space_found);
// INVALID_CHAR:
//   fprintf(stderr,"Invalid Character\n");
//                     // WARNING: Subroutine does not return
//   _exit(-2);
// }
void print_tree_rek(tree_node *node, int recursion_depth, char start) {
  int i;
  int spaces = 10;
  if (!node) {
    return;
  }

  print_tree_rek(node->tree_right, recursion_depth + 1, 'v');

  printf("\n"); 
  for (int i = 0; i < (recursion_depth - 1) * spaces; i++) {
    printf(" "); 
  }
  if (recursion_depth) {
    printf("%c", start);
    for (int i = 0; i < spaces - 1; i++) {
      printf("-");
    }
  }
  printf("%c  [%u]\n", node->input_byte, node->height_maybe); 

  print_tree_rek(node->next_or_left, recursion_depth + 1, '^');
} 

void print_tree(tree_node ** head) {
  print_tree_rek(*head, 0, ' ');
}


void print_counters() {
  printf("\n>>> counters:\n"
  "a_t_smaller_input_null: %d\n"
  "a_t_smaller_input_byte(2x): %d\n"
  "a_t_smaller_input_impossible: %d\n"
  "a_t_next_equals_current: %d\n"
  "a_t_next_not_equals_current: %d\n\n",
  a_t_smaller_input_null,
  a_t_smaller_input_byte,
  a_t_smaller_input_impossible,
  a_t_next_equals_current,
  a_t_next_not_equals_current);
}

int program_started;
// read all values mod flag length at least once, store them in consecutive order in the output
// buffer
int main(int argc,char **argv)

{
  FILE *flag_fileno;
  ulong flag_content_len;
  char *flag;
  uint *int_input_buffer;
  ulong input_len;
  ulong flag_content_len_cpy = 0;
  tree_node **tree_ptr;
  uint local_8c;
  ulong local_88;
  void *local_80;
  char initial_input32 [64];
  ulong counter;
  void *local_30;
  size_t tell_output;
  FILE *fflag;
  char **argvcpy;
  
  increment(&program_started);
                    // 10 seconds time
                    // 
//   flag_fileno = fopen("flag","r");
//   if (flag_fileno == (FILE *)0x0) {
//     fprintf(stderr,"open flag failed\n");
//                     // WARNING: Subroutine does not return
//     _exit(-1);
//   }
//                     // 2 is probably SEEK_END (?)
//   fseek(flag_fileno,0,2);
//   flag_content_len = ftell(flag_fileno);
//   fseek(flag_fileno,0,0);
//                     // file size plus 1
//   flag = (char *)malloc(flag_content_len + 1);
//   if (flag == (char *)0x0) {
//                     // WARNING: Subroutine does not return
//     _exit(-1);
//   }
//   memset(flag,0,flag_content_len + 1);
//   fread(flag,1,flag_content_len,flag_fileno);
//   fclose(flag_fileno);
//   memset(initial_input32,0,0x40);
//   int_input_buffer = (uint *)malloc((flag_content_len + 1) * 4);
//   if (int_input_buffer == (uint *)0x0) {
//                     // WARNING: Subroutine does not return
//     _exit(-1);
//   }
//   memset(int_input_buffer,0,(flag_content_len + 1) * 4);
//   input_len = read_input(initial_input32);
//   flag_content_len_cpy = read_strange_int_input_buffer(int_input_buffer,flag_content_len);
  tree_ptr = new_tree_ptr();

  //char buf[] = "xaffgzbaaduxy";
  if (argc < 2) {
    printf("usage: gimme your tree-string");
    exit(1337);
  }
  char *buf = argv[1];

  input_len = strlen(buf);

  counter = 0;
  while (counter < input_len) {
    add_tree_node((tree_node **)&tree_ptr, buf[counter]); //initial_input32[counter]);
    //increment(&main_tree_loop_1);
    printf("\n==============\nRound %lu: Added [%c]:\n\n", counter, buf[counter]);
    print_tree(tree_ptr);
    //print_counters();
    counter = counter + 1;
  }
  counter = 0;
  while (counter < (flag_content_len_cpy & 0xffffffff)) {
    add_tree_node((tree_node **)&tree_ptr,flag[(ulong)int_input_buffer[counter]]);
    //increment(&main_tree_loop_2);
    counter = counter + 1;
  }
  //increment(&main_finished);
  //free(flag);
  free(int_input_buffer);
  free_tree((tree_node *)tree_ptr);
  return 0;
}


