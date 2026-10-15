#!/usr/bin/env python3
"""读取固定Git快照或完整本地资源；标准库、只读、不加载模型、不执行资料内命令。"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote
from urllib.request import urlopen


def digest(b):return hashlib.sha256(b).hexdigest()


def safe_path(name):
    p=PurePosixPath(name)
    if not name or '\\' in name or ':' in name or p.is_absolute() or p.as_posix()!=name or any(x in ('','.','..') for x in name.split('/')):
        raise ValueError('不安全资源路径')
    return p


def local_file(root,name):
    safe_path(name)
    root=Path(root)
    if root.is_symlink():raise ValueError('资源根目录不能是符号链接')
    p=root
    for part in name.split('/'):
        p=p/part
        if p.is_symlink():raise ValueError('资源路径不能包含符号链接')
    return p


def config(skill):
    lock=json.loads((skill/'resources.lock.json').read_text())
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',lock['repository']) or not re.fullmatch(r'[0-9a-f]{40}',lock.get('commit') or ''):
        raise ValueError('资源仓库或固定commit未就绪；不能使用浮动分支代替')
    payload=(skill/'resources/catalog.json').read_bytes()
    if digest(payload)!=lock['catalog_sha256']:raise ValueError('资源目录指纹不符')
    catalog=json.loads(payload)
    if catalog['resource_version']!=lock['resource_version']:raise ValueError('资源版本不符')
    entries={}
    for item in catalog['files']:
        safe_path(item['path'])
        if item['path'] in entries or not re.fullmatch(r'[0-9a-f]{64}',item['sha256']):raise ValueError('资源条目重复或指纹无效')
        entries[item['path']]=item
    return lock,entries


def verify_bytes(payload,item):
    if len(payload)!=item['bytes'] or digest(payload)!=item['sha256']:raise ValueError('资源内容与固定版本指纹不符：'+item['path'])
    return payload


def verify_library(skill,library):
    lock,entries=config(skill)
    raw=local_file(library,'manifest.json').read_bytes()
    if digest(raw)!=lock['manifest_sha256']:raise ValueError('本地资源manifest与锁定快照不符')
    manifest=json.loads(raw)
    if manifest['version']!=lock['resource_version']:raise ValueError('资源版本不符')
    names={x['path'] for x in manifest['files']}
    actual=set()
    for p in Path(library).rglob('*'):
        if '.git' in p.relative_to(library).parts:continue
        if p.is_symlink():raise ValueError('资源中不能包含符号链接')
        if p.is_file():actual.add(p.relative_to(library).as_posix())
    if actual!=names|{'manifest.json'}:raise ValueError('本地资源文件缺失或出现未登记文件')
    for item in manifest['files']:verify_bytes(local_file(library,item['path']).read_bytes(),item)
    for name,item in entries.items():verify_bytes(local_file(library,name).read_bytes(),item)
    return {'status':'PASS','mode':'complete','resource_commit':lock['commit'],'files':len(actual)}


def read_resource(skill,name,library=None,opener=urlopen):
    lock,entries=config(skill)
    if name not in entries:raise ValueError('路径未在固定资源目录登记')
    item=entries[name]
    if library is not None:
        raw=local_file(library,name).read_bytes()
    else:
        url='https://raw.githubusercontent.com/'+lock['repository']+'/'+lock['commit']+'/'+quote(name,safe='/')
        with opener(url,timeout=30) as response:
            raw=response.read(item['bytes']+1)
    return verify_bytes(raw,item).decode('utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('status','verify','read'))
    parser.add_argument('--library',type=Path,help='已取得的完整资源快照目录；不写入该目录')
    parser.add_argument('--path',help='catalog登记的相对文件路径')
    parser.add_argument('--start-line',type=int,default=1);parser.add_argument('--end-line',type=int)
    args=parser.parse_args();skill=Path(__file__).resolve().parents[1]
    lock,entries=config(skill)
    library=args.library or (skill/'resources/library' if (skill/'resources/library').exists() else None)
    if args.action=='verify':
        if library is None:raise ValueError('未安装本地资源；按需模式请读取目录中的固定Git条目')
        result=verify_library(skill,library)
    elif args.action=='status':
        result={'status':'READY','mode':'complete' if library else 'git','resource_commit':lock['commit'],
                'catalog_entries':len(entries),'note':'READY仅表示锁定信息可读；完整本地校验使用verify，远程条目在read时验证'}
    else:
        if not args.path:raise ValueError('read需要--path')
        text=read_resource(skill,args.path,library);lines=text.splitlines()
        end=args.end_line if args.end_line is not None else len(lines)
        if not 1<=args.start_line<=end<=len(lines):raise ValueError('读取行范围无效')
        print('\n'.join(lines[args.start_line-1:end]))
        print(json.dumps({'resource_commit':lock['commit'],'path':args.path,'sha256':entries[args.path]['sha256'],
                          'displayed_lines':[args.start_line,end],'total_lines':len(lines)},ensure_ascii=False),file=sys.stderr)
        return
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'status':'UNAVAILABLE','error':str(error)},ensure_ascii=False),file=sys.stderr);raise SystemExit(1)
