// Define the interface to the word library.

class Word
{
    const char *the_word;


public:
    Word(const char *w);

    const char *reverse() const;
};
