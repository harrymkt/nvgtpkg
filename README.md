# NVGT PKG
A simple package manager for [NVGT](https://nvgt.gg) audio game engine.

[Visit NVGT Package Manager's Official Website](https://harrymkt.github.io/nvgtpkg)

NVGT Package Manager uses TOML as formatter, thus any configuration file must use TOML. Format indentation is expected, and must use tab over space.

## Creating a package
If you want to create a package, first setup a Git repository. This Git repository is not necessary unless you want to publish to NVGTPKG packages.

Once you have necessary setups:
- Create the library files, using include directives, separating them is possible as you want.
- `main.nvgt` should be in the root directory of the package folder. This file is used as an include starting file for users who will include `#include "package_name/main.nvgt"`
- Next, add `package.toml` with the TOML format. Content that you can copy will be provided below.

That's it!

### content for package.toml
```toml
# Name can contain spaces
name = "Your Package Display Name"
# Optional description
description = ""
# Author information
[author]
	name = "Author Name"
	# Optional homepage key that specifies the website, or the email, of the author. If it is email, start with mailto:
	homepage = "Author_homepage"
```

---

## Publishing a package
Once you have created a package you want create a pull request to this repository to publish it.

First, Edit the `assets/index.toml`, adding your library to the end of the file. Copy the content below for TOML format to edit index.toml. However, first note:
- `packname` should be replaced with your short, friendly package name. No spaces, use dashes.
```toml
[packname]
	# Name can contain spaces
	name = "Your Package Display Name"
	# Author information
	[packname.author]
		name = "Author Name"
		# Optional homepage key that specifies the website, or the email, of the author. If it is email, start with mailto:
		homepage = "Author_homepage"
```