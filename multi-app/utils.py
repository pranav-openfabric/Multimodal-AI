import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
punkt_downloaded = True

# Max number of tokens a text can have
TOKEN_LIMIT_COUNT = 2000


def _count_approx_tokens(text: str) -> int:
    """
    Given a text, count the number of approximate word tokens
    to prevent exceeding the token limit of LLMs

    Args:
    text: string
    """
    global punkt_downloaded

    if not punkt_downloaded:
        nltk.download('punkt')
        punkt_downloaded = True

    tokens: list = word_tokenize(text)
    num_tokens: int = len(tokens)

    return num_tokens


def is_tokens_exceeded(text: str) -> bool:
    """
    Check if the token limit of words is exceeded in the given text
    """

    num_tokens: int = _count_approx_tokens(text)

    if num_tokens > TOKEN_LIMIT_COUNT:
        return True
    
    return False
