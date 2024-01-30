import wonderparse as _wp

from ._clines import Cline
from ._summaries import Summary
from . import _progs

def main(args=None):
    _wp.easymode.simple_run(
        args=args,
        program_object=_progs,
        prog='handle_blastn',
    )

if __name__ == '__main__':
	main()