import gc
import os
import platform
import re
import sys
import traceback
import warnings

from deoplete.source.base import Base
from operator import itemgetter
from typing import Optional

warnings.filterwarnings('ignore')


# Use Config project
class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name: Optional[str] = 'ein'
        self.filetypes = ['javascript', 'typescript', 'html']
        mark_synbol: Optional[str] = '[python: ' + str(platform.python_version()) + ']'
        self.mark = str(mark_synbol)
        js_match: Optional[list] = [r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*']
        html_match: Optional[list] = [r'[<a-zA-Z(?: .+?)?>.*?<\/a-zA-Z>]']
        self.input_pattern: Optional[str] = '|'.join(js_match + html_match)
        self.rank = 500

    def get_complete_position(self, context):
        m = re.search('[a-zA-Z0-9_?!]*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        try:
            # It doesn't support python4 yet.
            py_mj = sys.version_info[0]
            py_mi = sys.version_info[1]

            # 3.5 and higher, 4.x or less,python version is required.
            if (py_mj == 3 and py_mi > 4) or (py_mj < 4):

                # Settings, vim-plug | neovim path is true/false folder search.
                neo_f: Optional[str] = '~/.neovim/plugged/ein/dict/'
                neo_t = '~/.neovim/plugged/ein/dict/javascript.txt'

                # Settings, vim-plug | vim path is true/false folder search.
                vim_f: Optional[str] = '~/.vim/plugged/ein/dict/'
                vim_t = '~/.vim/plugged/ein/dict/javascript.txt'

                # Settings, $HOME/dict path is true/false folder search.
                loc_f: Optional[str] = '~/dict/'
                loc_t: Optional[str] = '~/dict/javascript.txt'

                # Use vim-plug | neovim, Set the dictionary.
                if os.path.exists(os.path.expanduser(neo_f)):

                    # User side, normal function.
                    with open(os.path.expanduser(neo_t)) as r_meth:
                        neo_py: Optional[list] = list(r_meth.readlines())
                        neo_comp: Optional[list] = [s.rstrip() for s in neo_py]
                        neo_comp.sort(key=itemgetter(0))
                        return neo_comp

                # Use vim-plug | vim, Set the dictionary.
                elif os.path.exists(os.path.expanduser(vim_f)):

                    # User side, normal function.
                    with open(os.path.expanduser(vim_t)) as r_vim:
                        vim_py: Optional[list] = list(r_vim.readlines())
                        vim_comp: Optional[list] = [s.rstrip() for s in vim_py]
                        vim_comp.sort(key=itemgetter(0))
                        return vim_comp

                # $HOME/dict, Set the dictionary to develop mode.
                elif os.path.exists(os.path.expanduser(loc_f)):

                    # Function change destination.
                    with open(os.path.expanduser(loc_t)) as rb_mt:
                        dev_py: Optional[list] = list(rb_mt.readlines())
                        dev_comp: Optional[list] = [s.rstrip() for s in dev_py]
                        sorted(dev_comp, key=itemgetter(0))
                        return dev_comp

                # Config Folder not found.
                else:
                    raise ValueError("None, Please Check the dict Folder")

            # Python_VERSION: 3.5 or higher and 4.x or less.
            else:
                raise ValueError("VERSION: 3.5 and higher, 4.x or less")

        # TraceBack.
        except Exception:
            # Load/Create LogFile.
            ein: Optional[str] = os.path.expanduser('~/ein_log/')
            db_w: Optional[str] = os.path.expanduser('~/ein_log/debug.log')

            # Load the dictionary.
            if os.path.isdir(ein):
                with open(db_w, 'a') as log_py:
                    traceback.print_exc(file=log_py)

                    # throw except.
                    raise RuntimeError from None

            # ein Foler not found.
            else:
                raise ValueError("None, Please Create $HOME/ein_log Folder.")

        # Custom Exception.
        except ValueError as ext:
            print(ext)
            raise RuntimeError from None

        # Once Exec.
        finally:
            # GC collection.
            gc.collect()
