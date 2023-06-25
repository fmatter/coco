from clld.web.util.htmllib import HTML
from Bio import Phylo
import copy
from clld.web.util.helpers import link
from clld.db.meta import DBSession
from clld.db.models.common import Language, Parameter, Value
from coco import models
from io import StringIO



def iter_tree(clade):
    if len(clade.get_terminals()) > 1:
        yield (clade.name, False)
        for child in clade.clades:
            for x in iter_tree(child):
                yield x
    else:
        yield (clade.name, True)


def filtered_tree(tree, data):
    new_tree = copy.deepcopy(tree)
    internals = [x.name for x in new_tree.get_nonterminals()]
    for item in new_tree.get_terminals():
        if item.name not in data:
            # print("pruning", item.name)
            new_tree.prune(item)
    for item in new_tree.get_terminals():
        if not item.clades and item.name in internals:
            new_tree.prune(item)
    return new_tree


def build_ul(request, coghits, clade):
    lis = []
    for child in clade.clades:
        if child == clade:
            continue
        if child.name in coghits:
            lis.append(
                HTML.li(
                    link(request, coghits[child.name].counterpart.language),
                    ": ",
                    HTML.b(link(request, coghits[child.name].counterpart)),
                    class_="tree",
                )
            )
        else:
            print(child.name)
            lg = list(DBSession.query(Language).filter(Language.id == child.name))
            print(lg)
            if len(lg) > 0:
                lis.append(HTML.li(link(request, lg[0]), ": ?", class_="tree"))
            else:
                lis.append(HTML.li(child.name, ": ?", class_="tree"))                
        if not child.is_terminal():
            lis.append(build_ul(request, coghits, child))
    return HTML.ul(*lis, class_="tree")


def build_tree(request, cogset):
    trees = list(DBSession.query(models.Tree))
    if len(trees) > 0:
        ref_tree = trees[0]
        tree = Phylo.read(
    StringIO(ref_tree.newick),
    format="newick",
)

        coghits = {x.counterpart.language.id: x for x in cogset.reflexes}
        good_leafs = []
        for name, isleaf in iter_tree(tree.root):
            if name in coghits:
                good_leafs.append(name)
        new_tree = filtered_tree(tree, good_leafs)
        return build_ul(request, coghits, new_tree.root)
    return HTML.div("No trees in database.")
