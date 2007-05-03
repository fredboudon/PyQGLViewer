#include "word.h"

Word::Word(const char *w)
{
the_word = w;
}

const char * Word::reverse() const
{
return the_word;
}
