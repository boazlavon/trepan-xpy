# -*- coding: utf-8 -*-
#   Copyright (C) 2017, 2020 Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inspect
from xdis import findlinestarts

from trepan.processor.command.base_subcmd import DebuggerSubcommand
from trepan.lib.disassemble import disassemble_bytes
import trepan.lib.stack as Mstack
import linecache

# FIXME: this could be combined with trepan3k's `info pc`, which doesn't
# require a running program but uses use f_lasti.
# What we have here is less desirable the presence of exceptions,
# but this code would have to be looked over to see if it too would
# work.
class InfoPC(DebuggerSubcommand):
    """**info pc**

List the current program counter or bytecode offset,
and disassemble the instructions around that.

See also:
---------

`info line`, `info program`
"""

    min_abbrev = 2  # Need at least info 'pc'
    max_args = 0
    need_stack = True
    short_help = "Show Program Counter or Instruction Offset information"

    def print_locals_in_all_frames(self, curframe, limit=None):
        count = 0  # Initialize a counter to limit frames
        
        proc = self.proc
        frame = curframe
        while frame is not None and (limit is None or count < limit):
            print('[[[FrameEntry]]]')
            print(f"[[[FrameIndex]]] {count} [[[/FrameIndex]]]")
            #print(f"[[[FrameId]]] {id(frame)} [[[/FrameId]]]")
            print(f"[[[Function]]] {frame.f_code.co_name} [[[/Function]]]")
            filename = Mstack.frame2file(self.proc.core, frame, canonic=False)
            print(f"[[[Filename]]] {filename} [[[/Filename]]]")
            print(f"[[[Locals]]]\n{frame.f_locals}\n[[[/Locals]]]")
            line_no = inspect.getlineno(frame)
            line = linecache.getline(filename, line_no, frame.f_globals)

            self.msg('[[[LineNumber]]]')
            self.msg(line_no)
            self.msg('[[[/LineNumber]]]')

            self.msg('[[[SourceLine]]]')
            self.msg(line)
            self.msg('[[[/SourceLine]]]')

            offset = frame.f_lasti
            self.msg('[[[PcOffset]]]')
            self.msg(offset)
            self.msg('[[[/PcOffset]]]')
            self.msg('')

            offset = max(offset, 0)
            code = frame.f_code
            co_code = code.co_code

            self.msg('[[[DisassembleBytes]]]')
            disassemble_bytes(
                self.msg,
                self.msg_nocr,
                code = co_code,
                lasti = offset,
                cur_line = line_no,
                start_line = line_no - 1,
                end_line = line_no + 1,
                varnames=code.co_varnames,
                names=code.co_names,
                constants=code.co_consts,
                cells=code.co_cellvars,
                freevars=code.co_freevars,
                linestarts=dict(findlinestarts(code)),
                #end_offset=offset + 10,
                end_offset=None,
                opc=proc.vm.opc,
            )
            self.msg('[[[/DisassembleBytes]]]')
            print('[[[/FrameEntry]]]')

            # Move to the previous frame
            frame = frame.f_back
            count += 1

    def run(self, args, limit=5):
        print('[[[InfoFrames]]]')
        self.print_locals_in_all_frames(self.proc.curframe, limit)
        print('[[[/InfoFrames]]]')

    # def run(self, args):
    #     """Program counter."""
    #     proc = self.proc
    #     curframe = proc.curframe
    #     if curframe:
    #         line_no = inspect.getlineno(curframe)
    #         offset = curframe.f_lasti

    #         self.msg('[[[PcOffset]]]')
    #         self.msg("PC offset is %d." % offset)
    #         self.msg('[[[/PcOffset]]]')
    #         self.msg('')

    #         offset = max(offset, 0)
    #         code = curframe.f_code
    #         co_code = code.co_code

    #         self.msg('[[[DisassembleBytes]]]')
    #         disassemble_bytes(
    #             self.msg,
    #             self.msg_nocr,
    #             code = co_code,
    #             lasti = offset,
    #             cur_line = line_no,
    #             start_line = line_no - 1,
    #             end_line = line_no + 1,
    #             varnames=code.co_varnames,
    #             names=code.co_names,
    #             constants=code.co_consts,
    #             cells=code.co_cellvars,
    #             freevars=code.co_freevars,
    #             linestarts=dict(findlinestarts(code)),
    #             #end_offset=offset + 10,
    #             end_offset=None,
    #             opc=proc.vm.opc,
    #         )
    #         self.msg('[[[/DisassembleBytes]]]')
    #         # args = [('msg', self.msg),
    #         #     ('msg_nocr', self.msg_nocr),
    #         #     ('code', co_code),
    #         #     ('lasti', offset),
    #         #     ('cur_line',line_no),
    #         #     ('start_line', line_no - 1),
    #         #     ('end_line', line_no + 1),
    #         #     ('varnames', code.co_varnames),
    #         #     ('names', code.co_names),
    #         #     ('constants',code.co_consts),
    #         #     ('cells',code.co_cellvars),
    #         #     ('freevars',code.co_freevars),
    #         #     ('linestarts',dict(findlinestarts(code))),
    #         #     ('end_offset', None)]
    #         #self.msg(args)
    #         pass
        return False

    pass


if __name__ == "__main__":
    from trepan.processor.command import mock, info as Minfo

    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoPC(i)
    sub.run([])
