import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import unicodedata


# Excluded because only possible with combining diacritics: U̇, u̇, y̋
TEXT = {
    "l.0": "AÀÁÂÃÄÅĂĀĄÆBCĆĈČĊÇDĎÐEÈÉÊËĚĒĖȨFGĜĞĠĢHĤĦIÌÍÎĨÏǏĪİ",
    "l.1": "ĮJĴKĶLĹĽĻMNŃÑŇŅOÒÓÔÕÖŐŌØPQRŔŘŖSŚŜŠŞTŤŢȾUÙÚÛŨÜŮŰŬ",
    "l.2": "Ū ŲVWXYÝZŹŽŻaàáâãäåăāæbcćĉčçdďðeèéêëěėȩfgĝğġhĥħi",
    "l.3": "ìíîĩïīįjkķlĺľļłmnńñňņŋoòóôõöőōøºœpþqrŕřŗsŝšştťţⱦ",
    "l.4": "uùúũüůűū ųvwxyý zß01234567 89+-×/±=≡÷<>≤≥«»()[]{",
    "l.5": "}%∞√≈~!?&'\",;.:\\_∑∫∡⊳⊲≠#≙□∅  $¢£¥₧@©®℄↷ ⋂",
    "g.0": "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
    "e.0": "*",  # Extra glyphs
}

SVG_FONT_HEADER = \
"""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
<metadata>
Font name:               Norm Stroke
License:                 This work is marked with CC0 1.0. To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/
A derivative of:         https://commons.wikimedia.org/wiki/File:ISO3098.svg
Version:                 1.0
</metadata>
<defs>
<font id="NormStroke" horiz-adv-x="350" >
<font-face
font-family="Norm Stroke"
units-per-em="1000"
ascent="800"
descent="200"
cap-height="800"
x-height="560"
/>
<missing-glyph horiz-adv-x="480" />
<glyph unicode=" " horiz-adv-x="480" />
"""
SVG_FONT_FOOTER = \
"""
</font>
</defs>
</svg>
"""


def generate_svg_font(sourcedir, outpath):
    """Generate a SVG font from the SVG glyphs located in sourcedir"""
    s = SVG_FONT_HEADER
    for fname in sorted(os.listdir(sourcedir)):
        char = TEXT[fname[:3]][int(fname[4:6].rstrip("_"))]
        char_esc = escape(char)\
            .replace('"', "&quot;")
                                  
        width = fname.split("_")[1].split(".")[0]

        tree = ET.parse(os.path.join(sourcedir, fname))
        root = tree.getroot()
        path_d = " ".join([el.attrib["d"] for el in root[1:]])

        if char != " ":  # These are ignored
            s+= f'<glyph unicode="{char_esc}" horiz-adv-x="{width}" d="{path_d}" />\n'

    s += SVG_FONT_FOOTER

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(s)


if __name__ == "__main__":
    generate_svg_font("glyphs", "font/NormStroke.svg")
