"""Embed the YAFOWIL dict and array widget icons in their CSS (image build).

yafowil.plone concatenates the widgets' default/widget.css into one Plone
bundle, so their relative url('images/icon_*.png') references no longer
resolve and the add/remove/move buttons of the LDAP control panel are blank.
Replace each reference with a data: URL of the image next to the CSS file.
"""
import base64
import glob
import os
import re
import sys

PATTERN = re.compile(r"url\(\s*'?(images/[^')]+)'?\s*\)")


def inline(css_path):
    css_dir = os.path.dirname(css_path)

    def data_url(match):
        with open(os.path.join(css_dir, match.group(1)), "rb") as image:
            data = base64.b64encode(image.read()).decode("ascii")
        return "url('data:image/png;base64,%s')" % data

    with open(css_path) as css_file:
        css = css_file.read()
    css, count = PATTERN.subn(data_url, css)
    with open(css_path, "w") as css_file:
        css_file.write(css)
    return count


def main(site_packages):
    paths = glob.glob(
        os.path.join(site_packages, "yafowil/widget/*/resources/default/widget.css")
    )
    for path in sorted(paths):
        print("%s: %d icons embedded" % (path, inline(path)))
    if not paths:
        sys.exit("no YAFOWIL widget CSS found in %s" % site_packages)


if __name__ == "__main__":
    main(sys.argv[1])
