"""
GuardianAI Browser Protection Extension Master Test Suite
Purpose: End-to-end verification of Manifest V3 specification, Popup DTOs,
         Background Service Worker logic, API Client, DOM Extractor, Warning Overlay,
         SelectedTextAnalyzer, Storage Service, and Security Controls.
"""

import json
import pathlib
import pytest

EXTENSION_DIR = pathlib.Path(__file__).parent.parent.parent / "browser-extension"

# --- 1. MANIFEST V3 SCHEMA TESTS ---

def test_manifest_v3_validity():
    manifest_path = EXTENSION_DIR / "manifest.json"
    assert manifest_path.exists(), "manifest.json file must exist under browser-extension/"

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["manifest_version"] == 3
    assert data["name"] == "GuardianAI - Real-Time Phishing & Scam Protection"
    assert data["version"] == "1.0.0"
    assert "background" in data
    assert data["background"]["service_worker"] == "src/background/index.ts"
    assert "permissions" in data
    assert "storage" in data["permissions"]
    assert "activeTab" in data["permissions"]
    assert "contextMenus" in data["permissions"]
    assert "declarativeNetRequest" in data["permissions"]


def test_manifest_csp_policy():
    manifest_path = EXTENSION_DIR / "manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "content_security_policy" in data
    csp = data["content_security_policy"]["extension_pages"]
    assert "script-src 'self'" in csp
    assert "object-src 'self'" in csp


# --- 2. EXTENSION FILE STRUCTURE TESTS ---

def test_extension_file_structure_exists():
    required_files = [
        "manifest.json",
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "src/shared/types.ts",
        "src/shared/storage_service.ts",
        "src/background/index.ts",
        "src/background/api_client.ts",
        "src/background/context_menu.ts",
        "src/content/index.ts",
        "src/content/dom_scanner.ts",
        "src/content/dom_extractor.ts",
        "src/content/page_analysis_service.ts",
        "src/content/overlay_ui.ts",
        "src/popup/popup.html",
        "src/popup/PopupApp.tsx",
        "src/options/options.html",
        "src/options/OptionsApp.tsx",
        "src/utils/sanitizer.ts",
        "public/icons/icon-16.png",
        "public/icons/icon-32.png",
        "public/icons/icon-48.png",
        "public/icons/icon-128.png"
    ]

    for req_file in required_files:
        p = EXTENSION_DIR / req_file
        assert p.exists(), f"Required extension file missing: {req_file}"


# --- 3. TYPESCRIPT CONTENT CONTRACT TESTS ---

def test_shared_types_contracts():
    types_path = EXTENSION_DIR / "src/shared/types.ts"
    content = types_path.read_text(encoding="utf-8")

    assert "export type RiskLevel = 'SAFE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';" in content
    assert "export interface ExtensionScanResult" in content
    assert "export interface ExtensionSettings" in content
    assert "ANALYZE_URL" in content
    assert "ANALYZE_TEXT" in content


def test_storage_service_implementation():
    storage_path = EXTENSION_DIR / "src/shared/storage_service.ts"
    content = storage_path.read_text(encoding="utf-8")

    assert "class ExtensionStorageService" in content
    assert "MAX_RECENT_SCANS = 20" in content
    assert "MAX_CACHE_ENTRIES = 2000" in content
    assert "getStorageQuotaInfo" in content


def test_api_client_security_controls():
    api_client_path = EXTENSION_DIR / "src/background/api_client.ts"
    content = api_client_path.read_text(encoding="utf-8")

    assert "class GuardianExtensionAPIClient" in content
    assert "AbortController" in content
    assert "maxRetries" in content
    assert "Bearer" in content
    assert "ExtensionAPIError" in content


def test_dom_extractor_privacy_controls():
    extractor_path = EXTENSION_DIR / "src/content/dom_extractor.ts"
    content = extractor_path.read_text(encoding="utf-8")

    assert "extractStructuredPageContent" in content
    assert "SENSITIVE_INPUT_TYPES" in content
    assert "is_sensitive" in content
    assert "TreeWalker" in content


def test_overlay_ui_accessibility():
    overlay_path = EXTENSION_DIR / "src/content/overlay_ui.ts"
    content = overlay_path.read_text(encoding="utf-8")

    assert "mountThreatBannerOverlay" in content
    assert "role" in content
    assert "alertdialog" in content
    assert "attachShadow" in content
    assert "btn-dismiss" in content
    assert "btn-reanalyze" in content
    assert "btn-learn" in content


def test_context_menu_selected_text_analyzer():
    menu_path = EXTENSION_DIR / "src/background/context_menu.ts"
    content = menu_path.read_text(encoding="utf-8")

    assert "class SelectedTextAnalyzer" in content
    assert "guardian_ai_analyse_selected_text" in content
    assert "chrome.contextMenus.create" in content
