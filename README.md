# NVGT PKG
A simple, open source command line package manager for [NVGT](https://nvgt.dev) audio game engine.

[Visit NVGT Package Manager's Official Website](https://harrymkt.github.io/nvgtpkg)

NVGT Package Manager uses **JSON** as its formatter; therefore, all configuration files must use the `.json` extension. Standard JSON syntax is required (e.g., keys and strings must be enclosed in double quotes).

## Usage
To use the package manager software, run `nvgtpkg` to display the help menu. To get help for a specific command, run `nvgtpkg <command> -h` or `nvgtpkg <command> --help`.

If you are using the non-compiled version, run `python nvgtpkg.py` instead of the executable.

## License
NVGT Package Manager is licensed under the terms of the MIT license.

## Creating a package
To create a package for the NVGT Package Manager:
- Create your library files using include directives.
- Ensure `main.nvgt` is in the root directory of the package folder. Users will include your package via `#include "package_name/main.nvgt"`.
- Add a `package.json` file in the JSON format to your root directory.

### Content for package.json
Use the following structure for your metadata:
```json
{
  "name": "Your Package Display Name",
  "description": "Optional description of your package",
  "download_url": "https://example.com/package.zip",
  "author": {
    "name": "Author Name",
    "homepage": "Author_homepage_or_mailto:email"
  }
}
```

## Publishing a package
To publish, submit a pull request to the official repository with these changes:
- Copy your `package.json` to the `assets/pkgs` directory of the repository.
- Rename the file to your **package short name** (e.g., `my-package.json`). The short name must not contain spaces; use underscores or dashes instead.

## Building NVGTPKG
To build the software from source, ensure you have Python 3 installed, then:
1. Install dependencies: `pip install -r requirements.txt`.
2. Install PyInstaller: `pip install --upgrade pyinstaller`.
3. Run the build command:
```bash
pyinstaller --onefile --console nvgtpkg.py
```

## Contributing
Contributions must follow the [contributing guidelines](.github/CONTRIBUTING.md) and are licensed under the MIT license. You may add credits to your specific scripts, but the general copyright notice must remain unchanged.