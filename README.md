# header_utils.py

Convert headers to a [binder]https://github.com/RosettaCommons/binder) friendly format.

repo: <https://github.com/shakfu/header_utils>

## Usage

```
usage: header_utils.py [-h] [--dry-run] [--backup] [--list] [--graph GRAPH]
                       path

Convert include stmts to pointy braces and absolute paths.

positional arguments:
  path                  path to include directory

optional arguments:
  -h, --help            show this help message and exit
  --dry-run, -d         run in dry-run mode without actual changes
  --backup, -b          create backup
  --list, -l            list target headers only
  --graph GRAPH, -g GRAPH
                        path to output graphviz graph [png|pdf|svg]
```

## Features

Header Transformations

- Quotes to pointy brackets
- Relative to absolute include path references
- Pragma once to header guards

Analysis

- Generate graphviz (pdf|png|svg) graph of header dependencies.

This requires:

```bash
pip install graphviz
```

and graphviz to be installed on your system. On macOS for example:

```bash
brew install graphviz
```


### List of Transformations


1. [x] quotes to pointy brackets

```
#include "parent/abc.h" -> <parent/abc.h>
```

2. [x] relative to absolute include path references

```
#include "../abc.h" -> <parent/abc.h>
```

3. [x] pragma once to header guards

```
#pragma once
```
becomes
```
#ifndef ABC_H
#define ABC_H

...

#endif // ABC_H

```
