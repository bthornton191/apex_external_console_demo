import atexit as _atexit
import remoting as _remoting


_remoting.forceCloseKernels()
_remoting.launchApplication()
_atexit.register(_remoting.shutdownApplication)

import apex as _apex

# Define the units system
_apex.setScriptUnitSystem(unitSystemName = r'''in-slinch-s-lbf''') #pylint:disable=no-member
