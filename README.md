# NVGT PKG
A simple package manager for [NVGT](https://nvgt.gg).

## Creating a package
If you want to create a package, first setup a Git repository. This Git repository is not necessary unless you want to publish to NVGTPKG packages.

Once you have necessary setups:
- Create the library files, using include directives, separating them is possible as you want.
- `main.nvgt` should be in the root directory of the package folder. This file is used as an include starting file for users who will include `#include "package_name/main.nvgt"`
- Next, add `package.toml` with the TOML format. What variables can you use will be provided below.

That's it!

### Variables for package.toml
- `name`(string): The name of the package. Can contain spaces.

---

## Publishing a package
Once you have created a package you want create a pull request to this repository to publish it.
First, Edit the `index.toml`, adding your library to the end of the file. Copy the content below for TOML format to edit index.toml. However, first note:
1. `packname` should be replaced your short, friendly package name. No spaces, use dashes.
```toml
[packname]
# Other variables here
```

### Variables in index.toml
These variables must be placed after the package name, for example, `[packname]`.
- `name`(string) optional: The name of the package. Can contain spaces.
- `download_url`(string) required: The direct URL to download the package.