#include <iostream>
#include "factorial.h"

int Factorial::compute(int x)
{
    return x <= 1 ? 1 : x * compute(x-1);
}
