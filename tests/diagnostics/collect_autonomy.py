"""Конечный read-only сбор игрового прогона; не квалифицирует релиз."""
import argparse
import ctypes
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def process_identity(pid):
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.GetProcessTimes.argtypes = [ctypes.c_void_p] + [ctypes.c_void_p] * 4
    kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        raise RuntimeError('Игровой процесс недоступен')
    try:
        code = ctypes.c_ulong()
        if not kernel.GetExitCodeProcess(handle, ctypes.byref(code)) or code.value != 259:
            raise RuntimeError('Игровой процесс завершён')
        stamps = [ctypes.c_ulonglong() for _ in range(4)]
        if not kernel.GetProcessTimes(handle, *(ctypes.byref(x) for x in stamps)):
            raise RuntimeError('Не получено время создания процесса')
        return stamps[0].value
    finally:
        kernel.CloseHandle(handle)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--minutes', type=int, default=120)
    parser.add_argument('--interval', type=int, default=300)
    parser.add_argument('--domains', action='store_true', help='Дополнительно читать фактические продажи, угрозу и большую собственность')
    args = parser.parse_args()
    if args.minutes < 1 or args.interval < 60 or args.output.exists():
        parser.error('Нужен новый каталог, положительная длительность и интервал≥60s')
    args.output.mkdir(parents=True)
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads((root / 'docs/installed-manifest.json').read_text(encoding='utf-8'))
    installed = Path(manifest['target'])
    frozen = {str(installed / x['path']): x['sha256'] for x in manifest['files']}
    diagnostic = installed.parent / 'tm_empire_diagnostics'
    for path in sorted(diagnostic.rglob('*')):
        if path.is_file():
            frozen[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    identity = process_identity(args.pid)
    start = time.monotonic()
    count = 0
    state = 'running'
    summary = {'pid': args.pid, 'creation_time': identity, 'qualified_release': False,
               'requested_seconds': args.minutes * 60, 'files': frozen}
    (args.output / 'baseline.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    probe = root / 'tests/diagnostics/probe.py'
    dependencies = root / '.cache/tmp/station-boundary-20261011/python-deps'
    runner = ('import site,sys,runpy; site.addsitedir(' + repr(str(dependencies)) +
              '); sys.path.insert(0,' + repr(str(probe.parent)) +
              '); runpy.run_path(' + repr(str(probe)) + ',run_name="__main__")')
    try:
        while True:
            if (args.output / 'stop.request').exists():
                state = 'stopped_by_request'
                break
            if process_identity(args.pid) != identity:
                raise RuntimeError('Процесс игры изменился')
            if any(hashlib.sha256(Path(p).read_bytes()).hexdigest() != h for p, h in frozen.items()):
                raise RuntimeError('Установленный пакет изменился')
            for mode in (('role', 'provision', 'domain') if args.domains else ('role', 'provision')):
                output = args.output / f'{count:03d}-{mode}.json'
                result = subprocess.run([sys.executable, '-c', runner, mode, '--output', str(output)],
                                        cwd=root.parent, capture_output=True, timeout=90)
                (args.output / f'{count:03d}-{mode}-console.txt').write_bytes(result.stdout + result.stderr)
                if result.returncode:
                    raise RuntimeError(f'Проба {mode} завершилась с ошибкой; не повторяется')
            count += 1
            elapsed = time.monotonic() - start
            (args.output / 'progress.json').write_text(json.dumps({'samples': count, 'elapsed_seconds': elapsed}), encoding='utf-8')
            if elapsed >= args.minutes * 60:
                state = 'collection_finished'
                break
            next_sample = min(start + count * args.interval, start + args.minutes * 60)
            while time.monotonic() < next_sample and not (args.output / 'stop.request').exists():
                time.sleep(max(0, min(2, next_sample - time.monotonic())))
    except Exception as error:
        state = 'collection_error'
        summary['error'] = str(error)
        raise
    finally:
        summary.update(state=state, samples=count, elapsed_seconds=time.monotonic() - start)
        (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
