from httpie.cli.definition import options as httpie_options
from httpie.cli.options import ParserSpec, Qualifiers


def test_parser_serialization():
    small_parser = ParserSpec("test_parser")

    group_1 = small_parser.add_group("group_1")
    group_1.add_argument("regular_arg", help="regular arg", short_help="short")
    group_1.add_argument(
        "variadic_arg",
        metavar="META",
        help=Qualifiers.SUPPRESS,
        nargs=Qualifiers.ZERO_OR_MORE
    )
    group_1.add_argument(
        "-O",
        "--opt-arg",
        action="lazy_choices",
        getter=lambda: ["opt_1", "opt_2"],
        help_formatter=lambda state, *, isolation_mode: ", ".join(state),
        short_help="short_help",
    )

    group_2 = small_parser.add_group("group_2")
    group_2.add_argument("--typed", action="store_true", type=int)

    definition = small_parser.finalize()
    assert definition.serialize() == {
        "name": "test_parser",
        "description": None,
        "groups": [
            {
                "name": "group_1",
                "description": None,
                "is_mutually_exclusive": False,
                "args": [
                    {
                        "options": ["regular_arg"],
                        "description": "regular arg",
                        "short_description": "short",
                    },
                    {
                        "options": ["variadic_arg"],
                        "is_optional": True,
                        "is_variadic": True,
                        "metavar": "META",
                    },
                    {
                        "options": ["-O", "--opt-arg"],
                        "description": "opt_1, opt_2",
                        "short_description": "short_help",
                        "choices": ["opt_1", "opt_2"],
                    },
                ],
            },
            {
                "name": "group_2",
                "description": None,
                "is_mutually_exclusive": False,
                "args": [{"options": ["--typed"], "python_type_name": "int"}],
            },
        ],
    }


def test_session_ro_hidden_from_parser_schema():
    # harness:criterion=c-session-ro-not-in-parser-schema
    visible_options = [
        option
        for group in httpie_options.serialize()['groups']
        for argument in group['args']
        for option in argument['options']
    ]
    assert '--session-read-only' in visible_options
    assert '--session-ro' not in visible_options
