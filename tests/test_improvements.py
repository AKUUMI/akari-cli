import io
from types import SimpleNamespace

import pytest
from rich.console import Console
from akari import scrapers, ui, player


def test_cache_expires_and_separates_headers(monkeypatch):
    calls = []
    clock = [0]
    monkeypatch.setattr(scrapers, "_CACHE", scrapers.OrderedDict())
    monkeypatch.setattr(scrapers.time, "monotonic", lambda: clock[0])
    def get(url, **kwargs):
        calls.append(kwargs)
        return SimpleNamespace(url=url, raise_for_status=lambda: None)
    monkeypatch.setattr(scrapers.requests, "get", get)
    first = scrapers._safe_get("https://example.com")
    assert scrapers._safe_get("https://example.com") is first
    scrapers._safe_get("https://example.com", {"Referer": "https://other.test"})
    assert len(calls) == 2
    clock[0] = 61
    assert scrapers._safe_get("https://example.com") is not first
    assert len(calls) == 3


def test_failed_requests_are_not_cached(monkeypatch):
    calls = []
    monkeypatch.setattr(scrapers, "_CACHE", scrapers.OrderedDict())
    def get(url, **kwargs):
        calls.append(url)
        raise scrapers.requests.Timeout()
    monkeypatch.setattr(scrapers.requests, "get", get)
    assert scrapers._safe_get("https://example.com") is None
    assert scrapers._safe_get("https://example.com") is None
    assert len(calls) == 2


def test_paginated_selection(monkeypatch):
    rows = [{"titulo": str(i), "fuente": "Test"} for i in range(23)]
    answers = iter(["n", "n", "p", "3"])
    monkeypatch.setattr(ui, "console", Console(file=io.StringIO()))
    monkeypatch.setattr(ui.Prompt, "ask", lambda *a, **k: next(answers))
    assert ui.seleccionar_anime(rows) is rows[12]


def test_episode_cancel_and_sparse_default(monkeypatch):
    defaults = []
    monkeypatch.setattr(ui, "console", Console(file=io.StringIO()))
    def ask(*args, **kwargs):
        defaults.append(kwargs["default"])
        return "q"
    monkeypatch.setattr(ui.Prompt, "ask", ask)
    assert ui.seleccionar_episodio([4, 8], "Test", {"episodio": 2}) is None
    assert defaults == ["4"]


def test_download_fallback_and_safe_filename(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(player.shutil, "which", lambda _: "yt-dlp")
    def run(cmd):
        calls.append(cmd)
        return SimpleNamespace(returncode=1 if len(calls) == 1 else 0)
    monkeypatch.setattr(player.subprocess, "run", run)
    servers = [{"url": "https://example.com/a", "servidor": "One"},
               {"url": "https://example.com/b", "servidor": "Two"}]
    ok, path = player.descargar_episodio(servers, "../100%/Title", 1, destino=tmp_path)
    assert ok and path == tmp_path
    assert len(calls) == 2
    for cmd in calls:
        template = cmd[cmd.index("--output") + 1]
        assert "/" not in template and "100%%" in template
        assert "--continue" in cmd and cmd[-2] == "--"


def test_huge_episode_range_is_rejected():
    with pytest.raises(ValueError):
        player.parsear_episodios("1-999999999999", [1, 2, 3])
