import sys, os
from cx_Freeze import setup, Executable

#############################################################################
# preparation des options

# chemins de recherche des modules
path = sys.path # + ["images", "trad", '', '..', 'library']
print(sys.path)
# options d'inclusion/exclusion des modules
includes = ["PyQt5"]
excludes = []
packages = []

# copier les fichiers et/ou répertoires et leur contenu:
includefiles = [("images", "images/tokens")]
if sys.platform == "linux2":
    includefiles += [(r"/usr/lib/qt5/plugins/sqldrivers", "sqldrivers")]
elif sys.platform == "win32":
    includefiles += [("")]
else:
    pass

# pour inclusion éventuelle de bibliothèques supplémentaires
binpathincludes = []
if sys.platform == "linux2":
    # pour que les bibliothèques de /usr/lib soient copiées aussi
    binpathincludes += ["/usr/lib"]

# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes
           }

#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"

cible_1 = Executable(
    script="__init__.py",
    base=base,
    icon=None,
)

#############################################################################
# creation du setup
setup(
    name="Coronabi",
    version="1",
    description="Portage Hanabi",
    author="CCSF",
    options={"build_exe": options},
    executables=[cible_1]
)