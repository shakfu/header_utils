#!/usr/bin/env python3

# normalize_header.py
"""
Provide a class to recursively process header declarations for binder

see repo: <https://github.com/shakfu/norm_headers>

"""
import argparse
import os
import re
import shutil


try:
    import graphviz
    HAVE_GRAPHVIZ = True
except ImportError:
    HAVE_GRAPHVIZ = False


class HeaderProcessor:
    """Recursively processes header declarations for binder

    This is done via a pipeline of transformers:
        - change_quotes_to_pointy_brackets
        - change_pragma_one_to_header_guards
        - change_relative_to_absolute_header_references

    Also provides optional analyzers:
        - generate graph of header references in dot format

    see repo: <https://github.com/shakfu/norm_headers>
    """

    PATTERN = re.compile(r"^#include \"(.+)\"")

    def __init__(self, path: str, dry_run: bool = False, backup: bool = False):
        self.path = path
        self.dry_run = dry_run
        self.backup = backup
        if HAVE_GRAPHVIZ:
            self.graph = graphviz.Digraph('dependencies', comment="Header References")

    def get_headers(self, sort: bool = False) -> list[str]:
        """recursively get all header files 

        Can be sorted optionally.
        """
        endings = [".h", ".hpp"]
        results = []
        for root, _, files in os.walk(self.path):
            for fname in files:
                if any(fname.endswith(e) for e in endings):
                    results.append(os.path.join(root, fname))
        if sort:
            return sorted(results)
        return results

    def get_include_statements(self) -> list[str]:
        """recursively get all include statements"""
        _results = []
        for header in self.get_headers():
            with open(header, encoding="utf-8") as fopen:
                lines = fopen.readlines()
                for line in lines:
                    if line.startswith('#include '):
                        _results.append(line.strip())
        return _results

    def mk_absolute_include(self, base_path: str, relative_path: str):
        """converts relative path to absolute path"""
        base_parts = base_path.split("/")
        relative_parts = relative_path.split("/")
        base_parts.pop()
        for part in relative_parts:
            if part == ".":
                continue
            if part == "..":
                base_parts.pop()
            else:
                base_parts.append(part)
        return "/".join(base_parts)

    def add_reference(self, base_path: str, abs_ref: str):
        """adds an edge to the internal graphviz graph"""
        self.graph.edge(base_path, abs_ref)

    def normalize_header_include_statements(self, lines: list[str], base_path: str):
        """convert quotes to pointy brackets in an an include statement"""
        _shorten = lambda s: s.lstrip("#include ")
        _result = []
        for line in lines:
            if line.startswith("#include "):
                if line.endswith('"\n'):
                    line = line.strip()
                    abs_ref, abs_include = self.normalize_include_statement(
                        line, base_path
                    )
                    _result.append(abs_include)
                    print("  ", _shorten(line), "->", _shorten(abs_include.strip()))
                    if HAVE_GRAPHVIZ:
                        self.add_reference(base_path, abs_ref)
                    continue
            _result.append(line)
        return _result

    def normalize_include_statement(self, line: str, base_path: str):
        """normalize include statement

        converts:
            "` to point braces
            relative to absolute paths
        """
        match = self.PATTERN.match(line)
        if match:
            rel_ref = match.group(1)
            abs_ref = self.mk_absolute_include(base_path, rel_ref)
            return (abs_ref, f"#include <{abs_ref}>\n")
        raise ValueError

    def normalize_header_guards(self, lines: list[str], base_path: str):
        """convert pragma once to guarded headers"""
        _results = []
        name = (
            base_path.replace("/", "_").replace(".", "_").upper()
        )
        for line in lines:
            if line.startswith("#pragma once"):
                line = line.strip()
                replacement = f"#ifndef {name}\n"
                _results.append(replacement)
                define = f"#define {name}\n"
                _results.append(define)
                # print(replacement, define)
                print('#pragma once -> guarded headers')
                continue
            _results.append(line)
        _results.append(f"#endif // {name}\n")
        return _results

    def transform(self, lines: list[str], base_path: str):
        """main tranformation pipeline"""
        _transformers = [
            "normalize_header_include_statements",
            "normalize_header_guards",
        ]
        for transformer in _transformers:
            lines = getattr(self, transformer)(lines, base_path)
        return lines

    def get_base_path(self, header_path):
        """retrieves base path, or the path which follows `self.path`"""
        path = self.path
        if not path.endswith('/'):
            path = f"{path}/"
        return header_path[len(path):]

    def process_headers(self):
        """process headers from path recursively"""
        if self.backup:
            shutil.copytree(self.path, f"{self.path}__BACKUP")
        headers = self.get_headers(self.path)
        for header_path in headers:
            base_path = self.get_base_path(header_path)
            print(base_path)            
            with open(header_path, encoding="utf-8") as fopen:
                lines = fopen.readlines()
            _result = self.transform(lines, base_path)
            if not self.dry_run:
                with open(header_path, "w", encoding="utf-8") as fwrite:
                    fwrite.writelines(_result)
            print()

    def list_target_headers(self):
        """recursively list all headers"""
        headers = self.get_headers(self.path)
        for header_path in headers:
            print(header_path)

    @classmethod
    def commandline(cls):
        """commmandline api"""
        parser = argparse.ArgumentParser(
            description="Convert headers to a binder friendly format."
        )

        parser.add_argument("path", help="path to include directory")

        parser.add_argument(
            "--dry-run",
            "-d",
            action="store_true",
            help="run in dry-run mode without actual changes",
        )

        parser.add_argument("--backup", "-b", action="store_true", help="create backup")

        parser.add_argument(
            "--list", "-l", action="store_true", help="list target headers only"
        )

        parser.add_argument(
            "--graph", "-g", type=str, help="path to output graphviz graph [png|pdf|svg]"
        )

        args = parser.parse_args()

        if args.path:
            app = cls(args.path, args.dry_run, args.backup)
            if args.list:
                app.list_target_headers()
            else:
                app.process_headers()
                if args.graph:
                    app.graph.render(outfile=args.graph)

if __name__ == "__main__":
    HeaderProcessor.commandline()
