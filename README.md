# norm_headers

Normalize headers for [binder](https://github.com/RosettaCommons/binder)


repo: <https://github.com/shakfu/norm_headers>



## transformations


1. [x] quotes to pointy brackets

```
#include "parent/abc.h" -> <parent/abc.h>
```

2. [x] relative to absolute path references

```
#include "../abc.h" -> <parent/abc.h>
```

3. [ ] pragma once to header guards

```
#pragma once
	|
	V
#ifndef ABC_H
#define ABC_H

...

#endif // ABC_H

```

