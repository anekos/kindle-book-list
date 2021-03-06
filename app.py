from pathlib import Path
from typing import Set
import re
import xml.etree.ElementTree as ET

import click
import mojimoji


TypePath = click.types.Path(path_type=Path)


def cleanup_title(s: str) -> str:
    s = mojimoji.zen_to_han(s, kana=False).strip()
    s = re.sub(r'''\(.+\)''', '', s)
    s = re.sub(r'''（.+）''', '', s)
    s = re.sub(r'''(?i)(第|vol\.?)?\s*\d+\s*[巻]?.*''', '', s)
    s = re.sub(r'''【.+版】''', '', s)
    s = re.sub(r''':''', '', s)
    s = re.sub(r'''[上下]\s*$''', '', s)
    s = re.sub(r''' [上下全][巻]? .*$''', '', s)
    return s.strip()


def is_sample(s: str) -> bool:
    if '期間限定' in s:
        return True
    return False


@click.command()
@click.argument('xml-file', type=TypePath, required=True)
def main(xml_file: Path) -> None:
    tree = ET.parse(xml_file)
    add_update_list = tree.find('add_update_list')
    assert add_update_list is not None

    titles: Set[str] = set()

    for child in add_update_list:
        title = child.find('title')
        assert title is not None
        assert title.text is not None
        tt = title.text.strip()
        if is_sample(tt):
            continue
        titles.add(cleanup_title(tt))

    for it in sorted(titles):
        print(it)


if __name__ == "__main__":
    main()
