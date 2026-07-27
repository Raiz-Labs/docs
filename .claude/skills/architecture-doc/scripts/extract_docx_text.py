#!/usr/bin/env python3
"""Extract plain text from a .docx file's word/document.xml, stdlib only."""
import html
import io
import re
import sys
import zipfile


def extract_text(docx_path: str) -> str:
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    text = re.sub(r"<w:p(?: [^>]*)?/?>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def _demo() -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "word/document.xml",
            "<w:document><w:body>"
            "<w:p><w:r><w:t>Ol&#225; mundo</w:t></w:r></w:p>"
            "<w:p><w:r><w:t>Segunda linha</w:t></w:r></w:p>"
            "<w:p w:rsidR=\"00A12B\"><w:r><w:t>Terceira linha</w:t></w:r></w:p>"
            "</w:body></w:document>",
        )
    tmp_path = "/tmp/_architecture_doc_selftest.docx"
    with open(tmp_path, "wb") as f:
        f.write(buf.getvalue())

    result = extract_text(tmp_path)
    expected = "Olá mundo\nSegunda linha\nTerceira linha"
    assert result == expected, f"unexpected output: {result!r}"
    assert "rsidR" not in result, result
    print("self-test OK")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        _demo()
    elif len(sys.argv) == 2:
        print(extract_text(sys.argv[1]))
    else:
        print("usage: extract_docx_text.py <path.docx> | --selftest", file=sys.stderr)
        sys.exit(1)
