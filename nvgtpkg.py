import os
import toml
import requests
import zipfile
PACKAGE_INDEX_URL = "https://raw.githubusercontent.com/harrymkt/nvgt-packages/main/index.json"
packstore = "C:/nvgt/include"

def load_package_index():
	"""Fetch the latest package index from the server."""
	try:
		response = requests.get(PACKAGE_INDEX_URL)
		return toml.load(response.text) if response.status_code == 200 else {}
	except Exception as e:
		print(f"Error fetching package index: {e}")
		return {}

def install_package(package_name):
	"""Install an NVGT package by downloading and extracting it."""
	index = load_package_index()
	if package_name not in index:
		print(f"Package '{package_name}' not found!")
		return
	pindex = index[package_name]
	package_url = pindex["download_url"]
	package_zip = f"{packstore}/{package_name}.zip"
	print(f"Found {pindex.get("name", package_name)}. Downloading...")
	if os.path.exists(package_zip):
		print("Using cash");
	else:
		response = requests.get(package_url)
		if not response.status_code == 200:
			print(f"Failed to download '{package_name}'.")
			sys.exit(1)
		else:
			f = open(package_zip, "wb")
			f.write(response.content)
	# Extract files
	print(f"Extracting {pindex.get("name", package_name)}...")
	try:
		with zipfile.ZipFile(package_zip, "r") as zip_ref:
			zip_ref.extractall(f"{packstore}/{package_name}")
			print(f"Installed '{pindex.get("name", package_name)}' successfully!")
			os.remove(package_zip)
	except:
		print(f"Failed to install '{package_name}'.")

def list_installed_packages():
	"""List all installed NVGT packages."""
	l = [d for d in os.listdir(packstore) if os.path.isdir(os.path.join(packstore, d))]
	if len(l) < 1:
		print("No packages installed.")
		return
	for package in l:
		fullp = os.path.join(packstore, package)
		pg = toml.load(os.path.join(fullp, "package.toml")) if os.path.exists(os.path.join(fullp, "package.toml")) else dict()
		print(f"{pg.get("name", package)}")
if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("Usage: nvgtpkg <command> [package]")
		print("install or i, installs a package")
		print("list or l, lists packages you have installed")
		sys.exit(1)

	command = sys.argv[1]
	
	if (command == "install" or command == "i") and len(sys.argv) > 2:
		install_package(sys.argv[2])
	elif command == "list" or command == "l":
		list_installed_packages()
	else:
		print("Unknown command!")