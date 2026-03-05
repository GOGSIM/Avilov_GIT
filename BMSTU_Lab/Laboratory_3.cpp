#include <stdio.h>

int main() {
    int n;
    int count = 0; 

    printf("Введите целое число: ");
    scanf("%d", &n);

    for ( ; n > 0; n /= 10) {
        int digit = n % 10;       
        if (digit % 2 != 0) {     
            count++;
        }
    }

    printf("Количество нечетных цифр: %d\n", count);

    return 0;
}
