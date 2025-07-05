#include <assert.h>
#include "sample.hpp"

int main() {
    assert(add(1, 1) == 2);
    assert(add(2, 3) == 5);
    assert(add(-4, 6) == 2);
}