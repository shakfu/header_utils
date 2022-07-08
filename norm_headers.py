#!/usr/bin/env python3

# normalize_header.py
"""recursively normalizes header declarations

    #include "sub/foo.h"   -> #include <sub/foo.h>

    #include "sub/foo.hpp" -> #include <sub/foo.hpp>

    #include "../foo.h" -> #include <sub/foo.h>


see repo: <https://github.com/shakfu/norm_headers>

"""
import os
import re
import argparse
import shutil


pattern = re.compile(r"^#include \"(.+)\"")


def shorten(statement):
    """shorten include statement for logging"""
    return statement.lstrip("#include ")


def get_headers(top, sort=False):
    """get all header files recursively

    Can be sorted optionally.
    """
    endings = [".h", ".hpp"]
    results = []
    for root, _, files in os.walk(top):
        for fname in files:
            if any(fname.endswith(e) for e in endings):
                results.append(os.path.join(root, fname))
    if sort:
        return sorted(results)
    return results


def absolute(base, relative):
    """converts relative path to absolute path"""
    base_parts = base.split("/")
    relative_parts = relative.split("/")
    base_parts.pop()
    for elem in relative_parts:
        if elem == ".":
            continue
        if elem == "..":
            base_parts.pop()
        else:
            base_parts.append(elem)
    return "/".join(base_parts)


def normalize_include_statement(line, include):
    """normalize include statement

    converts:
        "` to point braces
        relative to absolute paths
    """
    headerpath = include.lstrip("include/")
    match = pattern.match(line)
    if match:
        ref = match.group(1)
        entry = absolute(headerpath, ref)
        return f"#include <{entry}>\n"
    raise ValueError


def normalize_header(lines): pass


def normalize_headers(path, dry_run=False):
    """normalize all headers recursively

    convert
        "` to point braces
        relative to absolute paths
    """
    includes = get_headers(path)
    for include in includes:
        print(include.lstrip("include/"))
        with open(include, encoding="utf-8") as fopen:
            lines = fopen.readlines()
        _result = []
        for line in lines:
            if line.startswith("#include "):
                if line.endswith('"\n'):
                    line = line.strip()
                    converted = normalize_include_statement(line, include)
                    _result.append(converted)
                    print("  ", shorten(line), "->", shorten(converted.strip()))
                    continue

            _result.append(line)
        if not dry_run:
            with open(include, "w", encoding="utf-8") as fwrite:
                fwrite.writelines(_result)
        print()


def dump(path):
    """recursively list all headers"""
    includes = get_headers(path)
    for header_path in includes:
        print(header_path)


def commandline():
    """commmandline api"""
    parser = argparse.ArgumentParser(
        description="Convert include stmts to pointy braces and absolute paths."
    )

    parser.add_argument("path", help="path to include directory")

    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="run in dry-run mode without actual changes",
    )

    parser.add_argument("--backup", "-b", action="store_true", help="create backup")

    parser.add_argument("--list", "-l", action="store_true", help="list headers only")

    args = parser.parse_args()
    if args.path:
        if args.backup:
            shutil.copytree(args.path, f"{args.path}__BACKUP")
        if args.list:
            dump(args.path)
        else:
            normalize_headers(args.path, args.dry_run)


if __name__ == "__main__":
    commandline()
