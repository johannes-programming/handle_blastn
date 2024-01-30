import collections.abc as _abc
import contextlib as _cl
import dataclasses as _dc
import os as _os
import subprocess as _sp
import tempfile as _tmp
import typing as _typing

import Bio.SeqIO as _SeqIO
import Bio.SeqRecord as _SR
import seqreads as _sr

from ._summaries import *


@_dc.dataclass
class Cline:
    cmd:str="blastn"
    db:str
    query:str
    out:str
    def __iter__(self) -> _abc.Generator[str, None, None]:
        l = [
            self.cmd,
            '-db', self.db,
            '-query', self.query, 
            '-out', self.out,
            '-task', 'blastn',
            '-dust', 'no',
            '-outfmt', '5',
            '-max_target_seqs', '1',
            '-evalue', '0.0001',
            '-sorthits', '1',
        ]
        return (x for x in l)
    def dump(self, obj) -> int:
        """Dump data into queryfile in the fasta format."""
        record = _to_record(obj)
        return _SeqIO.write(self.query, "fasta", record)
    def exec(self, **kwargs) -> _typing.Any:
        """Run cline as subprocess."""
        return _sp.run(list(self), **kwargs)
    def summarize(self) -> Summary:
        """Create summary from outfile."""
        return Summary.from_file(self.out)
    def simple_run(self, obj, **kwargs) -> Summary:
        self.dump(obj)
        self.exec(**kwargs)
        return self.summarize(self)
    @classmethod
    def manager(cls, *args, **kwargs):
        """Cline manager."""
        return _manager(*args, cls=cls, **kwargs)

@_cl.contextmanager
def _manager(*args, cls, query=None, out=None, **kwargs):
    if (query is None) or (out is None):
        inner_manager = _tmp.TemporaryDirectory()
    else:
        inner_manager = _cl.nullcontext()
    with inner_manager as directory:
        query = _file(query, directory=directory, filename="query.fasta")
        out = _file(out, directory=directory, filename="out.txt")
        yield cls(*args, query=query, out=out, **kwargs)

def _file(file, *, directory, filename) -> str:
    if file is None:
        return _os.path.join(directory, filename)
    return str(file)

def _to_record(obj) -> _SR.SeqRecord:
    if type(obj) is _sr.SeqRead:
        return obj.to_record()
    if type(obj) is _SR.SeqRecord:
        return obj
    return _SR.SeqRecord(obj)





