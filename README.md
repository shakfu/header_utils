# header_utils.py

Convert headers to a [binder](https://github.com/RosettaCommons/binder>) friendly format.

repo: <https://github.com/shakfu/header_utils>

## Features

### Header Transformations

Default

- Convert include statements with quotes to pointy brackets.

```c++
#include "parent/abc.h" -> <parent/abc.h>
```

- Convert relative to absolute include path references.

```c++
#include "../abc.h" -> <parent/abc.h>
```

Optional

- Convert `#pragma once` entries to header guards.

```c++
#pragma once
```

becomes

```c++
#ifndef ABC_H
#define ABC_H

...

#endif // ABC_H

```

### Dependency Analysis

- Generate a graphviz (pdf|png|svg) graph of header dependencies.

This requires:

```bash
pip install graphviz
```

and graphviz to be installed on your system. On macOS for example:

```bash
brew install graphviz
```

## Usage

A few usage examples (full commandline api is provided below):

```bash
./header_utils.py --dry-run include
```

Apply default transformations in `dry-run` mode without making any changes.

```bash
./header_utils.py --output-dir=include-mod include
```

Apply default transformations to headers copied to an `output-dir`. 


```bash
./header_utils.py --graph=depends.pdf include
```

Apply default transformations 'in-place' to headers in the `include` directory.
and generate a pdf graph of header-file dependencies using graphviz.
An automatic time-stamped backup will be made in this case. 


```bash
./header_utils.py --header-endings .hpp include
```

Run `header_utils`'s default transformations in `in-place` mode. Only headers with an `.hpp` suffix will be modified as opposed to any with the default ['.h', '.hpp', '.hh'] endings.


## Commandline API

```text
usage: header_utils.py [-h] [--output-dir OUTPUT_DIR]
                       [--header-endings HEADER_ENDINGS [HEADER_ENDINGS ...]]
                       [--header-guards] [--dry-run] [--skip-backup] [--list]
                       [--graph GRAPH]
                       path

Convert headers to a binder friendly format. (default: ['.h', '.hpp', '.hh'])

positional arguments:
  path                  path to include directory

optional arguments:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory for modified headers (default: None)
  --header-endings HEADER_ENDINGS [HEADER_ENDINGS ...], -e HEADER_ENDINGS [HEADER_ENDINGS ...]
  --header-guards       convert `#pragma once` to header guards (default:
                        False)
  --dry-run, -d         run in dry-run mode without actual changes (default:
                        False)
  --skip-backup, -s     skip creating backup if output_dir is not provided
                        (default: False)
  --list, -l            list target headers only (default: False)
  --graph GRAPH, -g GRAPH
                        output path for graphviz graph with format suffix
                        [png|pdf|svg] (default: None)
```
