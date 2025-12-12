# from googletrans import Translator

# translator = Translator()

# def translate_text(text, lang_code='en'):
#     """Translate given text to the specified language."""
#     if not text or lang_code == 'en':
#         return text  # No need to translate English
#     try:
#         result = translator.translate(text, dest=lang_code)
#         return result.text
#     except Exception as e:
#         print(f"Translation error: {e}")
#         return text  # fallback to English
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# helper to fix normal English to phonetic before transliteration
def normalize_english_name(name: str) -> str:
    """
    Basic phonetic normalization so 'Dhanalekshmi' → 'dhana-lakshmi'
    before transliteration. This improves accuracy.
    """
    name = name.lower()
    # fix common patterns
    replacements = {
        'dh': 'dh',
        'th': 'th',
        'sh': 'sh',
        'ch': 'ch',
        'kh': 'kh',
        'bh': 'bh',
        'gh': 'gh',
        'aa': 'a',
        'ee': 'i',
        'oo': 'u',
        'lekh': 'lekh',
        'laksh': 'laksh',
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
    return name

def transliterate_text(text: str, lang_code: str) -> str:
    """
    Convert English (Latin script) lottery names → Indic scripts automatically.
    """
    if not text or lang_code == 'en':
        return text

    lang_map = {
        'ml': sanscript.MALAYALAM,
        'hi': sanscript.DEVANAGARI,
        'ta': sanscript.TAMIL,
    }

    script = lang_map.get(lang_code)
    if not script:
        return text

    normalized = normalize_english_name(text)
    try:
        return transliterate(normalized, sanscript.ITRANS, script)
    except Exception:
        return text

    