"""
Join two KGTK edge files or two KGTK node files.

TODO: Need KgtkWriterOptions
"""

from argparse import Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.join.kgtkjoiner import KgtkJoiner
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Join two KGTK files',
        'description': 'Join two KGTK edge files or two KGTK node files. Two passes may be needed, stdin may be forbidden.'
    }


def add_arguments_extended(parser: KGTKArgumentParser, parsed_shared_args: Namespace):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """

    _expert: bool = parsed_shared_args._expert

    # This helper function makes it easy to suppress options from
    # The help message.  The options are still there, and initialize
    # what they need to initialize.
    def h(msg: str)->str:
        if _expert:
            return msg
        else:
            return SUPPRESS

    parser.add_argument(      "left_file_path", help="The left-side KGTK file to join (no default).", type=Path, default=None)

    parser.add_argument(      "right_file_path", help="The right-side KGTK file to join (no default).", type=Path, default=None)

    parser.add_argument(      "--join-on-label", dest="join_on_label",
                              help="If both input files are edge files, include the label column in the join (default=%(default)s).",
                              action='store_true')

    parser.add_argument(      "--join-on-node2", dest="join_on_node2",
                              help="If both input files are edge files, include the node2 column in the join (default=%(default)s).",
                              action='store_true')
    
    parser.add_argument(      "--left-file-join-columns", dest="left_join_columns", help="Left file join columns (default=None).", nargs='+')

    parser.add_argument(      "--left-join", dest="left_join", help="Perform a left outer join (default=%(default)s).", action='store_true')

    parser.add_argument("-o", "--output-file", dest="output_file_path", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--prefix", dest="prefix",
                              help="An optional prefix applied to right file column names in the output file (default=None).")
    
    parser.add_argument(      "--right-file-join-columns", dest="right_join_columns", help="Right file join columns (default=None).", nargs='+')
    
    parser.add_argument(      "--right-join", dest="right_join", help="Perform a right outer join (default=%(default)s).", action='store_true')

    # This argument is retained for compatability with earlier versions of this command.
    parser.add_argument(      "--error-limit", dest="error_limit",
                              help=h("The maximum number of errors per input fule (default=%(default)s)"),
                              default=KgtkReaderOptions.ERROR_LIMIT_DEFAULT)

    parser.add_argument(      "--field-separator", dest="field_separator",
                              help=h("Separator for multifield keys (default=%(default)s)")
                              , default=KgtkJoiner.FIELD_SEPARATOR_DEFAULT)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="left", expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, who="right", expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(left_file_path: typing.Optional[Path],
        right_file_path: typing.Optional[Path],
        left_join: bool,
        right_join: bool,
        join_on_label: bool,
        join_on_node2: bool,
        left_join_columns: typing.Optional[typing.List[str]],
        right_join_columns: typing.Optional[typing.List[str]],
        output_file_path: Path,
        prefix: typing.Optional[str] = None,

        field_separator: str = KgtkJoiner.FIELD_SEPARATOR_DEFAULT,

        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException


    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    if not right_join:
        if left_file_path is None or str(left_file_path) == "-":
            print("The left file may not be stdin when an inner join or left join is requested.", file=error_file, flush=True)
            return 1

    if not left_join:
        if right_file_path is None or str(right_file_path) == "-":
            print("The right file may not be stdin when an inner join or right join is requested.", file=error_file, flush=True)
            return 1

    if (left_file_path is None or str(left_file_path) == "-") and (right_file_path is None or str(right_file_path) == "-"):
        print("The left and right files may not both be stdin.", file=error_file, flush=True)
        return 1

    if left_file_path is None:
        left_file_path = Path("-")
        
    if right_file_path is None:
        right_file_path = Path("-")
        

    # Build the option structures.
    left_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="left", fallback=True)
    right_reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs, who="right", fallback=True)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    try:
        kr: KgtkJoiner = KgtkJoiner(
            left_file_path=left_file_path,
            right_file_path=right_file_path,
            output_path=output_file_path,
            left_join=left_join,
            right_join=right_join,
            join_on_label=join_on_label,
            join_on_node2=join_on_node2,
            left_join_columns=left_join_columns,
            right_join_columns=right_join_columns,
            prefix=prefix,
            field_separator=field_separator,
            left_reader_options=left_reader_options,
            right_reader_options=right_reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose,
        )
        
        kr.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

