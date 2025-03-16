def create_yiddish_sample():
    """Create a sample file that would decode to 'אויפן פסוק'"""
    # Define the bytes that should map to אויפן פסוק
    # according to our direct_decoder mapping
    yiddish_bytes = [
        # אויפן 
        0xC7, 0x02,  # א (Alef - using Unicode char \u02c7)
        0xC6, 0x02,  # ו (Vav - using Unicode char \u02c6)
        0x02,        # י (Yod)
        0x15,        # פ (Pe)
        0x06,        # נ (Nun)
        0x20,        # Space
        # פסוק
        0x15,        # פ (Pe)
        0x16,        # ס (Samech)
        0xC6, 0x02,  # ו (Vav - using Unicode char \u02c6)
        0x0c         # ק (Kuf)
    ]
    
    # Write to a file
    with open("yiddish_sample.txt", "wb") as f:
        f.write(bytes(yiddish_bytes))
    
    print("Created sample file that should decode to 'אויפן פסוק'")
    
    # Test decoding it
    from direct_decoder import direct_decode
    direct_decode("yiddish_sample.txt", "yiddish_sample_decoded.txt")

if __name__ == "__main__":
    create_yiddish_sample() 