#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可选离线校验：仅Python标准库，不联网、不改文件、不加载模型。"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def verify(root):
    root = Path(root).resolve()
    path = root / 'manifest.json'
    if path.is_symlink():
        raise ValueError('manifest不能是符号链接')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    names = [item['path'] for item in manifest['files']]
    if len(names) != len(set(names)):
        raise ValueError('清单包含重复路径')
    actual = set()
    for candidate in root.rglob('*'):
        if candidate.is_symlink():
            raise ValueError('包内不能包含符号链接')
        if candidate.is_file():
            rel = candidate.relative_to(root).as_posix()
            if rel != 'manifest.json':
                actual.add(rel)
    if actual != set(names):
        raise ValueError('文件缺失或存在未登记文件')
    for item in manifest['files']:
        name = item['path']
        rel = PurePosixPath(name)
        if not name or '\\' in name or ':' in name or rel.is_absolute() or rel.as_posix() != name or any(p in ('', '.', '..') for p in name.split('/')):
            raise ValueError('不安全的文件路径')
        payload = (root / name).read_bytes()
        if len(payload) != item['bytes'] or hashlib.sha256(payload).hexdigest() != item['sha256']:
            raise ValueError('文件内容不符：' + name)
    return {'status': 'PASS', 'name': manifest['name'], 'version': manifest['version'], 'files': len(names)}


if __name__ == '__main__':
    try:
        print(json.dumps(verify(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
