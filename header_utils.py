#!/usr/bin/env python3
"""header_utils.py

Provides `HeaderProcessor`, a utility class to recursively process header
declarations for [binder](https://github.com/RosettaCommons/binder).

see repo: <https://github.com/shakfu/header_utils>

Default header transformations:
    -> change_quotes_to_pointy_brackets
    -> change_relative_to_absolute_header_references

Optional header transformations
    -> change_pragma_one_to_header_guards

Additional Features:
    - generate graph of header references in [png|svg|pdf|dot] format

"""
import argparse
import os
import re
import shutil
import time
from typing import ClassVar


try:
    import graphviz  # type: ignore

    HAVE_GRAPHVIZ = True
except ImportError:
    HAVE_GRAPHVIZ = False


class HeaderProcessor:
    """Recursively processes header declarations for binder

    This is done via a pipeline of transformers:
        -> change_quotes_to_pointy_brackets
        -> change_relative_to_absolute_header_references

        (optional transformers)
        -> change_pragma_one_to_header_guards

        (optional analysis)
        - generate graph of header references in [png|svg|pdf|dot] format

    see repo: <https://github.com/shakfu/header_utils>
    """

    PATTERN: ClassVar = re.compile(r"^#include \"(.+)\"")
    DEFAULT_HEADER_ENDINGS: ClassVar[list[str]] = [".h", ".hpp", ".hh"]

    def __init__(
        self,
        path: str,
        output_dir: str = None,  # type: ignore
        header_endings: list[str] = None,  # type: ignore
        header_guards: bool = False,
        dry_run: bool = False,
        skip_backup: bool = False,
    ):
        self.path = path
        self.output_dir = output_dir
        self.using_output_dir = True if output_dir else False
        self.header_endings = (
            header_endings if header_endings else self.DEFAULT_HEADER_ENDINGS
        )
        self.header_guards = header_guards
        self.dry_run = dry_run
        self.skip_backup = skip_backup
        if HAVE_GRAPHVIZ:
            self.graph = graphviz.Digraph("dependencies", comment="Header References")
        else:
            self.graph = None

    def get_headers(self, sort: bool = False, from_output_dir: bool = False) -> list[str]:
        """recursively get all header files

        Can be sorted optionally and retrieved from output_dir
        """
        if from_output_dir:
            path = self.output_dir
        else:
            path = self.path
        results = []
        for root, _, files in os.walk(path):
            for fname in files:
                if any(fname.endswith(e) for e in self.header_endings):
                    results.append(os.path.join(root, fname))
        if sort:
            return sorted(results)
        return results

    def get_include_statements(self, sort: bool = False, from_output_dir: bool = False) -> list[str]:
        """recursively get all include statements"""
        _results = []
        for header in self.get_headers(sort, from_output_dir):
            with open(header, encoding="utf-8") as fopen:
                lines = fopen.readlines()
                for line in lines:
                    if line.startswith("#include "):
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
                    if HAVE_GRAPHVIZ and self.graph:
                        self.graph.edge(base_path, abs_ref)
                    continue
            _result.append(line)
        return _result

    def normalize_include_statement(self, line: str, base_path: str):
        """normalize include statement

        converts:
            `"` to pointy braces
            relative to absolute paths
        """
        match = self.PATTERN.match(line)
        if match:
            rel_ref = match.group(1)
            abs_ref = self.mk_absolute_include(base_path, rel_ref)
            return (abs_ref, f"#include <{abs_ref}>\n")
        raise ValueError

    def normalize_header_guards(self, lines: list[str], base_path: str):
        """convert '#pragma once' to guarded headers"""
        _results = []
        name = base_path.replace("/", "_").replace(".", "_").upper()
        for line in lines:
            if line.startswith("#pragma once"):
                line = line.strip()
                replacement = f"#ifndef {name}\n"
                _results.append(replacement)
                define = f"#define {name}\n"
                _results.append(define)
                print("#pragma once -> guarded headers")
                continue
            _results.append(line)
        _results.append(f"#endif // {name}\n")
        return _results

    def transform(self, lines: list[str], base_path: str):
        """main tranformation pipeline"""
        _transformers = [
            "normalize_header_include_statements",
        ]
        if self.header_guards:
            _transformers.append("normalize_header_guards")
        for transformer in _transformers:
            lines = getattr(self, transformer)(lines, base_path)
        return lines

    def get_base_path(self, header_path):
        """retrieves base path, or the path which follows `self.path`"""
        path = self.path
        if not path.endswith("/"):
            path = f"{path}/"
        return header_path[len(path) :]

    def process_headers(self):
        """process headers from path recursively"""
        if self.output_dir:
            def ignore_files(directory, files):
                return [f for f in files if os.path.isfile(os.path.join(directory, f))]
            shutil.copytree(self.path, self.output_dir, ignore=ignore_files)
        else:
            if not self.skip_backup and not self.dry_run:
                # default backup
                tstamp = time.strftime("%Y%m%d%H%M%S")
                shutil.copytree(self.path, f"{self.path}-{tstamp}")

        headers = self.get_headers()
        for header_path in headers:
            base_path = self.get_base_path(header_path)
            print(base_path)
            with open(header_path, encoding="utf-8") as fopen:
                lines = fopen.readlines()
            _result = self.transform(lines, base_path)
            if not self.dry_run:
                if self.output_dir:
                    header_path = os.path.join(self.output_dir, base_path)
                    print("header_path:", header_path)
                with open(header_path, "w", encoding="utf-8") as fwrite:
                    fwrite.writelines(_result)
            print()

    def list_target_headers(self):
        """recursively list all headers"""
        headers = self.get_headers()
        for header_path in headers:
            print(header_path)

    @classmethod
    def commandline(cls):
        """commmandline api"""
        parser = argparse.ArgumentParser(
            description=(
                "Convert headers to a binder friendly format. "
                f"(default: {cls.DEFAULT_HEADER_ENDINGS})"
            ),
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        required = option = parser.add_argument

        required("path", help="path to include directory")

        option(
            "--output-dir",
            "-o",
            help="output directory for modified headers",
        )

        option(
            "--header-endings",
            "-e",
            nargs="+",
        )

        option(
            "--header-guards",
            action="store_true",
            help="convert `#pragma once` to header guards",
        )

        option(
            "--dry-run",
            "-d",
            action="store_true",
            help="run in dry-run mode without actual changes",
        )

        option("--skip-backup", "-s", action="store_true", help="skip creating backup if output_dir is not provided")

        option("--list", "-l", action="store_true", help="list target headers only")

        option(
            "--graph",
            "-g",
            help="output path for graphviz graph with format suffix [png|pdf|svg]",
        )

        args = parser.parse_args()

        if args.path:
            app = cls(
                args.path,
                args.output_dir,
                args.header_endings,
                args.header_guards,
                args.dry_run,
                args.skip_backup,
            )
            if args.list:
                app.list_target_headers()
            else:
                app.process_headers()
                if args.graph and app.graph:
                    app.graph.render(outfile=args.graph)


if __name__ == "__main__":
    HeaderProcessor.commandline()
