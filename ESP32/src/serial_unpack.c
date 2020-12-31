#include "serial_unpack.h"

void serial_unpack_bytes(SerialBytes * x, uint8_t id, uint32_t value) {
    x->rightmost = (uint8_t)(value & 255);
    uint8_t e_id = id << 4;
    x->leftmost = (uint8_t)(((value >> 8) & 255) | e_id);
}