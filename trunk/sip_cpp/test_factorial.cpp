#include <iostream>
#include "factorial.h"

int main()
{

    int value = 5;
    Factorial fact;

    std::cout << "Factorial(" << value << ") = " << fact.compute(value) << std::endl;

    return 0;
}

