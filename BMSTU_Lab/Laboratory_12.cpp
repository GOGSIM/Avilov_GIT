#include <stdio.h>
#include <time.h>
#include <stdlib.h>

void printMatrix(int **M, int rows, int cols, const char *title){
    printf("\n%s (%d x %d):\n", title, rows, cols);
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            printf("%6d ", *(*(M+i)+j));
        }
        printf("\n");
    }
}

void inputMatrix(int **M, int rows, int cols){
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            *(*(M + i)+j) = rand() % 199 - 99;
        }
    }
}

void freeMatrix(int **M, int rows){
    for (int i = 0; i < rows; i++){
        delete[] *(M+i);
    }
    delete[] M;
}

void solution(int **A, int **B, int n){
    int rows = n + 1;
    int cols = n;

    printf("\nMax elements addresses (one per column):\n");
    printf("Col | MaxValue | Address\n");
    printf("----+----------+-----------------\n");

    for (int j = 0; j < cols; j++){
        int maxRow = 0;
        int maxVal = *(*(A + 0) + j);

        for (int i = 1; i < rows; i++){
            int val = *(*(A+i)+j);
            if (val > maxVal){
                maxVal = val;
                maxRow = i;
            }
        }

        int* pMax = (*(A + maxRow) + j);
        printf("%3d | %8d | %p\n", j + 1, maxVal, (void*)pMax);

        int bi = 0;
        for (int i = 0; i < rows; i++){
            if(i != maxRow){
                *(*(B +bi)+j) = *(*(A+i)+j);
                bi++;
            }
        }
    }
}

int main(){
    srand((unsigned)time(NULL));

    int n;
    printf("Input size of matrix((N+1) x N): ");
    scanf("%d", &n);

    int rows = n + 1;
    int cols = n;

    int** A = new int*[rows];
    for (int i = 0; i < rows; i++) {
        *(A+i) = new int[cols];
    }

    int** B = new int*[n];
    for (int i = 0; i < n; i++) {
        *(B+i) = new int[n];
    }

    inputMatrix(A, rows, cols);
    printMatrix(A, rows, cols, "Original matrix A");

    solution(A, B, n);

    printMatrix(B, n, n, "Result matrix B");

    freeMatrix(A, rows);
    freeMatrix(B, n);

    return 0;
}
