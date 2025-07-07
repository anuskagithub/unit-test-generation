#include "sample.hpp"
#include <cassert>

int main() {
    assert(add(1, 2) == 3);
    assert(add(-5, 5) == 0);
    assert(add(0, 0) == 0);

    return 0;
}
