from pathlib import Path
import shutil
import subprocess
import sys
from types import SimpleNamespace

import click
import pytest

from akari import updater


@pytest.fixture
def repo(tmp_path, monkeypatch):
    git = shutil.which("git")
    if not git:
        pytest.skip("Git no disponible")
    def run(path, *args):
        return subprocess.run([git, *args], cwd=path, check=True, capture_output=True, text=True).stdout.strip()
    remote = tmp_path / "remote.git"
    source = tmp_path / "source"
    local = tmp_path / "installed"
    run(tmp_path, "init", "--bare", str(remote))
    run(tmp_path, "init", "-b", "main", str(source))
    run(source, "config", "user.name", "Test")
    run(source, "config", "user.email", "test@example.com")
    (source / "setup.py").write_text("initial", encoding="utf-8")
    run(source, "add", ".")
    run(source, "commit", "-m", "initial")
    run(source, "remote", "add", "origin", str(remote))
    run(source, "push", "origin", "main")
    run(tmp_path, "clone", "-b", "main", str(remote), str(local))
    monkeypatch.setattr(updater, "__file__", str(local / "akari" / "updater.py"))
    return local, source, run


def intercept_pip(monkeypatch, code=0):
    original = subprocess.run
    calls = []
    def run(cmd, **kwargs):
        if cmd[:3] == [sys.executable, "-m", "pip"]:
            calls.append((cmd, kwargs))
            return SimpleNamespace(returncode=code)
        return original(cmd, **kwargs)
    monkeypatch.setattr(updater.subprocess, "run", run)
    return calls


def advance(source, run):
    (source / "setup.py").write_text("updated", encoding="utf-8")
    run(source, "add", ".")
    run(source, "commit", "-m", "update")
    run(source, "push", "origin", "main")


def test_updates_installed_repo_from_another_directory(repo, monkeypatch, tmp_path):
    local, source, run = repo
    advance(source, run)
    calls = intercept_pip(monkeypatch)
    monkeypatch.chdir(tmp_path)
    updater.actualizar()
    assert (local / "setup.py").read_text() == "updated"
    assert run(local, "rev-parse", "HEAD") == run(source, "rev-parse", "HEAD")
    assert run(local, "branch", "--show-current") == "main"
    assert calls[0][0] == [sys.executable, "-m", "pip", "install", "--upgrade", "-e", str(local)]
    assert calls[0][1]["cwd"] == local


def test_retries_pip_when_repo_already_current(repo, monkeypatch):
    local, source, run = repo
    calls = intercept_pip(monkeypatch, code=1)
    with pytest.raises(click.ClickException, match="pip falló"):
        updater.actualizar()
    calls = intercept_pip(monkeypatch)
    updater.actualizar()
    assert len(calls) == 1


@pytest.mark.parametrize("state", ["dirty", "staged", "branch", "detached", "ahead", "diverged"])
def test_preserves_local_work(repo, monkeypatch, state):
    local, source, run = repo
    if state in {"dirty", "staged", "ahead", "diverged"}:
        (local / "setup.py").write_text("my work", encoding="utf-8")
    if state in {"staged", "ahead", "diverged"}:
        run(local, "add", ".")
    if state in {"ahead", "diverged"}:
        run(local, "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "local")
    if state == "diverged":
        advance(source, run)
    if state == "branch":
        run(local, "checkout", "-b", "custom")
    if state == "detached":
        run(local, "checkout", "--detach")
    before = run(local, "rev-parse", "HEAD")
    content = (local / "setup.py").read_text()
    calls = intercept_pip(monkeypatch)
    with pytest.raises(click.ClickException):
        updater.actualizar()
    assert run(local, "rev-parse", "HEAD") == before
    assert (local / "setup.py").read_text() == content
    assert not calls


def test_untracked_conflict_is_preserved(repo, monkeypatch):
    local, source, run = repo
    (local / "new.txt").write_text("local", encoding="utf-8")
    (source / "new.txt").write_text("remote", encoding="utf-8")
    advance(source, run)
    before = run(local, "rev-parse", "HEAD")
    calls = intercept_pip(monkeypatch)
    with pytest.raises(click.ClickException):
        updater.actualizar()
    assert (local / "new.txt").read_text() == "local"
    assert run(local, "rev-parse", "HEAD") == before
    assert not calls


def test_non_editable_install_has_actionable_error(tmp_path, monkeypatch):
    monkeypatch.setattr(updater, "__file__", str(tmp_path / "akari" / "updater.py"))
    with pytest.raises(click.ClickException, match="git clone"):
        updater.actualizar()
