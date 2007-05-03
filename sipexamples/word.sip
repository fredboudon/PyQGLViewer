// Define the SIP wrapper to the word library.

%Module word 0

class Word {

%TypeHeaderCode
#include "word.h"
%End

public:
    Word(const char *w);

    const char *reverse() const;
};
