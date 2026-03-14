import logging
import sys
from importlib import metadata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "setup"))

import setup_common  # noqa: E402


def test_installed_rejects_too_low_minimum_version(monkeypatch):
    def fake_version(package_name):
        if package_name == "rich":
            return "14.3.2"
        raise metadata.PackageNotFoundError(package_name)

    monkeypatch.setattr(setup_common.importlib.metadata, "version", fake_version)

    assert setup_common.installed("rich>=9999") is False


def test_check_python_version_reports_current_supported_range(monkeypatch, caplog):
    monkeypatch.setattr(setup_common.sys, "version_info", (3, 14, 0), raising=False)
    monkeypatch.setattr(setup_common.sys, "version", "3.14.0", raising=False)

    caplog.set_level(logging.ERROR, logger="sd")

    assert setup_common.check_python_version() is False
    assert ">= 3.10.9 and < 3.14.0" in caplog.text
