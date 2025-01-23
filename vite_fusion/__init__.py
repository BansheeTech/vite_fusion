"""
vite_fusion
Source by Claudio González
Copyright © 2024 Banshee Development S.L.
https://www.banshee.pro/
MIT License
"""

import os
import json
import time
from typing import Optional, Callable, Dict, Any
from flask import Flask


class ManifestCache:
    _instance = None
    prod_cache: Optional[Dict] = None
    dev_cache: Optional[Dict] = None
    last_dev_check: float = 0
    current_manifest_path: Optional[str] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManifestCache, cls).__new__(cls)
        return cls._instance

    def get_manifest(self, manifest_path: str, dev_mode: bool) -> Dict:
        if dev_mode:
            return self._get_dev_manifest(manifest_path)
        return self._get_prod_manifest(manifest_path)

    def _get_prod_manifest(self, manifest_path: str) -> Dict:
        if self.prod_cache is None or self.current_manifest_path != manifest_path:
            self.prod_cache = self._load_manifest(manifest_path)
            self.current_manifest_path = manifest_path
        return self.prod_cache

    def _get_dev_manifest(self, manifest_path: str) -> Dict:
        if time.time() - self.last_dev_check > 30 or self.current_manifest_path != manifest_path:
            self.dev_cache = self._load_manifest(manifest_path)
            self.last_dev_check = time.time()
            self.current_manifest_path = manifest_path
        return self.dev_cache

    @staticmethod
    def _load_manifest(manifest_path: str) -> Dict:
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found at {manifest_path}")

        with open(manifest_path, "r") as f:
            return json.load(f)


manifest_cache = ManifestCache()


def register_vite_assets(app: Flask, dev_mode: bool = True, dev_server_url: str = "http://localhost:5173", dist_path: str = "/src/dist", manifest_path: str = "src/dist/.vite/manifest.json", nonce_provider: Optional[Callable[[], str]] = None, logger: Optional[Any] = None) -> Flask:

    def load_manifest() -> Dict:
        try:
            return manifest_cache.get_manifest(manifest_path, dev_mode)
        except Exception as e:
            error_msg = f"Failed to load Vite manifest: {str(e)}"
            if logger:
                logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    @app.context_processor
    def inject_vite_assets() -> Dict:
        def get_nonced_attr() -> str:
            nonce = nonce_provider() if nonce_provider else None
            return f' nonce="{nonce}"' if nonce else ""

        def vitecss(entry: str) -> str:
            try:
                nonce_attr = get_nonced_attr()
                manifest = load_manifest()

                if dev_mode:
                    entry_key = next((k for k in manifest if k.endswith(f"{entry}.css")), None)
                    if entry_key:
                        return f'<link rel="stylesheet" href="{dev_server_url}/{manifest[entry_key]["src"]}"{nonce_attr} />'
                else:
                    css_entries = [f'<link rel="stylesheet" href="{dist_path}/{v["file"]}"{nonce_attr} />' for k, v in manifest.items() if k.endswith(f"{entry}.css")]
                    return "\n".join(css_entries)

                return ""
            except Exception as e:
                if logger:
                    logger.error(f"Vite CSS Error ({entry}): {str(e)}")
                return ""

        def vitejs(entry: str) -> str:
            try:
                nonce_attr = get_nonced_attr()
                manifest = load_manifest()

                if dev_mode:
                    entry_data = next((v for v in manifest.values() if v.get("name") == entry), None)
                    if entry_data:
                        return f'<script type="module" src="{dev_server_url}/{entry_data["src"]}"{nonce_attr} defer></script>'
                else:
                    entry_data = next((v for k, v in manifest.items() if k.endswith(f"{entry}.js") or k.endswith(f"{entry}.ts")), None)
                    if entry_data:
                        css_files = set(entry_data.get("css", []))
                        for import_key in entry_data.get("imports", []):
                            css_files.update(manifest.get(import_key, {}).get("css", []))

                        css_tags = "\n".join(f'<link rel="stylesheet" href="{dist_path}/{css}"{nonce_attr} />' for css in css_files)
                        return f"{css_tags}\n<script type=\"module\" src=\"{dist_path}/{entry_data['file']}\"{nonce_attr} defer></script>"

                raise RuntimeError(f"Entry '{entry}' not found in manifest")
            except Exception as e:
                if logger:
                    logger.error(f"Vite JS Error ({entry}): {str(e)}")
                return ""

        return dict(vitecss=vitecss, vitejs=vitejs)

    return app
