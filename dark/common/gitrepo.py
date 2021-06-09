class GitRepo:
    url: str
    commit: str
    local_directory: str

    def __init__(self, url, commit, local_directory):
        self.url = url
        self.commit = commit
        self.local_directory = local_directory

    def __repr__(self):
        return f'GitRepo(url={self.url},commit={self.commit},local_directory={self.local_directory})'
