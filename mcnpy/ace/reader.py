def sza_to_string(s, z, a):
    ''' Convert SZA to string id '''

    sza_str = '{:>03}{:>03}{:>03}'.format(s, z, a)

    return sza_str

def string_to_sza(sza_str):
    ''' Convert SZA id string to SZA values '''

    s, z, a = None, None, None

    if len(sza_str) != 9:
        return s, z, a

    s = int(sza_str[:3])
    z = int(sza_str[3:6])
    a = int(sza_str[6:])

    return s, z, a

def ace_filename_to_szax(filename):
    ''' Convert filename to SZA and library identifiers, and data class '''
    prefix, suffix = filename.partition('.')

    library_id = suffix[:3]