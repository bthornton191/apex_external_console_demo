import atexit as _atexit
import remoting as _remoting

# Launch the application
# NOTE: This must be done before importing apex
_remoting.launchApplication()

# This line makes the Apex application close if the script terminates
_atexit.register(_remoting.shutdownApplication)

import apex as _apex
# Define the units system
_apex.setScriptUnitSystem(unitSystemName = r'''in-slinch-s-lbf''') #pylint:disable=no-member
