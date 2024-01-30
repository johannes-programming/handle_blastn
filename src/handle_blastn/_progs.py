import os as _os

import Bio.SeqIO as _SeqIO
import fileunity as _fu

from . import _clines, _summaries

def summarize(
    infile: str,
) -> _fu.TOMLUnit:
    summary = _summaries.Summary.from_file(infile)
    return _fu.TOMLUnit(vars(summary))

def run_cmd(
    query:str,
    *,
    query_format:dict(
        choices=['infer', 'Seq', 'fasta', 'abi', 'phd'],
        type=str,
    )='infer',
    cmd:str = "blastn",
    db:str,
) -> _fu.TextUnit:
    query_format = _query_format(query, query_format)
    with _clines.Cline.manager(cmd=cmd, db=db) as cline:
        if query_format == 'fasta':
            cline.query = query
        elif query_format == 'Seq':
            cline.dump(query)
        else:
            rec = _SeqIO.read(query, query_format)
            cline.dump(rec)
        cline.exec()
        ans = _fu.TextUnit.from_file(cline.out)
        return ans

def _query_format(
    query:str, 
    query_format:str,
) -> str:
    if query_format != 'infer':
        return query_format
    ext = _os.path.splitext(query)[-1]
    return {
        '.phd':'phd',
        '.ab1':'abi',
        '.fasta':'fasta',
        '.fas':'fasta',
        '.fa':'fasta',
    }.get(ext, 'Seq')
    