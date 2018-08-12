import os
import subprocess


def call(*args, **kwargs):

    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


class GitCloneError(Exception):
    pass


class GitFetchError(Exception):
    pass


class GitResetError(Exception):
    pass


class GitSubmoduleError(Exception):
    pass


class GitAddtagError(Exception):
    pass


class GitPushtagError(Exception):
    pass


class GitBranchError(Exception):
    pass


class GitcheckoutBranchError(Exception):
    pass


class Git:
    """
    Clone project 
    Pull project
    Operate local tag and remote tag
    Checkout branch and create new branch 
    """

    def __init__(self, gitAddr):
        self.gitAddr = gitAddr

    def getMetaName(self):
        return self.gitAddr.split("/")[-1].split(".")[0]

    def getMetaPath(self):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        return baseDir + "/" + self.getMetaName()

    def clone(self):
        metaName = self.getMetaName()
        if os.path.exists(metaName):
            os.chdir(metaName)
            self.pull("master")
        cmd = "git clone --recursive " + self.gitAddr
        code, stdout, stderr = call(cmd, shell=True, cwd=os.getcwd())
        if code != 0:
            raise GitCloneError(str(stderr))
        return True

    def pull(self, branch):
        metaPath = self.getMetaPath()

        cmd = "git fetch origin"
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitFetchError(str(stderr))
        cmd = "git reset --hard origin/" + branch
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitResetError(str(stderr))
        cmd = "git submodule update --init --recursive"
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitSubmoduleError(str(stderr))
        return True

    def addTag(self, tag):
        metaPath = self.getMetaPath()

        cmd = "git tag " + tag
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitAddtagError(str(stderr))
        return True

    def pushTag(self, tag):
        metaPath = self.getMetaPath()

        cmd = "git push " + self.gitAddr + " " + tag
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitPushtagError(str(stderr))
        return True

    def getBranches(self):
        metaPath = self.getMetaPath()
        branches = []

        cmd = "git branch"
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitBranchError(str(stderr))
        ret = stdout.split('\n')[0:-1]
        for b in ret:
            if b.startswith("* "):
                branches.append(b.split('* ')[1])
            else:
                branches.append(b.strip())
        return branches

    def checkoutBranch(self, branch):
        metaPath = self.getMetaPath()
        branches = self.getBranches()

        if branch in branches:
            cmd = "git checkout " + branch
        else:
            cmd = "git checkout -b " + branch
        code, stdout, stderr = call(cmd, shell=True, cwd=os.chdir(metaPath))
        if code != 0:
            raise GitcheckoutBranchError(str(stderr))
        return True
