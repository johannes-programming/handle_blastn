import dataclasses as _dc
import typing as _typing
import xml.dom.minidom as _minidom

@_dc.dataclass(frozen=True)
class Summary:
    query_id: str
    subject_id: str
    bit_score: float
    evalue: float
    def __post_init__(self) -> None:
        cls = type(self)
        ann = cls.__annotations__
        for n, t in ann.items():
            v = getattr(self, n)
            if type(v) is not t:
                raise TypeError(f"{v} is not of the type {t}.")
    @classmethod
    def from_text(cls, text) -> _typing.Self:
        data = _minidom.parseString(text)
        kwargs = dict()
        kwargs['query_id'] = _get(
            'BlastOutput', 
            'BlastOutput_iterations', 
            'Iteration', 
            'Iteration_query-def',
            data=data,
        )
        kwargs['subject_id'] = _get(
            'BlastOutput', 
            'BlastOutput_iterations', 
            'Iteration', 
            'Iteration_hits', 
            'Hit', 
            'Hit_id',
            data=data,
        )
        kwargs['bit_score'] = _get(
            'BlastOutput', 
            'BlastOutput_iterations', 
            'Iteration', 
            'Iteration_hits', 
            'Hit', 
            'Hsp', 
            'Hsp_bit-score',
            data=data,
        )
        kwargs['evalue'] = _get(
            'BlastOutput', 
            'BlastOutput_iterations', 
            'Iteration', 
            'Iteration_hits', 
            'Hit', 
            'Hsp', 
            'Hsp_evalue',
            data=data, 
        )
        ann = cls.__annotations__
        for n, t in ann.items():
            if t is str:
                continue
            kwargs[n] = t(kwargs[n])            
        return cls(**kwargs)
    @classmethod
    def from_file(cls, file) -> _typing.Self:
        with open(file, 'r') as s:
            text = s.read()
        return cls.from_text(text)


def _get(*keys, data) -> _typing.Any:
    if data is None:
        return None
    ans = data
    try:
        for key in keys:
            ans = ans.getElementsByTagName(key)[0]
        ans = ans.childNodes[0]
    except ValueError:
        return float('nan')
    except IndexError:
        return float('nan')
    ans = ans.nodeValue
    if type(ans) is not str:
        raise TypeError
    return ans 
