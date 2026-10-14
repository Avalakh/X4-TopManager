"""Собрать полный игровой пакет без диагностического расширения."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from install_mod import installation_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    files = installation_files(include_adapted=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with ZipFile(args.output, 'w', compression=ZIP_DEFLATED) as archive:
        for relative, source in sorted(files.items()):
            data = source.read_bytes()
            name = 'tm_empire_management/' + relative.as_posix()
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
            records.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
    with ZipFile(args.output) as archive:
        if set(archive.namelist()) != {record['path'] for record in records}:
            raise ValueError('Состав архива отличается от полного игрового пакета')
        for record in records:
            if hashlib.sha256(archive.read(record['path'])).hexdigest() != record['sha256']:
                raise ValueError('SHA файла в архиве отличается: ' + record['path'])
    manifest = {'qualified_release': False, 'includes_adapted_manager': True,
                'archive_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                'files': records}
    args.output.with_suffix('.manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Пакет собран и SHA проверены: {len(records)} файлов; приёмка ещё не завершена')


if __name__ == '__main__':
    main()
