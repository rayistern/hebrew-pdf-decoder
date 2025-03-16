def test_yiddish_mapping():
    """Test our mapping with the known Yiddish text 'אויפן פסוק'"""
    # Create expected encoding based on our observed patterns
    expected_text = "אויפן פסוק"
    
    # Define our test cases with proper byte values
    # For Unicode characters, use their actual byte representation
    yiddish_bytes = [
        # אויפן
        0xC7, 0x02,  # א - Alef (actually \u02c7, but need to use bytes)
        0xC6, 0x02,  # ו - Vav (actually \u02c6)
        0x02,        # י - Yod
        0x15,        # פ - Pe
        0x06,        # ן - Final Nun (using regular nun here)
        0x04,        # Space
        # פסוק
        0x15,        # פ - Pe
        0x16,        # ס - Samech
        0xC6, 0x02,  # ו - Vav (actually \u02c6)
        0x0c,        # ק - Kuf
    ]
    
    # Write our test file directly as bytes
    with open("yiddish_test.txt", "wb") as f:
        f.write(bytes(yiddish_bytes))
    
    print("Created test file with encoded Yiddish text")
    
    # Now run our decoder on this test file
    from pattern_mapping import decode_with_patterns
    decode_with_patterns("yiddish_test.txt", "yiddish_decoded.txt")
    
    # Verify the result
    with open("yiddish_decoded.txt", "r", encoding="utf-8") as f:
        decoded = f.read()
    
    print(f"Expected text: {expected_text}")
    print(f"Decoded text:  {decoded}")
    print(f"Match: {'✓' if decoded.strip() == expected_text else '✗'}")

if __name__ == "__main__":
    test_yiddish_mapping() 