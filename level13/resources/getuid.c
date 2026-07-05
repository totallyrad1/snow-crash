/* level13: override getuid() to satisfy the binary's "expect 4242" check.
 * Preloaded (LD_PRELOAD) into a NON-setuid copy of the level13 binary, so the
 * loader honours it (LD_PRELOAD is ignored for setuid binaries). */
#include <sys/types.h>

uid_t getuid(void) { return 4242; }
