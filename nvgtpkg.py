import os
import shutil
import argparse
import toml
import sys
import requests
import zipfile
import fnmatch

package_path = "assets/pkgs"
packstore = ""

def install_package(package_name):
	"""Install an NVGT package by downloading and extracting it."""
	if package_name == None:
		print("No package name")
		return
	data = get_url(f"https://raw.githubusercontent.com/harrymkt/nvgtpkg/main/{package_path}/{package_name}.toml")
	if isinstance(data, Exception):
		if data == "":
			print(f"Package {package_name} not found")
		else:
			print(f"Failed to retrieve package {package_name}. {data}")
		return
	elif data == None:
		print("No package data")
		return
	pindex = toml.loads(data)
	package_url = pindex["download_url"]
	package_zip = f"{packstore}/{package_name}.zip"
	print(f"Found {pindex.get("name", package_name)} by {pindex["author"]["name"]}.")
	if os.path.exists(package_zip):
		print("Using cash");
	else:
		print("Downloading...")
		response = requests.get(package_url)
		if not response.status_code == 200:
			print(f"Failed to download '{package_name}'.")
			sys.exit(1)
		else:
			f = open(package_zip, "wb")
			f.write(response.content)
			f.close()
	# Extract files
	print(f"Extracting {pindex.get("name", package_name)}...")
	try:
		with zipfile.ZipFile(package_zip, "r") as zip_ref:
			zip_ref.extractall(f"{packstore}/{package_name}")
			zip_ref.close()
			print(f"Installed '{pindex.get("name", package_name)}' successfully!")
			os.remove(package_zip)
	except Exception as e:
		print(f"Failed to install '{pindex.get("name", package_name)}'. {e}")

def install_packages(args):
	packages = args.packages
	if args.fn:
		for x in args.fn:
			x = x.strip()
			if x.startswith("#"): continue
			packages.append(x)
	if len(args.packages) < 1:
		print("No packages provided")
		return
	print(f"Trying to install {len(packages)} packages: {", ".join(packages)}")
	for p in args.packages:
		install_package(p)

def list_installed_packages(args):
	"""List all installed NVGT packages."""
	l = [d for d in os.listdir(packstore) if os.path.isdir(os.path.join(packstore, d))]
	if len(l) < 1:
		print("No packages installed.")
		return
	for package in l:
		fullp = os.path.join(packstore, package)
		pg = toml.load(os.path.join(fullp, "package.toml")) if os.path.exists(os.path.join(fullp, "package.toml")) else dict()
		print(f"{pg.get("name", package)} by {pg["author"]["name"]}")

def show_package(args):
	"""Shows information about given installed package if available"""
	l = [d for d in os.listdir(packstore) if os.path.isdir(os.path.join(packstore, d))]
	if len(l) < 1:
		print("No packages installed.")
		return
	haspack = False
	name = args.name
	for package in l:
		if package.lower() == args.name.lower():
			haspack = True
			name = package
	if haspack:
		pg = toml.load(os.path.join(packstore, name, "package.toml")) if os.path.exists(os.path.join(packstore, name, "package.toml")) else dict()
		package_info(name, pg)
	else:
		print(f"No package with the term {args.name} found in your installed packages.")

def package_info(name, pg):
	if name == None or pg == None: return
	print(f"Found {pg.get("name", name)}")
	if not pg.get("name", name) == name:
		print("Module name:")
		print(name)
	print("Author:")
	print(pg["author"]["name"])
	if pg["description"]:
		print("Description:")
		print(pg["description"])

def search_package(args):
	package_name = args.name
	if package_name == None:
		print("No package name")
		sys.exit(1);
	print("Searching for package")
	data = get_url(f"https://raw.githubusercontent.com/harrymkt/nvgtpkg/main/{package_path}/{package_name}.toml")
	if isinstance(data, Exception):
		if data == "":
			print("Package not found")
		else:
			print(f"Failed to retrieve package. {data}")
		return
	elif data == None:
		print("No package data")
		return
	pindex = toml.loads(data)
	package_info(package_name, pindex)

def list_files_in_repo(owner, repo, path, pattern, recursive = False):
	"""Lists files in a GitHub repository matching a given pattern."""
	url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
	try:
		response = requests.get(url)
		if not response.status_code == 200:
			return Exception()
		contents = response.json()
		matching_files = []
		for item in contents:
			if item["type"] == "file":
				if fnmatch.fnmatch(item["name"], pattern):
					matching_files.append(item["path"])
			elif recursive and item["type"] == "dir": # Handle subdirectories recursively
				matching_files.extend(list_files_in_repo(owner, repo, item["path"], pattern, recursive)) # Recursive call
		return matching_files

	except Exception as e:
		return e

def get_url(url):
	try:
		response = requests.get(url)
		if not response.status_code == 200:
			return Exception()
		return response.text
	except Exception as e:
		return e

if __name__ == "__main__":
	p = argparse.ArgumentParser(description = "NVGT Package Manager")
	p.add_argument("-d", "-directory", dest = "directory", help = "Path to NVGT installation directory", default = os.path.dirname(shutil.which("nvgt")))
	sp = p.add_subparsers(title = "Commands", description= "Available commands")
	install = sp.add_parser("install", help= "Install a package")
	install.add_argument("-r", dest = "fn", help = "The file name to read the packages from", type = argparse.FileType("r"))
	install.add_argument("packages", help = "Names of the packages to install", action = "extend", nargs = "*")
	install.set_defaults(func = install_packages)
	listpacks = sp.add_parser("list", help = "List installed packages")
	listpacks.set_defaults(func = list_installed_packages)
	showpack = sp.add_parser("show", help = "Shows information about a given installed package")
	showpack.add_argument("name", help = "The name of the package to search if it is installed")
	showpack.set_defaults(func = show_package)
	searchpack = sp.add_parser("search", help = "Searches a package online without any installation")
	searchpack.add_argument("name", help = "The name of the package to search for")
	searchpack.set_defaults(func = search_package)
	args = p.parse_args()
	packstore = args.directory
	if not os.path.isdir(packstore): packstore = os.path.dirname(args.directory)
	if not packstore or not os.path.exists(packstore):
		print("Error, NVGT installation directory cannot be determined")
		sys.exit(1)
	elif not os.path.isdir(packstore):
		print("Error, provided NVGT installation path is not a directory")
		sys.exit(1)
	packstore = os.path.join(packstore, "include")
	if not os.path.exists(packstore):
		print("Error, NVGT has no include directory")
		sys.exit(1)
	if hasattr(args, "func"):
		args.func(args)
	else:
		p.print_help()