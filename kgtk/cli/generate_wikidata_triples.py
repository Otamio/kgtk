"""
Generate wikidata triples from two edge files:
1. A statement and qualifier edge file that contains an edge id, node1, label, and node2
2. A kgtk file that contains the mapping information from property identifier to its datatype

"""

def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        "help": "Generates wikidata triples from kgtk file",
        "description": "Generating Wikidata triples.",
    }
def str2bool(v):
    import argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
        prop_file: str, labelSet: str, aliasSet: str, descriptionSet: str, n: str, dest: Any  --output-n-lines --generate-truthy
    """
    parser.add_argument(
        "-lp",
        "--label-property",
        action="store",
        type=str,
        help="property identifiers which will create labels, separated by comma','.",
        dest="labels",
    )
    parser.add_argument(
        "-ap",
        "--alias-property",
        action="store",
        type=str,
        help="alias identifiers which will create labels, separated by comma','.",
        dest="aliases",
    )
    parser.add_argument(
        "-dp",
        "--description-property",
        action="store",
        type=str,
        help="description identifiers which will create labels, separated by comma','.",
        dest="descriptions",
    )
    parser.add_argument(
        "-pf",
        "--property-types",
        action="store",
        type=str,
        help="path to the file which contains the property datatype mapping in kgtk format.",
        dest="prop_file",
    )
    parser.add_argument(
        "-n",
        "--output-n-lines",
        action="store",
        type=int,
        help="output triples approximately every {n} lines of reading stdin.",
        dest="n",
    )
    parser.add_argument(
        "-gt",
        "--generate-truthy",
        action="store",
        type=str2bool,
        help="the default is to not generate truthy triples. Specify this option to generate truthy triples. NOTIMPLEMENTED",
        dest="truthy",
    )
    parser.add_argument(
        "-ig",
        "--ignore",
        action="store",
        type=str2bool,
        help="if set to yes, ignore various kinds of exceptions and mistakes and log them to a log file with line number in input file, rather than stopping. logging",
        dest="ignore",
    )
    parser.add_argument(
        "-gz",
        "--use-gz",
        action="store",
        type=str2bool,
        help="if set to yes, read from compressed gz file",
        dest="use_gz",
    )
    parser.add_argument(
        "-lbl",
        "--line-by-line",
        action="store",
        type=str2bool,
        help="if set to yes, read from standard input line by line, otherwise loads whole file into memory",
        dest="line_by_line",
    )


def run(
    labels: str,
    aliases: str,
    descriptions: str,
    prop_file: str,
    n: int,
    truthy: bool,
    ignore: bool,
    use_gz: bool,
    line_by_line: bool,
):
    # import modules locally
    import gzip
    from kgtk.triple_generator import TripleGenerator
    import sys
    generator = TripleGenerator(
        prop_file=prop_file,
        label_set=labels,
        alias_set=aliases,
        description_set=descriptions,
        n=n,
        ignore=ignore,
        truthy=truthy
    )
    # process stdin
    if use_gz:
        fp = gzip.open(sys.stdin.buffer, 'rt')
    else:
        fp = sys.stdin
    if line_by_line:
        print("#line-by-line")
        num_line = 1
        while True:
            edge = fp.readline()
            if not edge:
                break
            if edge.startswith("#") or num_line == 1: # TODO First line omit
                num_line += 1
                continue
            else:
                generator.entry_point(num_line, edge)
                num_line += 1
    else:
        # not line by line
        print("#not line-by-line")
        for num, edge in enumerate(fp.readlines()):
            if edge.startswith("#") or num == 0:
                continue
            else:
                generator.entry_point(num+1,edge)
    generator.finalize()

# testing profiling locally with direct call

if __name__ == "__main__":
    import gzip
    from kgtk.triple_generator import TripleGenerator
    import sys
    with open("/tmp/gwt.log","w") as dest_fp:
        generator = TripleGenerator(
            prop_file="/Users/rongpeng/Documents/ISI/Covid19/covid_data/v1.3/heng_props.tsv",
            label_set="label",
            alias_set="aliases",
            description_set="descriptions",
            n=10000,
            ignore=True,
            truthy=True,
            dest_fp = dest_fp
        )   
        with open("/Users/rongpeng/Documents/ISI/Covid19/covid_data/v1.3/kgtk_sample_sorted.tsv","r") as fp:
            for num, edge in enumerate(fp.readlines()):
                if edge.startswith("#") or num == 0:
                    continue
                else:
                    generator.entry_point(num+1,edge)
            generator.finalize() 