"""
VNI to Unicode font character mapping for Vietnamese text
"""

VNI_TO_UNICODE = {
    # Lowercase vowels with marks
    'à': 'à', 'á': 'á', 'ả': 'ả', 'ã': 'ã', 'ạ': 'ạ',
    'ă': 'ă', 'ằ': 'ằ', 'ắ': 'ắ', 'ẳ': 'ẳ', 'ẵ': 'ẵ', 'ặ': 'ặ',
    'â': 'â', 'ầ': 'ầ', 'ấ': 'ấ', 'ẩ': 'ẩ', 'ẫ': 'ẫ', 'ậ': 'ậ',
    
    'è': 'è', 'é': 'é', 'ẻ': 'ẻ', 'ẽ': 'ẽ', 'ẹ': 'ẹ',
    'ê': 'ê', 'ề': 'ề', 'ế': 'ế', 'ể': 'ể', 'ễ': 'ễ', 'ệ': 'ệ',
    
    'ì': 'ì', 'í': 'í', 'ỉ': 'ỉ', 'ĩ': 'ĩ', 'ị': 'ị',
    
    'ò': 'ò', 'ó': 'ó', 'ỏ': 'ỏ', 'õ': 'õ', 'ọ': 'ọ',
    'ô': 'ô', 'ồ': 'ồ', 'ố': 'ố', 'ổ': 'ổ', 'ỗ': 'ỗ', 'ộ': 'ộ',
    'ơ': 'ơ', 'ờ': 'ờ', 'ớ': 'ớ', 'ở': 'ở', 'ỡ': 'ỡ', 'ợ': 'ợ',
    
    'ù': 'ù', 'ú': 'ú', 'ủ': 'ủ', 'ũ': 'ũ', 'ụ': 'ụ',
    'ư': 'ư', 'ừ': 'ừ', 'ứ': 'ứ', 'ử': 'ử', 'ữ': 'ữ', 'ự': 'ự',
    
    'ỳ': 'ỳ', 'ý': 'ý', 'ỷ': 'ỷ', 'ỹ': 'ỹ', 'ỵ': 'ỵ',
    
    # Uppercase vowels with marks
    'À': 'À', 'Á': 'Á', 'Ả': 'Ả', 'Ã': 'Ã', 'Ạ': 'Ạ',
    'Ă': 'Ă', 'Ằ': 'Ằ', 'Ắ': 'Ắ', 'Ẳ': 'Ẳ', 'Ẵ': 'Ẵ', 'Ặ': 'Ặ',
    'Â': 'Â', 'Ầ': 'Ầ', 'Ấ': 'Ấ', 'Ẩ': 'Ẩ', 'Ẫ': 'Ẫ', 'Ậ': 'Ậ',
    
    'È': 'È', 'É': 'É', 'Ẻ': 'Ẻ', 'Ẽ': 'Ẽ', 'Ẹ': 'Ẹ',
    'Ê': 'Ê', 'Ề': 'Ề', 'Ế': 'Ế', 'Ể': 'Ể', 'Ễ': 'Ễ', 'Ệ': 'Ệ',
    
    'Ì': 'Ì', 'Í': 'Í', 'Ỉ': 'Ỉ', 'Ĩ': 'Ĩ', 'Ị': 'Ị',
    
    'Ò': 'Ò', 'Ó': 'Ó', 'Ỏ': 'Ỏ', 'Õ': 'Õ', 'Ọ': 'Ọ',
    'Ô': 'Ô', 'Ồ': 'Ồ', 'Ố': 'Ố', 'Ổ': 'Ổ', 'Ỗ': 'Ỗ', 'Ộ': 'Ộ',
    'Ơ': 'Ơ', 'Ờ': 'Ờ', 'Ớ': 'Ớ', 'Ở': 'Ở', 'Ỡ': 'Ỡ', 'Ợ': 'Ợ',
    
    'Ù': 'Ù', 'Ú': 'Ú', 'Ủ': 'Ủ', 'Ũ': 'Ũ', 'Ụ': 'Ụ',
    'Ư': 'Ư', 'Ừ': 'Ừ', 'Ứ': 'Ứ', 'Ử': 'Ử', 'Ữ': 'Ữ', 'Ự': 'Ự',
    
    'Ỳ': 'Ỳ', 'Ý': 'Ý', 'Ỷ': 'Ỷ', 'Ỹ': 'Ỹ', 'Ỵ': 'Ỵ',
    
    # ð with marks (VNI specific)
    'ð': 'đ', 'Ð': 'Đ',
}

# Create reverse mapping (Unicode to VNI)
UNICODE_TO_VNI = {v: k for k, v in VNI_TO_UNICODE.items()}

# VNI Font names to detect
VNI_FONTS = [
    'VNI-Times',
    'VnTimes',
    'VNTimes',
    'VnArial',
    'VNArial',
    '.VnArial',
    'VN-Arial',
    'Times New Roman VNI',
    'Arial VNI',
]

# Unicode fonts (standard)
UNICODE_FONTS = [
    'Times New Roman',
    'Arial',
    'Calibri',
    'Segoe UI',
    'Courier New',
]


def vni_to_unicode(text):
    """Convert VNI encoded text to Unicode"""
    result = []
    for char in text:
        result.append(VNI_TO_UNICODE.get(char, char))
    return ''.join(result)


def unicode_to_vni(text):
    """Convert Unicode text to VNI encoded"""
    result = []
    for char in text:
        result.append(UNICODE_TO_VNI.get(char, char))
    return ''.join(result)


def is_vni_font(font_name):
    """Check if font is VNI encoded"""
    if not font_name:
        return False
    for vni_font in VNI_FONTS:
        if vni_font.lower() in font_name.lower():
            return True
    return False


def is_unicode_font(font_name):
    """Check if font is Unicode"""
    if not font_name:
        return False
    for uni_font in UNICODE_FONTS:
        if uni_font.lower() in font_name.lower():
            return True
    return False
