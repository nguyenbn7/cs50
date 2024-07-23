#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>

#define QUARTERS_TO_CENTS 25
#define DIMES_TO_CENTS 10
#define NICKELS_TO_CENTS 5

int get_changes(int *cents, int threshold);
void print_changes(int changes, char *const singular, char *const plural,
                   bool last);

int main() {
  int cents;
  do {
    cents = get_int("Change owned: ");
  } while (cents < 0);

  int quarters = get_changes(&cents, QUARTERS_TO_CENTS);
  print_changes(quarters, "quarter", "quarters", cents <= 0);

  int dimes = get_changes(&cents, DIMES_TO_CENTS);
  print_changes(dimes, "dime", "dimes", cents <= 0);

  int nickels = get_changes(&cents, NICKELS_TO_CENTS);
  print_changes(nickels, "nickel", "nickels", cents <= 0);

  print_changes(cents, "penny", "pennies", true);
}

int get_changes(int *cents, int threshold) {
  int changes = 0;
  if (*cents >= threshold) {
    changes = *cents / threshold;
    *cents = *cents - (changes * threshold);
  }
  return changes;
}

void print_changes(int changes, char *const singular, char *const plural,
                   bool last) {

  if (changes < 1)
    return;

  if (changes == 1) {

    printf("%d %s", changes, singular);

    if (!last)
      printf(", ");
    else
      printf("\n");
    return;
  }

  printf("%d %s", changes, plural);
  if (!last)
    printf(", ");
  else
    printf("\n");
}