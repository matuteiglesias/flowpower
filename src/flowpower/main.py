import typer
import sys

# ✅ Import promptflow fallback logic
from promptflow._cli._pf.entry import get_parser_args, run_command
from promptflow._cli._utils import cli_exception_and_telemetry_handler
from promptflow._sdk._telemetry.activity import update_activity_name
from promptflow._cli._pf.help import show_privacy_statement, show_welcome_message
from promptflow._cli._user_agent import USER_AGENT
from promptflow._sdk._utilities.general_utils import print_promptflow_version_dict_string
from promptflow._utils.user_agent_utils import setup_user_agent_to_operation_context

# ✅ Import your custom commands
# from flowpower.cli.test_block import app as test_block_app  # example

cli = typer.Typer(help="🌊 FlowPower CLI – Extend PromptFlow with custom commands")

# ✅ Register commands
# cli.add_typer(test_block_app, name="test-block")

from dotenv import load_dotenv
load_dotenv()



@cli.callback(invoke_without_command=True)
def fallback_to_promptflow(ctx: typer.Context):
    """
    Run PromptFlow's native CLI logic if no subcommand is given.
    """
    argv = sys.argv[1:]

    if len(argv) == 0:
        show_privacy_statement()
        show_welcome_message()
        argv = ["-h"]

    elif len(argv) == 1 and argv[0] in {"version", "--version", "-v"}:
        print_promptflow_version_dict_string(with_azure=True)
        try:
            raise typer.Exit(0)
        except typer.Exit as e:
            sys.exit(e.exit_code)  # avoid showing traceback




    prog, args = get_parser_args(argv)

    setup_user_agent_to_operation_context(
        args.user_agent if hasattr(args, "user_agent") else USER_AGENT
    )

    activity_name = f"fp.{getattr(args, 'action', 'entry')}"
    activity_name = update_activity_name(activity_name, args=args)

    cli_exception_and_telemetry_handler(run_command, activity_name)(args)

    try:
        raise typer.Exit(0)
    except typer.Exit as e:
        sys.exit(e.exit_code)  # avoid showing traceback



def main():
    argv = sys.argv[1:]

    if not argv or argv in [["-h"], ["--help"]]:
        cli()  # Let Typer handle it
    elif argv[0] in cli.registered_commands:
        cli()
    else:
        fallback_to_promptflow(argv)



# def main():
#     cli()


# # ✅ Alias for setup.py/pyproject entrypoint
# cli = main




# import typer
# import sys

# # ✅ Import promptflow fallback logic
# from promptflow._cli._pf.entry import get_parser_args, run_command
# from promptflow._cli._utils import cli_exception_and_telemetry_handler
# from promptflow._sdk._telemetry.activity import update_activity_name
# from promptflow._cli._pf.help import show_privacy_statement, show_welcome_message
# from promptflow._cli._user_agent import USER_AGENT
# from promptflow._sdk._utilities.general_utils import print_promptflow_version_dict_string
# from promptflow._utils.user_agent_utils import setup_user_agent_to_operation_context

# # ✅ Import your custom commands
# from flowpower.cli.test_block import app as test_block_app  # example

# cli = typer.Typer(help="🌊 FlowPower CLI – Extend PromptFlow with custom commands")

# # ✅ Register commands
# cli.add_typer(test_block_app, name="test-block")


# @cli.callback(invoke_without_command=True)
# def fallback_to_promptflow(ctx: typer.Context):
#     """
#     Run PromptFlow's native CLI logic if no subcommand is given.
#     """
#     argv = sys.argv[1:]

#     if len(argv) == 0:
#         show_privacy_statement()
#         show_welcome_message()
#         argv = ["-h"]

#     elif len(argv) == 1 and argv[0] in {"version", "--version", "-v"}:
#         print_promptflow_version_dict_string(with_azure=True)
#         raise typer.Exit(0)

#     prog, args = get_parser_args(argv)

#     setup_user_agent_to_operation_context(
#         args.user_agent if hasattr(args, "user_agent") else USER_AGENT
#     )

#     activity_name = f"fp.{getattr(args, 'action', 'entry')}"
#     activity_name = update_activity_name(activity_name, args=args)

#     cli_exception_and_telemetry_handler(run_command, activity_name)(args)
#     raise typer.Exit(0)


# def main():
#     cli()


# # ✅ Alias for setup.py/pyproject entrypoint
# cli = main
