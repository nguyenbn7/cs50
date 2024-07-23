#include <cs50.h>
#include <stdio.h>

void print_row(int spaces, int bricks) {
  for (int i = 0; i < spaces; i++) {
    printf(" ");
  }
  for (int i = 0; i < bricks; i++) {
    printf("#");
  }

  printf("  ");
  for (int i = 0; i < bricks; i++) {
    printf("#");
  }

  printf("\n");
}

int main() {
  int n;
  int bricks;
  int spaces;

  do {
    n = get_int("Height: ");
  } while (n < 1 || n > 8);

  for (int i = 0; i < n; i++) {
    bricks = i + 1;
    spaces = n - bricks;
    print_row(spaces, bricks);
  }
}
