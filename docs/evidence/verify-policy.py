"""Exercise the exact workflow shell checks with passing and failing inputs."""
from pathlib import Path
import subprocess
import tempfile
import yaml

root = Path(__file__).resolve().parents[2]
steps = yaml.safe_load((root / '.github/workflows/security.yml').read_text())['jobs']['security-policy']['steps']
secret_check = next(s['run'] for s in steps if s['name'] == 'Reject tracked .env')
uid_check = next(s['run'] for s in steps if s['name'] == 'Verify non-root runtime user')


def check(label, script, cwd, expected):
    result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', script], cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(label, flush=True)
    print(result.stdout.rstrip(), flush=True)
    assert (result.returncode == 0) == expected, (label, result.returncode)
    print(f'PASS: expected {"acceptance" if expected else "rejection"}; exit code {result.returncode}\n', flush=True)


check('Real repository: .env untracked', secret_check, root, True)
with tempfile.TemporaryDirectory(prefix='week9-policy-') as tmp:
    subprocess.run(['git', 'init', '-q', tmp], check=True)
    (Path(tmp) / '.env').write_text('DUMMY_TEST_VALUE=not-a-secret\n')
    subprocess.run(['git', '-C', tmp, 'add', '.env'], check=True)
    check('Isolated temporary repository: dummy .env tracked', secret_check, tmp, False)
check('Hardened image', uid_check.replace('helpdesk:security', 'helpdesk:week9-after'), root, True)
check('Baseline root image', uid_check.replace('helpdesk:security', 'helpdesk:week9-before'), root, False)
