#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>

int count_digits(long long number);
bool card_number_valid(long long number);
int get_first_2_digits(long long number);

int main() {
  long long number;
  do {
    number = get_long_long("Number: ");
  } while (number < 1);

  int totalDigits = count_digits(number);
  if (totalDigits < 13 || totalDigits > 16) {
    printf("INVALID\n");
    return 1;
  }

  if (!card_number_valid(number)) {
    printf("INVALID\n");
    return 1;
  }

  int first2Digits = get_first_2_digits(number);

  if (first2Digits >= 34 && first2Digits <= 37) {
    printf("AMEX\n");
  } else if (first2Digits >= 51 && first2Digits <= 55) {
    printf("MASTERCARD\n");
  } else if (first2Digits / 10 == 4) {
    printf("VISA\n");
  } else {
    printf("INVALID\n");
    return 1;
  }
}

int get_first_2_digits(long long number) {
  while (number > 99) {
    number /= 10;
  }
  return number;
}

int count_digits(long long number) {
  int count = 0;
  while (number != 0) {
    count += 1;
    number /= 10;
  }
  return count;
}

bool card_number_valid(long long number) {
  bool mutiplyBy2 = false;
  int rem;
  int tempSum;
  int total = 0;

  while (number != 0) {
    rem = number % 10;
    if (mutiplyBy2) {
      tempSum = rem * 2;
      while (tempSum != 0) {
        total += (tempSum % 10);
        tempSum /= 10;
      }
      mutiplyBy2 = false;
    } else {
      total += rem;
      mutiplyBy2 = true;
    }
    number /= 10;
  }

  return (total % 10) == 0;
}
