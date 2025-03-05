import importlib
from typing import List
import os.path
from pathlib import Path
from django.conf import settings
default_app_config = "pycom.payment"


def discover_plugins_modules(plugins: List[str]):
    plugins_modules = []
    for dotted_path in plugins:
        try:
            module_path, class_name = dotted_path.rsplit(".", 1)
        except ValueError as err:
            raise ImportError(f"{dotted_path} doesn't look like a module path") from err

        module = importlib.import_module(module_path)
        plugins_modules.append(module.__package__)
    return plugins_modules
def loadGateways():
  path1 = Path(__file__).parent
  abspath=path1.absolute()
  #print("in loadgateways")
  path2=Path(path1,'gateways')
  #print(path1.absolute().iterdir('gateways'))
  #print(settings.INSTALLED_APPS)
  k=[x for x in path2.iterdir() if x.is_dir()]
  for module_path in k :
   #print(module_path.name)
   if not module_path.name=='__pycache__':
        pp='payment.gateways.'+module_path.name+'.apps.'+module_path.name.title()+'Config'
        #print(pp)
        settings.INSTALLED_APPS.append(pp)
        #importlib.import_module(pp)
loadGateways()  