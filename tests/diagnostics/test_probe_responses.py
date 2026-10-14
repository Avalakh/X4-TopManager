"""A delayed diagnostic result cannot authorize another world operation."""
import unittest
import tempfile
from pathlib import Path

from probe import request, request_status_save


class Pipe:
    def __init__(self, response):
        self.response = response
        self.sent = []

    def send(self, frame, **kwargs):
        self.sent.append(frame)

    def recv(self, timeout):
        return self.response


class ResponseTests(unittest.TestCase):
    def test_occupied_physical_slot_never_sends_save(self):
        base = Path(__file__).resolve().parents[2] / '.cache' / 'tmp' / 'save-preflight-tests'
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as folder:
            Path(folder, 'save_011.xml.gz').write_bytes(b'incompatible save')
            pipe = Pipe('save_current_status|requested|slot=save_011|overwrite=false')
            with self.assertRaises(FileExistsError):
                request_status_save(pipe, folder)
            self.assertEqual(pipe.sent, [])

    def test_bound_save_rejects_stale_reply_without_replay(self):
        pipe = Pipe('hire_setup|state=prepared')
        with self.assertRaises(ValueError):
            request(pipe, 'save_current_status|preflight_save_011_absent')
        self.assertEqual(pipe.sent, ['save_current_status|preflight_save_011_absent'])

    def test_scan_and_result_share_one_frame(self):
        response = ('personnel_hire_scan|effects=false\n'
                    'personnel_autonomous|passed=0|effects=false')
        pipe = Pipe(response)
        self.assertEqual(request(pipe, 'personnel_autonomous_read'), response)
        self.assertEqual(pipe.sent, ['personnel_autonomous_read'])

    def test_stale_result_stops_without_replaying_command(self):
        pipe = Pipe('personnel_autonomous|passed=0|effects=false')
        with self.assertRaises(ValueError):
            request(pipe, 'hire_candidate_next')
        self.assertEqual(pipe.sent, ['hire_candidate_next'])

    def test_timeout_does_not_repeat_world_preparation(self):
        pipe = Pipe(None)
        with self.assertRaises(TimeoutError):
            request(pipe, 'hire_setup')
        self.assertEqual(pipe.sent, ['hire_setup'])


if __name__ == '__main__':
    unittest.main()
