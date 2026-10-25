"""Light and dark themes. Kept in Python (not a .qss file) so PyInstaller bundles them."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


@dataclass(frozen=True)
class Colors:
    background: str
    panel: str
    sunken: str
    border: str
    grid: str
    text: str
    muted: str
    accent: str
    on_accent: str
    match: str
    """Pixels matching the bobber colour in the preview."""
    warn: str
    danger: str
    success: str


DARK = Colors(
    background="#16171a",
    panel="#1e2024",
    sunken="#121316",
    border="#2d3036",
    grid="#26292e",
    text="#e4e6e9",
    muted="#8a9099",
    accent="#4f8cff",
    on_accent="#ffffff",
    match="#ff4fd8",
    warn="#f2a33a",
    danger="#e5484d",
    success="#3dd68c",
)

LIGHT = Colors(
    background="#f4f5f7",
    panel="#ffffff",
    sunken="#eef0f3",
    border="#dcdfe4",
    grid="#e6e8ec",
    text="#1c1f24",
    muted="#6b7280",
    accent="#2563eb",
    on_accent="#ffffff",
    match="#d61fb4",
    warn="#c2780a",
    danger="#d93036",
    success="#1a9e5c",
)

_current = DARK


def colors() -> Colors:
    """The colours of the active theme (for custom-painted widgets)."""
    return _current


def system_prefers_dark() -> bool:
    return QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark


def stylesheet(c: Colors) -> str:
    return f"""
QMainWindow {{ background: {c.background}; }}
QWidget {{ color: {c.text}; font-family: "Segoe UI", sans-serif; font-size: 9pt; }}
QToolTip {{ background: {c.panel}; color: {c.text}; border: 1px solid {c.border}; padding: 4px; }}

QGroupBox {{
    background: {c.panel}; border: 1px solid {c.border}; border-radius: 8px;
    margin-top: 20px; padding: 8px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 2px; top: 0; color: {c.muted}; }}

QLabel#titleLabel {{ font-size: 11pt; font-weight: 600; }}
QLabel#previewInfoLabel, QLabel[caption="true"] {{ color: {c.muted}; font-size: 8pt; }}
QLabel#stateLabel {{
    border: 1px solid {c.border}; border-radius: 9px; padding: 1px 9px;
    font-size: 8pt; font-weight: 600; color: {c.muted};
}}
QLabel#stateLabel[state="fishing"] {{ border-color: {c.success}; color: {c.success}; }}
QLabel#stateLabel[state="stopping"] {{ border-color: {c.warn}; color: {c.warn}; }}
QLabel[statValue="true"] {{ font-size: 13pt; font-weight: 600; }}

QLineEdit, QPlainTextEdit {{
    background: {c.sunken}; border: 1px solid {c.border}; border-radius: 5px; padding: 3px 6px;
    selection-background-color: {c.accent}; selection-color: {c.on_accent};
}}
QLineEdit:focus {{ border-color: {c.accent}; }}
QPlainTextEdit#logView {{
    font-family: "Cascadia Mono", "Consolas", monospace; font-size: 8pt; color: {c.muted};
}}

QPushButton {{
    background: {c.panel}; border: 1px solid {c.border}; border-radius: 5px; padding: 5px 12px;
}}
QPushButton:hover {{ border-color: {c.accent}; }}
QPushButton:pressed {{ background: {c.sunken}; }}
QPushButton:disabled {{ color: {c.muted}; }}
QPushButton[flat="true"] {{ border: none; background: transparent; color: {c.muted}; }}
QPushButton[flat="true"]:hover {{ color: {c.text}; background: {c.grid}; }}
QPushButton#startButton, QPushButton#compactStartButton {{
    background: {c.accent}; color: {c.on_accent}; border: none; min-height: 30px;
    font-size: 10pt; font-weight: 600;
}}
QPushButton#startButton[fishing="true"], QPushButton#compactStartButton[fishing="true"] {{
    background: {c.danger};
}}
QPushButton#startButton:disabled, QPushButton#compactStartButton:disabled {{
    background: {c.grid}; color: {c.muted};
}}

QLabel#bobberColorLabel {{ border: 1px solid {c.border}; border-radius: 4px; }}
QStatusBar {{ background: {c.background}; color: {c.muted}; }}
QScrollBar:vertical {{ background: transparent; width: 8px; }}
QScrollBar::handle:vertical {{ background: {c.border}; border-radius: 4px; min-height: 24px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
"""


def apply(app: QApplication, *, dark: bool) -> None:
    """Fusion with a matching palette (covers widgets the stylesheet skips) plus the stylesheet."""
    global _current
    c = _current = DARK if dark else LIGHT
    app.setStyle("Fusion")
    palette = QPalette()
    for role, color in (
        (QPalette.ColorRole.Window, c.background),
        (QPalette.ColorRole.WindowText, c.text),
        (QPalette.ColorRole.Base, c.sunken),
        (QPalette.ColorRole.AlternateBase, c.panel),
        (QPalette.ColorRole.Text, c.text),
        (QPalette.ColorRole.Button, c.panel),
        (QPalette.ColorRole.ButtonText, c.text),
        (QPalette.ColorRole.Highlight, c.accent),
        (QPalette.ColorRole.HighlightedText, c.on_accent),
        (QPalette.ColorRole.ToolTipBase, c.panel),
        (QPalette.ColorRole.ToolTipText, c.text),
        (QPalette.ColorRole.PlaceholderText, c.muted),
    ):
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
    app.setStyleSheet(stylesheet(c))
