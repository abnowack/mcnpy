from collections import namedtuple
from numpy import cumsum

header = namedtuple('header', 'fmtversion szax source atwgtr temp date n comments')
atwgtr_table = namedtuple('za', 'ratio')


def extract_substrings(string, substring_lengths, strip=False):
    """
    Utility function to extract consecutive substrings of specified lengths.
    Include case that if last element of substring_lengths is -1,
    it will set the last substring to the remaining characters

    Parameters
    ----------
    string : str
        Input string to break up into seperate substrings
    substring_lengths : list
        Int list of substring size.
        If less than size of string, the remaining characters are also returned
    strip : bool
        Indicates whether to strip whitespace from substrings

    Returns
    -------
    substrings : list
        The list of parsed substrings

    Examples
    --------
    >>> extract_substrings('333444455555', [3, 4, 5])
    >>> ('333', '4444', '55555')
    >>> extract_substrings('333444455555     1', [3, 4, 5, -1])
    >>> ('333', '4444', '55555', '     1')
    """

    positions = cumsum([0] + substring_lengths)
    substrings = []

    for i, pos_curr in enumerate(positions[:-1]):
        pos_next = positions[i+1]
        substr = string[pos_curr:pos_next]
        if strip:
            substr = substr.strip()
        substrings.append(substr)

    if positions[-1] < len(string):
        substrings.append(string[positions[-1]:])

    return substrings


def sza_to_string(s, z, a):
    """ Convert SZA to string id

    Parameters
    ----------
    s : int
        Excited State Number
    z : int
        Atomic Number
    a : int
        Atomic Mass Number

    Returns
    -------
    sza_str : str
        SSSZZZAAA formatted string
    """

    sza_str = '{:>03}{:>03}{:>03}'.format(s, z, a)

    return sza_str


def string_to_sza(sza_str):
    """Convert SZA string to s, z, a ints

    Parameters
    ----------
    sza_str : str
        Text representation in SSSZZZAAA format

    Returns
    -------
    s : int
        Excited State Number
    z : int
        Atomic Number
    a : int
        Atomic Mass Number
    """

    sza = int(sza_str)
    s = sza / 1000000
    z = (sza / 1000) % 1000
    a = sza % 1000

    return s, z, a


def ace_filename_to_szax(filename):
    """Convert filename to SZA and library identifiers, and data class

    Parameters
    ----------
    filename : str
        Name of ACE file in 'SSSZZZAAA.dddCC' format

    Returns
    -------
    s : int
    z : int
    a : int
    dd : int
    lib_id : str
    """
    prefix, sep, suffix = filename.partition('.')

    s, z, a = string_to_sza(prefix)
    dd = int(suffix[:3])
    lib_id = suffix[3:]

    return s, z, a, dd, lib_id


def read_header(ace_file):
    """ Convert header of ace file into named tuple

    Parameters
    ----------
    ace_file : file
        Opened ace file for parsing header information

    Returns
    -------
    header : namedtuple
        Contains parsed header information
    """
    line = ace_file.readline()
    fmtversion, szax, source = extract_substrings(line, [10, 24, 24], strip=True)

    sza_to_string()

    line = ace_file.readline()
    atwgtr, temp, date, n = extract_substrings(line, [11, 11, 8, -1], strip=True)
    comments = []
    for i in xrange(int(n)):
        # might consider changing if need to interpret string by position
        comments.append(ace_file.readline().strip())

    return header(fmtversion=fmtversion, szax=szax, source=source, 
                  atwgtr=atwgtr, temp=temp, date=date, n=n, 
                  comments=comments)