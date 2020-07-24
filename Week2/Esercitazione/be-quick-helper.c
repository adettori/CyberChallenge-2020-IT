#include <stdlib.h>
#include <string.h>
#include <stdio.h>

ulong calc(uint param_1, uint *arr)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint local_1c;

  if(arr[param_1] != 0)
	  return arr[param_1];
  
  if (param_1 < 5) {
    local_1c = param_1 * param_1 + 0x2345;
  }
  else {
    iVar1 = calc((ulong)(param_1 - 1), arr);
    iVar2 = calc((ulong)(param_1 - 2), arr);
    iVar3 = calc((ulong)(param_1 - 3), arr);
    iVar4 = calc((ulong)(param_1 - 4), arr);
    iVar5 = calc((ulong)(param_1 - 5), arr);
    local_1c = iVar5 * 0x1234 + (iVar1 - iVar2) + (iVar3 - iVar4);
  }

  arr[param_1] = local_1c;

  return (ulong)local_1c;
}

int main(void) {

	uint arg = 104805;

	uint *arr = malloc(sizeof(uint)*arg);
	memset(arr, 0, arg);

	printf("%ld\n", calc(arg, arr));

	free(arr);

	return 0;
}
