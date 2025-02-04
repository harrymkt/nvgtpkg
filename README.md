# NVGT PKG
A simple, open source command line package manager for [NVGT](https://nvgt.gg) audio game engine.

[Visit NVGT Package Manager's Official Website](https://harrymkt.github.io/nvgtpkg)

NVGT Package Manager uses [TOML](https://toml.io/en/) as formatter, thus any configuration file must use TOML. Format indentation is expected, and must use tab over space.

## Usage
To use the package manager software, run `nvgtpkg` and it will display help. To get help for a command you can run `nvgtpkg <command> -h` or `nvgtpkg <command> --help`.

Note that if you are using non compiled version you may run `nvgtpkg.py` instead of `nvgtpkg`.

## Creating a package
If you want to create a package, first setup a Git repository. This Git repository is not necessary unless you want to publish to NVGTPKG packages easily.

Once you have necessary setups:
- Create the library files, using include directives, separating them is possible as you want.
- `main.nvgt` should be in the root directory of the package folder. This file is used as an include starting file for users who will include `#include "package_name/main.nvgt"`
- Next, add `package.toml` with the TOML format. Content that you can copy will be provided below.

That's it!

### content for package.toml
```toml
# Optional Name. can contain spaces
name = "Your Package Display Name"
# Optional description
description = ""
# Direct URL to download, only required if you want to publish the package.
download_url = "https://example.com/package.zip"
# Author information
[author]
	name = "Author Name"
	# Optional homepage key that specifies the website, or the email, of the author. If it is email, start with mailto:
	homepage = "Author_homepage"
```

---

## Publishing a package
Once you have created a package, create a pull request to this repository to publish it with the following changes to this repository:
- First, Copy your package's package.toml to assets/pkgs.
- Next, rename the file as your package short name. A package short name cannot contain spaces, and must use underlines or dashes.

---

## Building NVGTPKG
If you want to contribute code to NVGTPKG software, you will first know how to build.

To build NVGT Package Manager software:
- First, make sure you have [Python](https://www.python.org/) 3 and above installed.
- Install the requirements.
	```bash
	pip install -r requirements.txt
	```
- Install PyInstaller.
	```bash
	pip install --upgrade pyinstaller
	```
- Lastly, run the following command from the root of the NVGTPKG repository:
	```bash
	pyinstaller --onefile --console nvgtpkg.py
	```
