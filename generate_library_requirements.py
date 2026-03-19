import ast
import json
import re
import sys
from pathlib import Path

try:
    from importlib import metadata as importlib_metadata  # py3.8+
except ImportError:  # pragma: no cover
    import importlib_metadata  # type: ignore


ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "library requirement.txt"


LOCAL_ROOT_MODULES = {
    # Imported like `from utils...` and `from tab_components...` in app code.
    "utils",
    "tab_components",
    # This helper script imports it only for version resolution; not part of app requirements.
    "importlib_metadata",
}


def _is_stdlib_module(mod_root: str) -> bool:
    mod_root = mod_root.strip()
    if not mod_root:
        return True
    if mod_root in sys.builtin_module_names:
        return True

    stdlib_names = getattr(sys, "stdlib_module_names", None)
    if stdlib_names is not None:
        return mod_root in stdlib_names
    # Conservative fallback: do not filter out stdlib if we can't determine it reliably.
    return False


def _extract_import_roots_from_ast(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mod = alias.name.split(".", 1)[0].strip()
                if mod:
                    roots.add(mod)
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue  # relative import like `from .x import y`
            mod = node.module.split(".", 1)[0].strip()
            if mod:
                roots.add(mod)
    return roots


def _collect_import_roots_from_py(py_path: Path) -> set[str]:
    try:
        text = py_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = py_path.read_text(encoding="latin-1")

    tree = ast.parse(text)
    return _extract_import_roots_from_ast(tree)


def _collect_import_roots_from_ipynb(nb_path: Path) -> set[str]:
    roots: set[str] = set()
    raw = nb_path.read_text(encoding="utf-8")
    nb = json.loads(raw)

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        if isinstance(source, list):
            code_text = "".join(source)
        else:
            code_text = str(source)

        # Notebook code blocks can include magics/shell commands; extract line-based import statements.
        for line in code_text.splitlines():
            stripped = line.strip()
            if not (stripped.startswith("import ") or stripped.startswith("from ")):
                continue
            # Try parsing the line as Python; if it fails, skip.
            try:
                tree = ast.parse(line)
            except SyntaxError:
                continue
            roots |= _extract_import_roots_from_ast(tree)

    return roots


def _build_top_level_to_distribution_map():
    top_level_to_dist: dict[str, str] = {}
    dist_name_to_version: dict[str, str] = {}

    for dist in importlib_metadata.distributions():
        dist_name = dist.metadata.get("Name") or dist.metadata.get("Summary") or dist.name
        if not dist_name:
            continue
        dist_key = dist_name.lower()
        try:
            dist_name_to_version[dist_key] = dist.version
        except Exception:
            continue

        # Many distributions include `top_level.txt` in their metadata.
        try:
            top_level_text = dist.read_text("top_level.txt")
        except Exception:
            top_level_text = None
        if not top_level_text:
            continue

        for mod in top_level_text.splitlines():
            mod = mod.strip()
            if not mod:
                continue
            top_level_to_dist.setdefault(mod.lower(), dist_name)

    return top_level_to_dist, dist_name_to_version


def main() -> None:
    imported_module_roots: set[str] = set()

    for py_path in ROOT.rglob("*.py"):
        # Skip pycache etc.
        if "__pycache__" in py_path.parts:
            continue
        # Don't treat the helper script's own imports as app dependencies.
        if py_path.name == "generate_library_requirements.py":
            continue
        imported_module_roots |= _collect_import_roots_from_py(py_path)

    for nb_path in ROOT.rglob("*.ipynb"):
        imported_module_roots |= _collect_import_roots_from_ipynb(nb_path)

    # Filter out local modules and stdlib.
    filtered = {
        r
        for r in imported_module_roots
        if r not in LOCAL_ROOT_MODULES and not _is_stdlib_module(r)
    }

    top_level_to_dist, dist_name_to_version = _build_top_level_to_distribution_map()

    requirements: list[str] = []
    missing: set[str] = set()

    for mod_root in sorted(filtered, key=str.lower):
        dist_name = top_level_to_dist.get(mod_root.lower())
        if dist_name is None:
            # Fallback: many packages share the same distribution name as the top-level module.
            try:
                version = importlib_metadata.version(mod_root)
                requirements.append(f"{mod_root}=={version}")
                continue
            except Exception:
                missing.add(mod_root)
                continue

        dist_key = dist_name.lower()
        version = dist_name_to_version.get(dist_key)
        if not version:
            # Fallback: resolve distribution version by name.
            try:
                version = importlib_metadata.version(dist_name)
            except Exception:
                missing.add(mod_root)
                continue

        requirements.append(f"{dist_name}=={version}")

    OUTPUT_FILE.write_text("\n".join(requirements) + "\n", encoding="utf-8")

    if missing:
        # Non-fatal: print to stderr so the file is still produced.
        print(f"Warning: Could not map these imported modules to distributions: {sorted(missing)}", file=sys.stderr)

    print(f"Wrote {len(requirements)} pinned dependencies to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

