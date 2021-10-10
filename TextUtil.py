def compare_text(text1, text2):
    if type(text1).__name__ == 'str' and type(text2).__name__ == 'str':
        text1 = text1.strip()
        text1 = text1.replace('-', '-')
        text1 = text1.replace('‑', '-')
        text2 = text2.strip()
        text2 = text2.replace('-', '-')
        text2 = text2.replace('‑', '-')

        is_same = text1 == text2
        return text1 == text2
    else:
        raise Exception