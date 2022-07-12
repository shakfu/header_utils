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

**Note**: 

- As a safety measure: `header_utils.py` does not do in-place transformations. It will *always* write its transformations to a copy of the `input_dir`.  

- If `dry-run` mode is active no changes are made, and an `output_dir` need not be provide. In this mode, [graphviz](https://graphviz.org) dependency graphs can be generated from the `input_dir`.

- If `dry-run` mode is not active, then an `output_dir` must be provided.


### 1. Dry-run mode

```bash
./header_utils.py --graph=depends.pdf --dry-run include
```

Print out default transformations in `dry-run` mode without making any changes.
Also generate a pdf graph of header-file dependencies using [graphviz](https://graphviz.org).

### 2. Default Transformations with dependency graph generation

```bash
./header_utils.py include-src include-dst
```

Apply default transformations to headers copied to `include-dst`.

### 3. Default Transformations with custom endings filter

```bash
./header_utils.py --header-endings .hpp include-src include-dst
```

In this case, only headers with an `.hpp` suffix will be modified as opposed to the default: any with ['.h', '.hpp', '.hh'] endings.

### 4. Default Transformations with transform header-guards option

```bash
./header_utils.py --header-guards include-src include-dst
```

Apply default transformations to headers and also apply conversion of `#pragma once` entries to header guards.

## Commandline API

```text
usage: header_utils.py [-h] [--output_dir OUTPUT_DIR]
                       [--header-endings HEADER_ENDINGS [HEADER_ENDINGS ...]]
                       [--header-guards] [--dry-run] [--force-overwrite]
                       [--list] [--graph GRAPH]
                       input_dir

Convert headers to a binder friendly format. (default: ['.h', '.hpp', '.hh'])

positional arguments:
  input_dir             input include directory containing source headers

optional arguments:
  -h, --help            show this help message and exit

  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory for modified headers (default: None)
  
  --header-endings HEADER_ENDINGS [HEADER_ENDINGS ...], -e HEADER_ENDINGS [HEADER_ENDINGS ...]
  
  --header-guards       convert `#pragma once` to header guards (default: False)
  
  --dry-run, -d         run in dry-run mode without actual changes (default: False)
  
  --force-overwrite, -f
                        force overwrite output_dir if it already exists (default: False)
  
  --list, -l            list target headers only (default: False)
  
  --graph GRAPH, -g GRAPH
                        output path for graphviz graph with format suffix
                        [png|pdf|svg] (default: None)
```

## Testing

To test `header_utils.py`, ensure you have `pytest` installed. Note that this project uses the actual headers from the [taskflow](https://github.com/taskflow/taskflow) project to test its functionality.

```bash
pytest
```

## TODO

- [ ] add more tests
