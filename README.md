# header_utils.py

Convert headers to a [binder](https://github.com/RosettaCommons/binder>) friendly format.

repo: <https://github.com/shakfu/header_utils>


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

- [x] quotes to pointy brackets

```c++
#include "parent/abc.h" -> <parent/abc.h>
```

- [x] relative to absolute include path references

```c++
#include "../abc.h" -> <parent/abc.h>
```

- [x] pragma once to header guards

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


## Usage

Here are some usage examples (full commandline api is provided below):

- Run `header_utils`'s default transformations in `dry-run` mode which will not make any changes. In this case, you can see what changes will occur to each `#include` statement in each file in the provided directory. 

```
$ ./header_utils.py --dry-run include
```

- Provide an `output-dir` to `header_utils`. In this mode, default transformations will be applied to headers in the `output-dir`. Specifying a `graph` path with `.pdf` suffix will have `header_utils` generate a pdf graph (and dot file) of header-file dependencies using graphviz.


```
$ ./header_utils.py --output-dir=include-mod --graph=depends.pdf include
```

- Run `header_utils`'s default transformations in `in-place` mode which **will** make changes directly to the provided directory. An automatic time-stamped backup will be made in this case. Only headers with an `.hpp` suffix will be modified as opposed to any of the default ['.h', '.hpp', '.hh']

```
$ ./header_utils.py --header-endings .hpp include
```


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

