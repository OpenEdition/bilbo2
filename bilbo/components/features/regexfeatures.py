""" regular expression features """
import re


class RegexFeature:
    """
    generate features based on regular expressions
    """
    def __init__(self, name, pattern):
        self._regexp = re.compile(pattern)
        self._name = name

    def __call__(self, section, token_id):
        """
        return the value of the regexp given in the config file

        :param section: section of tokens
        :param token_id: id of the token

        :returns: value of the regexp
        """
        token = section.token_str_lst[token_id][0]
        return self._name if self._regexp.search(token) \
                else ''.join(('NO', self._name))
