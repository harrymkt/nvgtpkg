import os
import shutil
import argparse
import toml
import sys
import requests
import zipfile

PACKAGE_INDEX_URL = "https://raw.githubusercontent.com/harrymkt/nvgtpkg/main/assets/index.toml"
packstore = ""

def load_package_index():
	"""Fetch the latest package index from the server."""
	try:
		response = requests.get(PACKAGE_INDEX_URL)
		return toml.loads(response.text) if response.status_code == 200 else {}
	except Exception as e:
		print(f"Error fetching package index: {e}")
		return {}

def install_package(args):
	"""Install an NVGT package by downloading and extracting it."""
	package_name = args.package_name
	if package_name == None:
		print("No package name")
		sys.exit(1);
	index = load_package_index()
	if package_name not in index:
		print(f"Package '{package_name}' does not exist in package index")
		return
	pindex = index[package_name]
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
		print(f"Found {pg.get("name", name)}")
		if not pg.get("name", name) == name:
			print("Module name:")
			print(name)
		print("Author:")
		print(pg["author"]["name"])
		if hasattr(pg, "description"):
			print("Description:")
			print(pg["description"])
	else:
		print(f"No package with the term {args.name} found in your installed packages.")

if __name__ == "__main__":
	p = argparse.ArgumentParser(description = "NVGT Package Manager")
	p.add_argument("-d", "-directory", dest = "directory", help = "Path to NVGT installation directory", default = os.path.dirname(shutil.which("nvgt")))
	sp = p.add_subparsers(title = "Commands", description= "Available commands")
	install = sp.add_parser("install", help= "Install a package")
	install.add_argument("package_name", help = "Name of the package to install")
	install.set_defaults(func = install_package)
	listpacks = sp.add_parser("list", help = "List installed packages")
	listpacks.set_defaults(func = list_installed_packages)
	showpack = sp.add_parser("show", help = "Shows information about a given installed package")
	showpack.add_argument("name", help = "The name of the package to search if it is installed")
	showpack.set_defaults(func = show_package)
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