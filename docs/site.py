import os
import sys

import django

print("=======================================")
print(" HERE ")
print("=======================================")


sys.path.append(os.path.abspath("../../"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")


django.setup()
