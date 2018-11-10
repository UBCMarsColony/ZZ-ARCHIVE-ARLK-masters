#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>

int main(void) {
	int a[8], b[8], p1, p2, p3, error;

	printf("Enter a databit:");
	scanf("%d", &a[3]);
	printf("Enter a databit:");
	scanf("%d", &a[5]);
	printf("Enter a databit:");
	scanf("%d", &a[6]);
	printf("Enter a databit:");
	scanf("%d", &a[7]);

	a[1] = a[3] ^ a[5] ^ a[7];
	a[2] = a[3] ^ a[6] ^ a[7];
	a[4] = a[5] ^ a[6] ^ a[7];

	for (int i = 1; i < 8; i++) {
		printf("%d ", a[i]);
	}
	printf("\n");

	for (int i = 1; i < 8; i++) {
		printf("Enter the data: ");
		scanf("%d", &b[i]);
	}

	p1 = b[1] ^ b[3] ^ b[5] ^ b[7];
	p2 = b[2] ^ b[3] ^ b[6] ^ b[7];
	p3 = b[4] ^ b[5] ^ b[6] ^ b[7];

	error = p1 * 1 + p2 * 2 + p3 * 4;

	if (error == 0)
		printf("There is no error.\n");
	else {
		printf("There is an error in position %d.", error);

		printf("\n");

		if (b[error] == 0)
			b[error] = 1;
		else
			b[error] = 0;
		for (int i = 1; i < 8; i++)
			printf("%d ", b[i]);
		printf("\n");
	}
	system("PAUSE");
	return 0;
}

