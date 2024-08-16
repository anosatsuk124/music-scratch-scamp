from IPython import start_ipython
from traitlets.config import Config

c = Config()

# lines of code to run at IPython startup.
# NOTE: disabling autoreload in ipython_config.py will improve performance.
c.InteractiveShellApp.exec_lines = [
    "import scamp as sc",  # import scamp
    "%autoreload 2",
]

# A list of dotted module names of IPython extensions to load.
c.InteractiveShellApp.extensions = [
    "autoreload"
]

start_ipython(config=c)
