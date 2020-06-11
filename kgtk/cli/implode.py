"""Copy records from the first KGTK file to the output file,
building one column (usually node2) from discrete subfields.

TODO: Need KgtkWriterOptions
"""

from argparse import _MutuallyExclusiveGroup, Namespace, SUPPRESS
from pathlib import Path
import sys
import typing

from kgtk.kgtkformat import KgtkFormat
from kgtk.cli_argparse import KGTKArgumentParser
from kgtk.io.kgtkreader import KgtkReader, KgtkReaderOptions
from kgtk.io.kgtkwriter import KgtkWriter
from kgtk.reshape.kgtkimplode import KgtkImplode
from kgtk.utils.argparsehelpers import optional_bool
from kgtk.value.kgtkvalue import KgtkValueFields
from kgtk.value.kgtkvalueoptions import KgtkValueOptions

def parser():
    return {
        'help': 'Copy a KGTK file, building one column (usualy node2) from seperate columns for each subfield.',
        'description': 'Copy a KGTK file, building one column (usually node2) from seperate columns for each subfield. ' +
        '\n\nStrings may include language qualified strings, and quantities may include numbers. ' +
        '\n\nDate and times subfields and symbol subfields may be optionally quoted. Triple quotes may be used where quotes are accepted. ' +
        '\n\nAdditional options are shown in expert help.\nkgtk --expert expand --help'
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

    parser.add_argument(      "input_kgtk_file", nargs="?", type=Path, default="-",
                              help="The KGTK file to filter. May be omitted or '-' for stdin (default=%(default)s).")

    parser.add_argument("-o", "--output-file", dest="output_kgtk_file", help="The KGTK file to write (default=%(default)s).", type=Path, default="-")

    parser.add_argument(      "--reject-file", dest="reject_kgtk_file", help="The KGTK file into which to write rejected records (default=%(default)s).",
                              type=Path, default=None)

    parser.add_argument(      "--column", dest="column_name", help="The name of the column to explode. (default=%(default)s).", default=KgtkFormat.NODE2)

    parser.add_argument(      "--prefix", dest="prefix", help="The prefix for exploded column names. (default=%(default)s).",
                              default=KgtkFormat.NODE2 + ";" + KgtkFormat.KGTK_NAMESPACE)

    parser.add_argument(      "--types", dest="type_names", nargs='*',
                               help="The KGTK data types for which fields should be imploded. (default=%(default)s).",
                               choices=KgtkFormat.DataType.choices(),
                               default=KgtkFormat.DataType.choices())

    parser.add_argument(      "--without", dest="without_fields", nargs='*',
                               help="The KGTK fields to do without. (default=%(default)s).",
                               choices=KgtkValueFields.OPTIONAL_DEFAULT_FIELD_NAMES,
                               default=None)

    parser.add_argument(      "--overwrite", dest="overwrite_column",
                              help="Indicate that it is OK to overwrite an existing imploded column. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--validate", dest="validate",
                              help="Validate imploded values. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--escape-pipes", dest="escape_pipes",
                              help="When true, pipe characters (|) need to be escaped (\\|) per KGTK file format. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--quantities-include-numbers", dest="quantities_include_numbers",
                              help="When true, numbers are acceptable quantities. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--general-strings", dest="general_strings",
                              help="When true, strings may include language qualified strings. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--remove-prefixed-columns", dest="remove_prefixed_columns",
                              help="When true, remove all columns beginning with the prefix from the output file. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    parser.add_argument(      "--ignore-unselected-types", dest="ignore_unselected_types",
                              help="When true, input records with valid but unselected data types will be passed through to output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--retain-unselected-types", dest="retain_unselected_types",
                              help="When true, input records with valid but unselected data types will be retain existing data on output. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=True)

    parser.add_argument(      "--show-data-types", dest="show_data_types",
                              help="Print the list of data types and exit. (default=%(default)s).",
                              type=optional_bool, nargs='?', const=True, default=False)

    KgtkReader.add_debug_arguments(parser, expert=_expert)
    KgtkReaderOptions.add_arguments(parser, mode_options=True, expert=_expert)
    KgtkValueOptions.add_arguments(parser, expert=_expert)

def run(input_kgtk_file: Path,
        output_kgtk_file: Path,
        reject_kgtk_file: typing.Optional[Path],
        column_name: str,
        prefix: str,
        type_names: typing.List[str],
        without_fields: typing.Optional[typing.List[str]],
        overwrite_column: bool,
        validate: bool,
        escape_pipes: bool,
        quantities_include_numbers: bool,
        general_strings: bool,
        remove_prefixed_columns: bool,
        ignore_unselected_types: bool,
        retain_unselected_types: bool,
        show_data_types: bool,
        
        errors_to_stdout: bool = False,
        errors_to_stderr: bool = True,
        show_options: bool = False,
        verbose: bool = False,
        very_verbose: bool = False,

        **kwargs # Whatever KgtkFileOptions and KgtkValueOptions want.
)->int:
    # import modules locally
    from kgtk.exceptions import KGTKException

    # Select where to send error messages, defaulting to stderr.
    error_file: typing.TextIO = sys.stdout if errors_to_stdout else sys.stderr

    # Build the option structures.
    reader_options: KgtkReaderOptions = KgtkReaderOptions.from_dict(kwargs)
    value_options: KgtkValueOptions = KgtkValueOptions.from_dict(kwargs)

    # Show the final option structures for debugging and documentation.
    if show_options:
        print("input: %s" % (str(input_kgtk_file) if input_kgtk_file is not None else "-"), file=error_file)
        print("--column %s" % column_name, file=error_file, flush=True)
        print("--prefix %s" % prefix, file=error_file, flush=True)
        print("--overwrite %s" % str(overwrite_column), file=error_file, flush=True)
        print("--validate %s" % str(validate), file=error_file, flush=True)
        print("--escape-pipes %s" % str(escape_pipes), file=error_file, flush=True)
        print("--quantities-include-numbers %s" % str(quantities_include_numbers), file=error_file, flush=True)
        print("--general-strings %s" % str(general_strings), file=error_file, flush=True)
        print("--remove-prefixed-columns %s" % str(remove_prefixed_columns), file=error_file, flush=True)
        print("--ignore-unselected-types %s" % str(ignore_unselected_types), file=error_file, flush=True)
        print("--retain-unselected-types %s" % str(retain_unselected_types), file=error_file, flush=True)
        if type_names is not None:
            print("--types %s" % " ".join(type_names), file=error_file, flush=True)
        if without_fields is not None:
            print("--without %s" % " ".join(without_fields), file=error_file, flush=True)
        print("--output-file=%s" % (str(output_kgtk_file) if output_kgtk_file is not None else "-"), file=error_file, flush=True)
        if reject_kgtk_file is not None:
            print("--reject-file=%s" % str(reject_kgtk_file), file=error_file, flush=True)
        print("--show-data-types %s" % str(show_data_types), file=error_file, flush=True)
        reader_options.show(out=error_file)
        value_options.show(out=error_file)
        print("=======", file=error_file, flush=True)
    if show_data_types:
        data_type: str
        for data_type in KgtkFormat.DataType.choices():
            print("%s" % data_type, file=error_file, flush=True)
        return 0

    wf: typing.List[str] = without_fields if without_fields is not None else list()

    try:
        ex: KgtkImplode = KgtkImplode(
            input_file_path=input_kgtk_file,
            output_file_path=output_kgtk_file,
            reject_file_path=reject_kgtk_file,
            column_name=column_name,
            prefix=prefix,
            type_names=type_names,
            without_fields=wf,
            overwrite_column=overwrite_column,
            validate=validate,
            escape_pipes=escape_pipes,
            quantities_include_numbers=quantities_include_numbers,
            general_strings=general_strings,
            remove_prefixed_columns=remove_prefixed_columns,
            ignore_unselected_types=ignore_unselected_types,
            retain_unselected_types=retain_unselected_types,
            reader_options=reader_options,
            value_options=value_options,
            error_file=error_file,
            verbose=verbose,
            very_verbose=very_verbose)

        ex.process()

        return 0

    except SystemExit as e:
        raise KGTKException("Exit requested")
    except Exception as e:
        raise KGTKException(str(e))

