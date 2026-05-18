"""Transforms for resolving references."""

from _typeshed import Incomplete
from collections.abc import Iterable
from typing import ClassVar, Final, overload

from docutils import nodes
from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"

class PropagateTargets(Transform):
    """
    Propagate empty internal targets to the next element.

    Given the following nodes::

        <target ids="internal1" names="internal1">
        <target anonymous="1" ids="id1">
        <target ids="internal2" names="internal2">
        <paragraph>
            This is a test.

    `PropagateTargets` propagates the ids and names of the internal
    targets preceding the paragraph to the paragraph itself::

        <target refid="internal1">
        <target anonymous="1" refid="id1">
        <target refid="internal2">
        <paragraph ids="internal2 id1 internal1" names="internal2 internal1">
            This is a test.
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class AnonymousHyperlinks(Transform):
    """
    Link anonymous references to targets.  Given::

        <paragraph>
            <reference anonymous="1">
                internal
            <reference anonymous="1">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">

    Corresponding references are linked via "refid" or resolved via "refuri"::

        <paragraph>
            <reference anonymous="1" refid="id1">
                text
            <reference anonymous="1" refuri="http://external">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class IndirectHyperlinks(Transform):
    """
    a) Indirect external references::

           <paragraph>
               <reference refname="indirect-external">
                   indirect external
           <target ids="id1" names="direct-external"
               refuri="http://indirect">
           <target ids="id2" names="indirect-external"
               refname="direct-external">

       The "refuri" attribute is migrated back to all indirect targets
       from the final direct target (i.e. a target not referring to
       another indirect target)::

           <paragraph>
               <reference refname="indirect-external">
                   indirect external
           <target ids="id1" names="direct-external"
               refuri="http://indirect">
           <target ids="id2" names="indirect-external"
               refuri="http://indirect">

       Once the attribute is migrated, the preexisting "refname" attribute
       is dropped.

    b) Indirect internal references::

           <target ids="id1" names="final-target">
           <paragraph>
               <reference refname="indirect-internal">
                   indirect internal
           <target ids="id2" names="indirect-internal-2"
               refname="final target">
           <target ids="id3" names="indirect-internal"
               refname="indirect-internal-2">

       Targets which indirectly refer to an internal target become one-hop
       indirect (their "refid" attributes are directly set to the internal
       target's "id"). References which indirectly refer to an internal
       target become direct internal references::

           <target ids="id1" names="final-target">
           <paragraph>
               <reference refid="id1">
                   indirect internal
           <target ids="id2" names="indirect-internal-2" refid="id1">
           <target ids="id3" names="indirect-internal" refid="id1">
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...
    def resolve_indirect_target(self, target: nodes.Element) -> None: ...
    def nonexistent_indirect_target(self, target: nodes.Element) -> None: ...
    def circular_indirect_reference(self, target: nodes.Element) -> None: ...
    def indirect_target_error(self, target: nodes.Element, explanation) -> None: ...
    def resolve_indirect_references(self, target: nodes.Element) -> None: ...

class ExternalTargets(Transform):
    """
    Given::

        <paragraph>
            <reference refname="direct-external">
                direct external
        <target ids="id1" names="direct-external" refuri="http://direct">

    The "refname" attribute is replaced by the direct "refuri" attribute::

        <paragraph>
            <reference refuri="http://direct">
                direct external
        <target ids="id1" names="direct-external" refuri="http://direct">
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class InternalTargets(Transform):
    default_priority: ClassVar[int]
    def apply(self) -> None: ...
    def resolve_reference_ids(self, target: nodes.Element) -> None:
        """
        Given::

            <paragraph>
                <reference refname="direct-internal">
                    direct internal
            <target ids="id1" names="direct-internal">

        The "refname" attribute is replaced by "refid" linking to the target's
        "id"::

            <paragraph>
                <reference refid="id1">
                    direct internal
            <target ids="id1" names="direct-internal">
        """
        ...

class Footnotes(Transform):
    """
    Assign numbers to autonumbered footnotes, and resolve links to footnotes,
    citations, and their references.

    Given the following ``document`` as input::

        <document>
            <paragraph>
                A labeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id1" refname="footnote">
            <paragraph>
                An unlabeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id2">
            <footnote auto="1" ids="id3">
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" ids="footnote" names="footnote">
                <paragraph>
                    Labeled autonumbered footnote.

    Auto-numbered footnotes have attribute ``auto="1"`` and no label.
    Auto-numbered footnote_references have no reference text (they're
    empty elements). When resolving the numbering, a ``label`` element
    is added to the beginning of the ``footnote``, and reference text
    to the ``footnote_reference``.

    The transformed result will be::

        <document>
            <paragraph>
                A labeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id1" refid="footnote">
                    2
            <paragraph>
                An unlabeled autonumbered footnote reference:
                <footnote_reference auto="1" ids="id2" refid="id3">
                    1
            <footnote auto="1" ids="id3" backrefs="id2">
                <label>
                    1
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" ids="footnote" names="footnote" backrefs="id1">
                <label>
                    2
                <paragraph>
                    Labeled autonumbered footnote.

    Note that the footnotes are not in the same order as the references.

    The labels and reference text are added to the auto-numbered ``footnote``
    and ``footnote_reference`` elements.  Footnote elements are backlinked to
    their references via "refids" attributes.  References are assigned "id"
    and "refid" attributes.

    After adding labels and reference text, the "auto" attributes can be
    ignored.
    """
    default_priority: ClassVar[int]
    autofootnote_labels: list[str] | None
    symbols: ClassVar[list[str]]
    def apply(self) -> None: ...
    def number_footnotes(self, startnum: int) -> int:
        """
        Assign numbers to autonumbered footnotes.

        For labeled autonumbered footnotes, copy the number over to
        corresponding footnote references.
        """
        ...
    def number_footnote_references(self, startnum: int) -> None:
        """Assign numbers to autonumbered footnote references."""
        ...
    def symbolize_footnotes(self) -> None:
        """Add symbols indexes to "[*]"-style footnotes and references."""
        ...
    def resolve_footnotes_and_citations(self) -> None:
        """
        Link manually-labeled footnotes and citations to/from their
        references.
        """
        ...

    @overload
    def resolve_references(self, note: nodes.footnote, reflist: Iterable[nodes.footnote_reference]) -> None: ...
    @overload
    def resolve_references(self, note: nodes.citation, reflist: Iterable[nodes.citation_reference]) -> None: ...
    @overload
    def resolve_references(self, note: nodes.title, reflist: Iterable[nodes.title_reference]) -> None: ...

class CircularSubstitutionDefinitionError(Exception): ...

class Substitutions(Transform):
    """
    Given the following ``document`` as input::

        <document>
            <paragraph>
                The
                <substitution_reference refname="biohazard">
                    biohazard
                 symbol is deservedly scary-looking.
            <substitution_definition names="biohazard">
                <image alt="biohazard" uri="biohazard.png">

    The ``substitution_reference`` will simply be replaced by the
    contents of the corresponding ``substitution_definition``.

    The transformed result will be::

        <document>
            <paragraph>
                The
                <image alt="biohazard" uri="biohazard.png">
                 symbol is deservedly scary-looking.
            <substitution_definition names="biohazard">
                <image alt="biohazard" uri="biohazard.png">
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class TargetNotes(Transform):
    """
    Creates a footnote for each external target in the text, and corresponding
    footnote references after each reference.
    """
    default_priority: ClassVar[int]
    classes: Incomplete
    def __init__(self, document: nodes.document, startnode: nodes.Node) -> None: ...
    def apply(self) -> None: ...
    def make_target_footnote(self, refuri: str, refs: list[Incomplete], notes: dict[Incomplete, Incomplete]): ...

class CitationReferences(Transform):
    """
    Resolve <citation_references>.

    The 'use_bibtex'__ configuration setting indicates that citation entries
    are fetched from a BibTeX database by the backend (LaTeX).

    __ https://docutils.sourceforge.io/docs/user/config.html#use-bibtex
    """
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class DanglingReferences(Transform):
    'Check for dangling references (incl. footnote & citation) and for\nunreferenced targets.\n\nProvisional : pending deprecation\n  Docutils readers will add separate transforms for resolving\n  refnames to refids and for reporting unresolved references\n  instead of this transform (to make space for reference-resolving\n  transforms added by extensions or applications) in Docutils\xa01.0.\n  This transform will be removed in Docutils\xa02.0.'
    default_priority: ClassVar[int]
    def apply(self) -> None: ...

class DanglingReferencesVisitor(nodes.SparseNodeVisitor):
    'Provisional : pending deprecation\n\nThis auxiliary class is used by the `DanglingReferences` transform\nwhich will no longer be used in Docutils\xa01.0.\nIt will be removed in Docutils\xa02.0.'
    document: nodes.document
    def __init__(self, document: nodes.document, unknown_reference_resolvers) -> None: ...
    def unknown_visit(self, node: nodes.Node) -> None: ...
    def visit_reference(self, node: nodes.reference) -> None: ...
    def visit_footnote_reference(self, node: nodes.footnote_reference) -> None: ...
    def visit_citation_reference(self, node: nodes.citation_reference) -> None: ...
