import cbpro
from itertools import islice
from sty import fg, bg
import Settings

auth_client = cbpro.AuthenticatedClient(Settings.Key,
                                        Settings.Secret,
                                        Settings.Pass)

print(auth_client.get_accounts())