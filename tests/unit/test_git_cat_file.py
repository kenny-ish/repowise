from __future__ import annotations

import subprocess
from types import SimpleNamespace

from repowise.core.analysis.git_cat_file import cat_file_batch


def test_submodule_probe_does_not_inherit_stdin(tmp_path, monkeypatch) -> None:
    seen: list[dict[str, object]] = []

    def _fake_run(cmd, **kwargs):
        seen.append(kwargs)
        if cmd[1:3] == ["cat-file", "--batch"]:
            return SimpleNamespace(returncode=0, stdout=b"HEAD:submodule missing\n", stderr=b"")
        return SimpleNamespace(
            returncode=0, stdout="160000 commit deadbeef\tsubmodule\n", stderr=""
        )

    import repowise.core.analysis.git_cat_file as git_cat_file_mod

    monkeypatch.setattr(git_cat_file_mod.subprocess, "run", _fake_run)

    assert cat_file_batch(str(tmp_path), ["HEAD:submodule"], on_missing="raise") == [
        ("HEAD:submodule", None)
    ]
    assert seen[1]["stdin"] is subprocess.DEVNULL
