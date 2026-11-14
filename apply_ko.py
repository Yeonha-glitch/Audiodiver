#!/usr/bin/env python3
"""Apply unofficial, partial Korean UI and core translations to Audiodiver 1.7.2."""
import json
import sys
from pathlib import Path
from ko_strings import UI, CORE, DATA

def sub(path, old, new):
    s=path.read_text(encoding="utf-8")
    if new in s:
        return
    if s.count(old)!=1:
        raise RuntimeError(f"Unexpected source at {path}: {old!r}")
    path.write_text(s.replace(old,new,1),encoding="utf-8")

def q(s):
    return json.dumps(s,ensure_ascii=False)

def po(path, mapping):
    path.parent.mkdir(parents=True,exist_ok=True)
    rows=['msgid ""','msgstr ""',q("Content-Type: text/plain; charset=utf-8\n"),q("Language: ko\n"),q("Plural-Forms: nplurals=1; plural=0;\n"),'']
    for key,val in sorted(mapping.items()):
        if val and key!=val:
            rows += [f"msgid {q(key)}",f"msgstr {q(val)}",""]
    path.write_text("\n".join(rows),encoding="utf-8")

def main(root):
    root=Path(root)
    assert json.loads((root/"app/package.json").read_text(encoding="utf-8"))["version"]=="1.7.2", "Only v1.7.2 is supported"
    sub(root/"app/src/i18n.ts",'  { tag: "ja", name: "日本語" },','  { tag: "ja", name: "日本語" },\n  { tag: "ko", name: "한국어" },')
    sub(root/"app/lingui.config.ts",'"ja", "pseudo"','"ja", "ko", "pseudo"')
    sub(root/"app/src-tauri/tauri.conf.json",'"Japanese"], "displayLanguageSelector"','"Japanese", "Korean"], "displayLanguageSelector"')
    po(root/"app/src/locales/ko/messages.po",UI)
    po(root/"core/audiodiver/locale/ko.po",CORE)
    p=root/"core/audiodiver/locale/data/ko.json"
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    p=root/"app/src-tauri/tauri.ko-build.conf.json"
    p.write_text(json.dumps({"bundle":{"createUpdaterArtifacts":False,"resources":["core/**/*"]}},indent=2)+"\n",encoding="utf-8")
    print(f"Korean patch applied: UI {len(UI)} / core {len(CORE)} / catalog {len(DATA)} (partial)")

if __name__=="__main__":
    main(sys.argv[1])
