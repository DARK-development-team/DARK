from subprocess import Popen, PIPE


def is_repository(url):
    lsremote = Popen(['git', 'ls-remote', '--quiet', url], stdout=PIPE)
    output, _ = lsremote.communicate()
    rc = lsremote.returncode
    if rc != 0:
        return False
    else:
        return True


def list_remote_hash_refs(url):
    lsremote = Popen(['git', 'ls-remote', '--quiet', url], stdout=PIPE)
    output, _ = lsremote.communicate()
    rc = lsremote.returncode
    if rc != 0:
        return None
    else:
        commits = output.split('\n')
        hash_ref_pairs = [(hsh, ref) for entry in commits for hsh, ref in entry.split('\t')]
        return hash_ref_pairs