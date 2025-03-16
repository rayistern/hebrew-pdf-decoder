def create_new_hebrew_mapping():
    mapping = {
        # Map spaces
        '\x04': ' ',  # Most common character, likely space
        
        # Common Hebrew letters (based on frequency in Hebrew language)
        '˙': 'א',  # Alef - very common
        'ˇ': 'א',  # Another representation of Alef
        '˛': 'ה',  # He - very common
        '\x02': 'י',  # Yod - very common
        '"': 'ל',  # Lamed - common
        '\x14': 'מ',  # Mem - common
        '#': 'מ',  # Another representation of Mem
        '\x06': 'נ',  # Nun - common
        '\x03': 'ר',  # Resh - common
        '!': 'ש',  # Shin - common
        '\x01': 'ת',  # Tav
        
        # Less common Hebrew letters
        '\x05': 'ב',  # Bet
        '\x10': 'ג',  # Gimel
        '\x0f': 'ד',  # Dalet
        'ˆ': 'ו',  # Vav
        '˝': 'ז',  # Zayin
        '\x07': 'ח',  # Chet
        '\x0b': 'ט',  # Tet
        '\x12': 'כ',  # Kaf
        '\x0e': 'ך',  # Final Kaf
        '\x16': 'ס',  # Samech
        '\x11': 'ע',  # Ayin
        '\x15': 'פ',  # Pe
        '\x17': 'ף',  # Final Pe
        '\x13': 'צ',  # Tsadi
        '\x0c': 'ק',  # Kuf
        
        # Punctuation
        '˘': '.',  # Period
        '°': "'",  # Apostrophe
        '˜': ')',  # Right parenthesis
    }
    return mapping 