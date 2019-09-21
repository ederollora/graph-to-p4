
FIRST_LINE = "/* -*- P4_16 -*- */"


OPENING_PT = "("
CLOSING_PT = ")"
OPENING_BLOCK = "{"
CLOSING_BLOCK = "}"

SLASH = "/"
COMMA = ","
DOT = "."
SPACE = " "
NEWLINE = "\n"
INDENT = (4 * SPACE)
EMPTY_STRING = ""

EMPTY = True


P4_EXTENSION = ".p4"

INCLUDE = "include"
DEFINEs = "defines"

OUTPUT_DIR = "output"

DEFAULT_LIBRARY = "#include <{0}.p4>"
INCLUDE_FILE = "#include \"{0}{1}\""

# HEADERS

HEADER_INIT = "header {0}_t"
HEADER_LINE = "bit<{0}> {1} {2};"
HEADERS_DEF = "struct {0}"


# BLOCKS and PARAMETERS

START = "start"
PARSER = "parser"
CONTROL = "control"
HEADERS = "headers"
DEPARSER = "deparser"
DEFINES = "defines"
CHECKSUM = "checksum"
EXTERN = "extern"
MAIN = "main"
ACCEPT = "accept"


PACKET_IN = "packet_in"
PACKET_NAME = "packet"

OUT = "out"
HEADERS_TYPE = "headers"
HEADER_NAME = "hdr"

INOUT = "inout"
METADATA_TYPE = "metadata"
METADATA_NAME = "meta"

SMETADATA_TYPE = "standard_metadata_t"
SMETADATA_NAME = "standard_metadata"

STATE_INIT = "state {0} {{"
EXTRACT_LINE = "packet.extract({0}.{1});"
TRANSITION_INIT = "transition select({0}.{1}.{2}) {{"
TRANSITION_LINE = "{0}: {1};"
TRANSITION_DIRECT = "transition {0};"
TRANSITION_ACCEPT = "transition accept;"
TRANS_DEFAULT = "default: accept;"

EMPTY_METADATA = "struct metadata {\n /* empty */ \n}"

APPLY = "apply"

DEFINE_ENTRY = "#define {0} {1}"
CONSTANT_ENTRY = "const bit<{0}> {1} = {2};"
TYPEDEF_ENTRY = "typedef bit<{0}> {1};"

SWITCH_DEF = "{0} ({1}) {2};"
CONTROL_BLOCK_DEF = "{0} {1} ({2})"
PARAMETER_2 = "{0} {1}"
PARAMETER_3 = "{0} {1} {2}"
EMIT_STMT = "{0}.emit({1}.{2});"
SWITCH_DEF = "{0}({1}{2}) {3};"
# DEPARSER_STMT = INDENT + APPLY + SPACE + (2*OPENING_BLOCK) + NEWLINE + " {0} " + INDENT + (2*CLOSING_BLOCK)
DEPARSER_STMT = INDENT + "apply {{\n{0}"+ INDENT +"}}"

MAU = "mau"

POSITION_0 = 0
POSITION_1 = 1
FORMAT_PARAMETER_0 = "{0}"


BINARY_VALUES = ["binary", "bin", "b"]
OCTAL_VALUES = ["octal", "oct", "o"]
HEXADECIMAL_VALUES = ["hexadecimal", "hex", "h"]
DECIMAL_VALUES = ["decimal", "dec", "d"]


