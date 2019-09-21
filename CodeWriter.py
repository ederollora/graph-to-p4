from Constants import *
import os


class CodeWriter:

    def __init__(self):
        self.name = ''
        self.fields = []
        self.typedefs = []
        self.defines = []
        self.consts = []
        self.str_tr_const = ""

    def write_libraries(self, arch, main_file):
        for lib in arch.libraries:
            main_file.write(DEFAULT_LIBRARY.format(lib) + NEWLINE)

    def write_includes(self, arch, args, main_file):
        lines_to_write = ""

        types = ""

        if args.separate_files:
            types = args.separate_files.split(",")

        path = ""

        if args.include_dir:
            path += INCLUDE + SLASH  # include/

        if DEFINES in types:
            lines_to_write += INCLUDE_FILE.format(path + DEFINES, P4_EXTENSION) + NEWLINE
        if HEADERS in types:
            lines_to_write += INCLUDE_FILE.format(path + arch.headers["filename"], P4_EXTENSION) + NEWLINE

        for k, v in arch.prog_blocks.items():
            if (v.type == CONTROL and v.abstraction == MAU) and v.type in types:
                lines_to_write += INCLUDE_FILE.format(path + v.filename, P4_EXTENSION) + NEWLINE
            elif v.abstraction == DEPARSER and v.abstraction in types:
                lines_to_write += INCLUDE_FILE.format(path + v.filename, P4_EXTENSION) + NEWLINE
            elif v.type == CHECKSUM and v.type in types:
                lines_to_write += INCLUDE_FILE.format(path + v.filename, P4_EXTENSION) + NEWLINE
            elif v.type == PARSER and v.type in types:
                lines_to_write += INCLUDE_FILE.format(path + v.filename, P4_EXTENSION) + NEWLINE

        main_file.write(lines_to_write)

    def write_dct(self, arch, args, main_path):

        lines_to_write = ""

        path = self.decide_path(DEFINES, args, main_path)

        for name, define in arch.defines.items():
            lines_to_write += DEFINE_ENTRY.format(define.name, str(define.value)) + NEWLINE

        lines_to_write += (NEWLINE)

        for name, constant in arch.constants.items():
            lines_to_write += CONSTANT_ENTRY.format(str(constant.bitwidth), constant.name, constant.value) + NEWLINE

        lines_to_write += (NEWLINE)

        lines_to_write += self.str_tr_const

        lines_to_write += (NEWLINE)

        for name, typedef in arch.typedefs.items():
            lines_to_write += TYPEDEF_ENTRY.format(str(typedef.bitwidth), typedef.name) + NEWLINE

        lines_to_write += (2 * NEWLINE)

        with open(path, 'a') as defines_file:
            defines_file.write(lines_to_write)

    def write_a_header(self, header, hname_length, path):
        with open(path, 'a') as header_file:
            header_file.write((HEADER_INIT +
                              (2 * OPENING_BLOCK) +
                              NEWLINE).format(header.name))
            for field in header.fields:
                header_file.write(
                    (INDENT + HEADER_LINE + NEWLINE).format(
                        field.bit_width,
                        ((header.longest_bw - len(str(field.bit_width))) * SPACE) + (2 * SPACE),
                        field.name)
                )
            header_file.write(CLOSING_BLOCK + (2 * NEWLINE))

        return ("{0}_t{1}{0};" + NEWLINE) \
            .format(header.name, ((hname_length - len(header.name)) * SPACE) + (2 * SPACE))

    def write_headers(self, headers, hname_length, arch, args, main_path):

        lines_to_write = ""

        path = self.decide_path(HEADERS, args, main_path)

        header_compilation = HEADERS_DEF.format(arch.headers["name"]) + OPENING_BLOCK + NEWLINE

        for header_name, header in sorted(headers.items(), key=lambda h: h[1].stage):
            header_compilation += (4 * SPACE) + self.write_a_header(header, hname_length, path)

        header_compilation += CLOSING_BLOCK + 2*NEWLINE

        with open(path, 'a') as header_file:
            header_file.write(EMPTY_METADATA + 3*NEWLINE)
            header_file.write(header_compilation)

    def write_parser(self, lines, args, main_path):

        path = self.decide_path(PARSER, args, main_path)

        with open(path, 'a') as parser_file:
            parser_file.write(lines)

    def write_control_block(self, block, arch, args, type, empty):

        path = args.output_path

        if type in args.separate_files.split(","):
            path += INCLUDE + SLASH + block["filename"] + P4_EXTENSION
        else:
            path += arch.main["filename"] + P4_EXTENSION

        lines_to_write = ""

        self.write_block_upper(block, path)

        if empty:
            lines_to_write += (INDENT) + APPLY + OPENING_BLOCK + SPACE + CLOSING_BLOCK \
                              + (2 * NEWLINE) + CLOSING_BLOCK + (2 * NEWLINE)

        with open(path, 'a') as file:
            file.write(lines_to_write)

    def write_deparser(self, headers, block, arch, args, type):

        path = args.output_path

        if type in args.separate_files.split(","):
            path += INCLUDE + SLASH + block.filename + P4_EXTENSION
        else:
            path += arch.main["filename"] + P4_EXTENSION

        lines_to_write = ""
        statements = ""

        self.write_block_upper(block, path)

        for header_name, header in sorted(headers.items(), key=lambda h: h[1].stage):
            statements += (2 * INDENT) + \
                              EMIT_STMT.format(
                                  block.parameters[POSITION_0].name,
                                  block.parameters[POSITION_1].name,
                                  header_name) + \
                              NEWLINE

        lines_to_write = DEPARSER_STMT.format(statements) + NEWLINE
        lines_to_write += CLOSING_BLOCK + (2*NEWLINE)

        with open(path, 'a') as file:
            file.write(lines_to_write)

    def switch_definition(self, arch, args, main_path):

        path = main_path

        lines_to_write = SWITCH_DEF.format(arch.switch_name, NEWLINE, FORMAT_PARAMETER_0, MAIN)

        pb_def = ""

        for idx, block_name in enumerate(arch.pipeline):

            pb_def += INDENT + block_name+OPENING_PT+CLOSING_PT

            if idx != (len(arch.pipeline) - 1):
                pb_def += COMMA

            pb_def += NEWLINE

        lines_to_write = lines_to_write.format(pb_def)

        with open(path, 'a') as main_file:
            main_file.write(lines_to_write)

    def write_P4(self, arch, args, graph):

        str_parsers = {}

        for block_name in arch.pipeline:
            block = arch.prog_blocks[block_name]
            if block.type == PARSER:
                str_parsers[block.name] = self.process_parser(graph.headers, graph.states, graph.transitions, block)

        self.process_transition_consts()

        op = args.output_path
        op = (op + SLASH) if not op.endswith(SLASH) else (op + EMPTY_STRING)

        path = op + arch.main["filename"] + P4_EXTENSION

        if not os.path.exists(op):
            os.makedirs(op)

        if args.include_dir and args.separate_files:
            inc_path =  op + INCLUDE + SLASH
            if not os.path.exists(inc_path):
                os.makedirs(inc_path)

        with open(path, 'a') as main_file:
            main_file.write(FIRST_LINE + 2*NEWLINE)

            # includes for core, arch ...
            self.write_libraries(arch, main_file)

            main_file.write(2 * NEWLINE)

            # include separate files for headers, parser, etc.
            self.write_includes(arch, args, main_file)

            main_file.write(NEWLINE)

        # write defines, constants typedefs in separate or main file
        self.write_dct(arch, args, path)

        self.write_headers(graph.headers, graph.longest_hname, arch, args, path)

        for block_name in arch.pipeline:
            block = arch.prog_blocks[block_name]
            if block.type == PARSER:
                self.write_parser(str_parsers[block.name], args, path)
            elif block.type == CONTROL and (block.abstraction == MAU or block.abstraction == EXTERN):
                # if control and match action unit
                self.write_control_block(block, arch, args, block.type, EMPTY)
            elif block.type == DEPARSER or block.abstraction == DEPARSER:
                self.write_deparser(graph.headers, block, arch, args, DEPARSER)

        self.switch_definition(arch, args, path)


    # UTILS

    def process_parser(self, headers, states, transitions, block):

        lines_to_write = self.process_block_upper(block)

        for state_id, state in sorted(states.items(), key=lambda s: s[1].stage):
            lines_to_write += self.process_a_parse_block(state, transitions, states, headers)

        lines_to_write += CLOSING_BLOCK + (2 * NEWLINE)

        return lines_to_write

    def process_a_parse_block(self, current_state, transitions, states, headers):

        FIRST = 0

        lines = ""

        # if an accept block then just return
        if current_state.name == 'accept':
            return lines

        # if a start block
        if (current_state.name == 'start'):
            lines += INDENT + STATE_INIT.format(current_state.parse_name) + NEWLINE
            parse_name = states[transitions[current_state.id][FIRST].to_id].parse_name
            lines += (2 * INDENT) + TRANSITION_DIRECT.format(parse_name) + NEWLINE
            lines += INDENT + CLOSING_BLOCK + (2*NEWLINE)
            return lines

        # if neither of above then regular header parsing

        lines += INDENT + STATE_INIT.format(current_state.parse_name) + NEWLINE
        lines += (2 * INDENT) + EXTRACT_LINE.format(HEADER_NAME, current_state.name) + NEWLINE

        if len(current_state.transition_to) < 2:
            next_state = ""

            if states[current_state.transition_to[FIRST].to_id].name == ACCEPT:
                next_state = states[current_state.transition_to[FIRST].to_id].name
            else:
                next_state = states[current_state.transition_to[FIRST].to_id].parse_name

            lines += (2 * INDENT) + TRANSITION_DIRECT.format(next_state) + NEWLINE
            lines += INDENT + CLOSING_BLOCK + (2 * NEWLINE)
        else:

            nxt_states = [states[nstate.to_id] for nstate in current_state.transition_to]
            on_fields = [x.default_trans[current_state.name].on_field for x in nxt_states if
                         current_state.name in x.default_trans]

            # if not len(on_fields) == len(nxt_states) or all(f == on_fields[ANY] for f in on_fields):
            # we have a problem here
            # pass

            lines += (2 * INDENT) + TRANSITION_INIT.format(HEADER_NAME, current_state.name, on_fields[FIRST]) + NEWLINE

            trans = 0

            for transition in transitions[current_state.id]:

                print(current_state.name+" -> "+states[transition.to_id].name)

                trans += 1

                if states[transition.to_id].name == 'accept':
                    lines += (2 * INDENT) + TRANSITION_ACCEPT + NEWLINE
                    lines += INDENT + CLOSING_BLOCK + (2 * NEWLINE)
                    continue

                dt = None

                if current_state.name in states[transition.to_id].default_trans:
                    dt = states[transition.to_id].default_trans[current_state.name]

                if (dt is None and (transition.value is None)) or \
                        ((dt.has_missing_params()) or transition.value.has_missing_params()):
                    # we have a problem
                    pass

                from_header = dt.from_header if transition.value.has_missing_params() else transition.value.from_header
                on_field = dt.on_field if not transition.value.on_field else transition.value.on_field
                on_value = dt.on_value if not transition.value.on_value else transition.value.on_value
                on_value_type = dt.on_value_type if not transition.value.on_value_type else \
                    transition.value.on_value_type

                if on_value_type in BINARY_VALUES:
                    if not (on_value.startswith('0b') or on_value.startswith('0B')):
                        on_value = '0b' + on_value
                elif on_value_type in OCTAL_VALUES:
                    if not (on_value.startswith('0o') or on_value.startswith('0O')):
                        on_value = '0o' + on_value
                elif on_value_type in HEXADECIMAL_VALUES:
                    if not (on_value.startswith('0x') or on_value.startswith('0X')):
                        on_value = '0x' + on_value

                constant = on_field.upper() + "_" + states[transition.to_id].name.upper()

                if constant not in self.consts:
                    bit_width = headers[from_header].get_field_by_name(on_field).bit_width
                    self.consts.append({constant: (bit_width, on_value)})

                lines += (3 * INDENT) + TRANSITION_LINE.format(constant, states[transition.to_id].parse_name) + NEWLINE

                if trans == len(transitions[current_state.id]):
                    lines += (3 * INDENT) + TRANS_DEFAULT + NEWLINE

            lines += (2 * INDENT) + CLOSING_BLOCK + NEWLINE

            lines += INDENT + CLOSING_BLOCK + (2*NEWLINE)

        return lines

    def write_block_upper(self, block, path):

        lines_to_write = self.process_block_upper(block)

        with open(path, 'a') as file:
            file.write(lines_to_write)

        return lines_to_write

    def process_block_upper(self, block):

        lines_to_write = block.type + SPACE + block.name + OPENING_PT

        PARAM_INDENT_COUNT = len(lines_to_write)

        for idx, param in enumerate(block.parameters):

            if idx != 0:
                lines_to_write += (PARAM_INDENT_COUNT * SPACE)

            param_fmt = self.generate_param(param.get_attr_dict())

            if param.get_num_params() == 2:
                lines_to_write += param_fmt.format(param.type, param.name)
            elif param.get_num_params() == 3:
                lines_to_write += param_fmt.format(param.direction, param.type, param.name)

            if idx != (len(block.parameters) - 1):
                lines_to_write += COMMA + NEWLINE

        lines_to_write += CLOSING_PT + OPENING_BLOCK + (2 * NEWLINE)

        return lines_to_write

    def decide_path(self, type, args, main_path):

        path = args.output_path

        if type in args.separate_files.split(","):
            if args.include_dir:
                path += INCLUDE + SLASH

            path += type + P4_EXTENSION
        else:
            path = main_path

        return path

    def generate_param(self, params):

        single = "{{{0}}}"+SPACE
        param_arg = ""

        i = 0

        for k,v in params.items():
            if v:
                param_arg += single.format(str(i))
                i+=1

        return param_arg.strip()

    def process_transition_consts(self):

        self.str_tr_const = ""

        for constant in self.consts:
            name = ""
            bitwidth = ""
            value = ""
            for k,v in constant.items():
                name = k
                bitwidth = v[0]
                value = v[1]
            self.str_tr_const += CONSTANT_ENTRY.format(bitwidth, name, value) + NEWLINE