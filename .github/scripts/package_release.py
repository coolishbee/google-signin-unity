import argparse
import json
import os
from pathlib import Path
import re
import subprocess

PACKAGE = Path('Packages/com.coolishbee.google-signin')
VERSION = re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?')


def valid_version(value):
    if not isinstance(value, str) or not VERSION.fullmatch(value):
        raise ValueError('유효한 버전 번호가 필요합니다. 빌드 메타데이터는 사용하지 않습니다.')
    return value


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def validate():
    manifest = json.loads((PACKAGE / 'package.json').read_text())
    assert manifest['name'] == 'com.coolishbee.google-signin'
    valid_version(manifest['version'])
    for relative in ['README.md', 'README.md.meta', 'LICENSE', 'CHANGELOG.md']:
        assert (PACKAGE / relative).is_file(), relative
    for sample in manifest['samples']:
        assert (PACKAGE / sample['path']).is_dir(), sample['path']
    packed = json.loads(subprocess.check_output(
        ['npm', 'pack', '--dry-run', '--json', '--ignore-scripts'], cwd=PACKAGE, text=True))[0]
    names = {item['path'] for item in packed['files']}
    assert {'README.md', 'LICENSE', 'package.json', 'CHANGELOG.md'} <= names
    for prefix in ['Runtime/', 'Editor/', 'Plugins/', 'Samples~/']:
        assert any(name.startswith(prefix) for name in names), prefix
    assert not any(name.startswith(('SampleProject/', '.github/')) for name in names)
    assert packed['size'] < 512 * 1024 * 1024
    print('패키지 정보와 배포 파일 검사 완료')


def decide(retry_version=None):
    manifest = json.loads((PACKAGE / 'package.json').read_text())
    version = valid_version(retry_version or manifest['version'])
    tag = 'upm/v' + version
    exists = subprocess.run(['git', 'show-ref', '--verify', '--quiet', 'refs/tags/' + tag]).returncode == 0
    if retry_version and not exists:
        raise ValueError('재시도할 태그가 없습니다.')
    if exists:
        tagged = json.loads(git('show', f'{tag}:{PACKAGE}/package.json'))
        assert tagged['name'] == manifest['name'] and tagged['version'] == version
        subprocess.run(['git', 'merge-base', '--is-ancestor', tag, 'HEAD'], check=True)
    values = {'version': version, 'tag': tag, 'create': str(not exists).lower(),
              'publish': str(bool(retry_version) or not exists).lower()}
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
            for key, value in values.items():
                stream.write(f'{key}={value}\n')
    print(json.dumps(values))
    return values


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['validate', 'decide'])
    parser.add_argument('--retry-version', default='')
    args = parser.parse_args()
    if args.command == 'validate':
        validate()
    else:
        decide(args.retry_version)
