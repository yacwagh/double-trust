from __future__ import annotations

import ast
import logging
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union
import ast


logger = logging.getLogger(__name__)


class SystemPromptVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.prompts: List[Tuple[str, str]] = []  # (source_hint, content)
        self.env_stack: List[Dict[str, Optional[str]]] = []

    def visit_Module(self, node: ast.Module) -> None:  # type: ignore[override]
        self.env_stack.append(self._collect_assignments(node.body))
        self.generic_visit(node)
        self.env_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # type: ignore[override]
        # Parameters may shadow names; treat as unknown (None)
        fn_env = self._collect_assignments(node.body)
        for arg in node.args.args:
            fn_env[arg.arg] = None
        self.env_stack.append(fn_env)
        self.generic_visit(node)
        self.env_stack.pop()

    def visit_Assign(self, node: ast.Assign) -> None:  # type: ignore[override]
        # Keep collecting simple constant assignments as we go
        values = self._resolve_node_to_str(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._current_env()[target.id] = values
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # type: ignore[override]
        # Look for dict-like constructions: {...} or dict(role=..., content=...)
        # Also scan keyword args named 'messages=[...]' patterns if present
        # Case 1: keyword argument carries a list of dicts
        for kw in node.keywords:
            if kw.arg == "messages":
                msgs = self._collect_messages(kw.value)
                for src, content in msgs:
                    if content:
                        self.prompts.append((src, content))
        self.generic_visit(node)

    def visit_List(self, node: ast.List) -> None:  # type: ignore[override]
        # Top-level lists of messages
        msgs = self._collect_messages(node)
        for src, content in msgs:
            if content:
                self.prompts.append((src, content))
        self.generic_visit(node)

    def _collect_messages(self, node: ast.AST) -> List[Tuple[str, Optional[str]]]:
        results: List[Tuple[str, Optional[str]]] = []
        if isinstance(node, (ast.List, ast.Tuple)):
            for elt in node.elts:
                res = self._extract_role_content_from_node(elt)
                if res is not None:
                    results.append(res)
        else:
            res = self._extract_role_content_from_node(node)
            if res is not None:
                results.append(res)
        return results

    def _extract_role_content_from_node(self, node: ast.AST) -> Optional[Tuple[str, Optional[str]]]:
        # Expect a dict with keys 'role' and 'content'
        if isinstance(node, ast.Dict):
            keys = [self._resolve_node_to_str(k) for k in node.keys]
            vals = node.values
            items: Dict[str, Optional[str]] = {}
            for k_node, v_node, k in zip(node.keys, vals, keys):
                if k is None:
                    continue
                items[k] = self._resolve_node_to_str(v_node)
            role = items.get("role")
            content = items.get("content")
            if role == "system":
                # content can be None if unresolved
                return ("dict", content)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
            items: Dict[str, Optional[str]] = {}
            for kw in node.keywords:
                if kw.arg:
                    items[kw.arg] = self._resolve_node_to_str(kw.value)
            role = items.get("role")
            content = items.get("content")
            if role == "system":
                return ("dict_call", content)
        return None

    def _collect_assignments(self, body: List[ast.stmt]) -> Dict[str, Optional[str]]:
        env: Dict[str, Optional[str]] = {}
        for stmt in body:
            if isinstance(stmt, ast.Assign):
                value = self._resolve_node_to_str(stmt.value)
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        env[target.id] = value
            elif isinstance(stmt, ast.AnnAssign):
                value = self._resolve_node_to_str(stmt.value) if stmt.value is not None else None
                target = stmt.target
                if isinstance(target, ast.Name):
                    env[target.id] = value
        return env

    def _resolve_node_to_str(self, node: Optional[ast.AST]) -> Optional[str]:
        if node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.JoinedStr):  # f-string: take literal chunks, placeholders as {...}
            parts: List[str] = []
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    parts.append(v.value)
                elif isinstance(v, ast.FormattedValue):
                    parts.append("{...}")
            res = "".join(parts).strip()
            return res if res else None
        if isinstance(node, ast.Name):
            return self._lookup_name(node.id)
        if isinstance(node, ast.Call):
            # Handle simple method calls on literals like "...".strip()
            if isinstance(node.func, ast.Attribute):
                base_str = self._resolve_node_to_str(node.func.value)
                if base_str is None:
                    return None
                attr = node.func.attr
                if attr == "strip" and not node.args and not node.keywords:
                    return base_str.strip()
                # Other methods (e.g., format) are not safely resolvable; return base as best-effort
                if attr == "format":
                    return base_str
            # str("...") wrapper
            if isinstance(node.func, ast.Name) and node.func.id == "str" and len(node.args) == 1:
                return self._resolve_node_to_str(node.args[0])
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._resolve_node_to_str(node.left)
            right = self._resolve_node_to_str(node.right)
            if left is None or right is None:
                return None
            return left + right
        # Other node types (calls, subscripts, attribute access) are unknown
        return None

    def _lookup_name(self, name: str) -> Optional[str]:
        for env in reversed(self.env_stack):
            if name in env:
                return env[name]
        return None

    def _current_env(self) -> Dict[str, Optional[str]]:
        if not self.env_stack:
            self.env_stack.append({})
        return self.env_stack[-1]


def _iter_code_files(root: Path) -> Iterable[Path]:
    exts = {".py"}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in exts:
            yield path


def extract_system_prompts(directory: str) -> List[Tuple[str, str]]:
    logger.info("Scanning for system prompts in: %s", directory)
    results: List[Tuple[str, str]] = []
    for file_path in _iter_code_files(Path(directory)):
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        try:
            tree = ast.parse(text)
        except Exception:
            logger.debug("Skipping unparsable file: %s", file_path)
            continue
        visitor = SystemPromptVisitor()
        visitor.visit(tree)
        for _, content in visitor.prompts:
            if content is not None and content.strip():
                results.append((str(file_path), content))
            else:
                # keep empty/unknown to signal variable-dependent prompts
                results.append((str(file_path), ""))
        if visitor.prompts:
            logger.debug("%s: found %d system prompt candidates", file_path, len(visitor.prompts))
    logger.info("System prompt scan complete. %d prompts found", len(results))
    return results


class LangChainAgentVisitor(ast.NodeVisitor):
    """Detect LangChain create_react_agent calls and extract inline/assigned params."""
    def __init__(self) -> None:
        self.imported_create_react_agent_names: set[str] = set()
        self.assign_env: Dict[str, ast.AST] = {}
        self.found: List[Dict[str, Optional[str]]] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # type: ignore[override]
        if node.module and node.module.startswith("langchain.agents"):
            for alias in node.names:
                if alias.name == "create_react_agent":
                    self.imported_create_react_agent_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:  # type: ignore[override]
        # Keep raw AST for later resolution
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assign_env[target.id] = node.value
        self.generic_visit(node)

    def _resolve_str(self, node: Optional[ast.AST]) -> Optional[str]:
        if node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name) and node.id in self.assign_env:
            return self._resolve_str(self.assign_env[node.id])
        if isinstance(node, ast.JoinedStr):
            parts: List[str] = []
            for v in node.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    parts.append(v.value)
                else:
                    parts.append("{...}")
            res = "".join(parts).strip()
            return res if res else None
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = self._resolve_str(node.left)
            right = self._resolve_str(node.right)
            if left and right:
                return left + right
        return None

    def _resolve_tools(self, node: Optional[ast.AST]) -> List[str]:
        names: List[str] = []
        if node is None:
            return names
        if isinstance(node, ast.List):
            for elt in node.elts:
                if isinstance(elt, ast.Name):
                    names.append(elt.id)
                elif isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    names.append(str(elt.value))
        elif isinstance(node, ast.Name):
            # try to look up assigned value
            assigned = self.assign_env.get(node.id)
            if assigned is not None:
                names.extend(self._resolve_tools(assigned))
        return names

    def visit_Call(self, node: ast.Call) -> None:  # type: ignore[override]
        # match create_react_agent(...)
        name = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name and name in self.imported_create_react_agent_names:
            # extract keywords: prompt, tools (common usage)
            data: Dict[str, Optional[str] | List[str]] = {"framework": "Langchain", "prompt": None, "tools": []}
            for kw in node.keywords:
                if kw.arg == "prompt":
                    data["prompt"] = self._resolve_str(kw.value)
                if kw.arg == "tools":
                    data["tools"] = self._resolve_tools(kw.value)
            self.found.append(data)
        self.generic_visit(node)


def extract_langchain_agents(directory: str) -> List[Tuple[str, Dict[str, Optional[str]]]]:
    """Scan directory to find LangChain create_react_agent calls and extract prompt."""
    results: List[Tuple[str, Dict[str, Optional[str]]]] = []
    for file_path in _iter_code_files(Path(directory)):
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(text)
        except Exception:
            continue
        visitor = LangChainAgentVisitor()
        visitor.visit(tree)
        for item in visitor.found:
            results.append((str(file_path), item))
    return results

 