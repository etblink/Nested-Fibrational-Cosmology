from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Scope:
    regime: str
    domain: str
    certificate_scope: str
    inherited_constraints: List[str] = field(default_factory=list)
    continuum_license: Optional[str] = None
    promotion_ceiling: Optional[str] = None

@dataclass
class Discharge:
    target: str
    kind: str
    basis: List[str]
    scope_relation: str
    transfer_required: bool = False
    transfer_basis: List[str] = field(default_factory=list)

@dataclass
class Claim:
    id: str
    book: str
    track: str
    kind: str
    number: str
    title: str
    declared_status: str
    scope: Scope
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    discharges: List[Discharge] = field(default_factory=list)
    supersedes: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    body_file: Optional[str] = None
    proof_file: Optional[str] = None
    audit: Dict[str, Any] = field(default_factory=dict)
