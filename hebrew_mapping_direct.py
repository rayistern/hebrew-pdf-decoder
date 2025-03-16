def create_direct_hebrew_mapping():
    # Direct mapping based on image comparison with character codes
    mapping = {
        # Common characters
        '\x04': ' ',   # Space (most frequent)
        '\x02': 'י',   # Yod (common)
        '\x03': 'ר',   # Resh
        '\x01': 'ת',   # Tav
        
        # Hebrew letters
        '\x05': 'ב',   # Bet
        '\x06': 'נ',   # Nun
        '\x07': 'ח',   # Chet
        '\x0e': 'ך',   # Final Kaf
        '\x0f': 'ד',   # Dalet
        '\x10': 'ג',   # Gimel
        '\x11': 'ע',   # Ayin
        '\x12': 'כ',   # Kaf
        '\x13': 'צ',   # Tsadi
        '\x14': 'מ',   # Mem
        '\x15': 'פ',   # Pe
        '\x16': 'ס',   # Samech
        '\x17': 'ף',   # Final Pe
        
        # Extended Unicode characters
        '\u02d9': 'א', # Alef - '˙'
        '\u02c7': 'א', # Alternative Alef - 'ˇ'
        '\u02c6': 'ו', # Vav - 'ˆ'
        '\u02d8': '.', # Period - '˘' 
        '\u02dd': 'ז', # Zayin - '˝'
        '\u02db': 'ה', # He - '˛'
        '\u00b0': "'", # Apostrophe - '°'
        '\u02dc': ')', # Right parenthesis - '˜'
        
        # ASCII characters 
        '!': 'ש',      # Shin
        '"': 'ל',      # Lamed
        '#': 'ם',      # Final Mem
        
        # Ensure proper punctuation
        '(': '(',
        ')': ')',
        ',': ',',
        ':': ':',
    }
    return mapping 