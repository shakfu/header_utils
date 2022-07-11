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

Note: As a safety measure: `header_utils.py` does not do in-place transformations.
It will always write its transformations to a copy of the `input_dir`.  

If `dry-mode` is active no changes are made. 

If dry-mode is not active, then an `output_dir` must be provided.


### 1. Dry-run mode

```bash
./header_utils.py --graph=depends.pdf --dry-run include
```

Print out default transformations in `dry-run` mode without making any changes.
Also generate a pdf graph of header-file dependencies using graphviz.

### 2. Transformation mode with depenency graph generation

```bash
./header_utils.py include-src include-dst
```

Apply default transformations to headers copied to `include-dst`.

### 3. Transformation mode with custom endings filter

```bash
./header_utils.py --header-endings .hpp include-src include-dst
```

Run `header_utils` with default transformations. In this case, only headers with an `.hpp` suffix will be modified as opposed to the default: any with ['.h', '.hpp', '.hh'] endings.


## Commandline API

```text
usage: header_utils.py [-h]
                       [--header-endings HEADER_ENDINGS [HEADER_ENDINGS ...]]
                       [--header-guards] [--dry-run] [--force-overwrite]
                       [--list] [--graph GRAPH]
                       input_dir output_dir

Convert headers to a binder friendly format. (default: ['.h', '.hpp', '.hh'])

positional arguments:
  input_dir             input include directory containing source headers
  output_dir            output directory for modified headers

optional arguments:
  -h, --help            show this help message and exit

  --header-endings HEADER_ENDINGS [HEADER_ENDINGS ...], -e HEADER_ENDINGS [HEADER_ENDINGS ...]
  
  --header-guards       convert `#pragma once` to header guards (default: False)
  
  --dry-run, -d         run in dry-run mode without actual changes (default: False)

  --force-overwrite, -f force overwrite output_dir if it already exists (default: False)
  
  --list, -l            list target headers only (default: False)
  
  --graph GRAPH, -g GRAPH
                        output path for graphviz graph with format suffix
                        [png|pdf|svg] (default: None)
```
