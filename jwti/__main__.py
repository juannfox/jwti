from typing import Annotated, Optional
from types import FunctionType
from sys import exit, argv
from sys import version_info, stdin
from json import dumps

import typer
from rich import print
from rich.status import Status

from jwti.__version__ import app_full_name, app_version
from jwti.logger import log
from jwti.jwt import decode_jwt, parse_jwt_registered_claims, filter_jwt_claims


def railguard_execution(
    callable: FunctionType, action_description: Optional[str] = None, **kwargs
):
    """Safely execute a callable and break app execution."""
    log.debug(f"Executing '{callable}({kwargs})'.")
    action_description = action_description or f"executing {callable.__name__}"

    try:
        with Status(f":hourglass: {action_description.capitalize()}..."):
            return callable(**kwargs)
    except Exception as e:
        log.error(f"Runtime error {action_description}: {e}")
    exit(1)


######################################################################


app = typer.Typer(
    help=(
        f"""
        :anchor: [bold blue]{app_full_name}[/bold blue]:
        Seamless [italic]JWT[/italic] query tool
        """
    ),
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.callback()
def main(
    ctx: typer.Context,
    log_level: Annotated[
        Optional[str],
        typer.Option(
            "--log-level",
            "-l",
            envvar="JWTQ_LOG_LEVEL",
            help="Set the logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL).",
        ),
    ] = "INFO",
):
    """Init for Typer app"""
    if log_level:
        log.setLevel(log_level.upper())
        log.debug(f"Log level set to {log_level.upper()}")
    log.debug(f"Starting Typer app's subcommand '{ctx.invoked_subcommand}'")
    log.debug(f" User executed: {argv}.")


@app.command()
def inspect(
    token: Annotated[
        Optional[str],
        typer.Argument(
            help=(
                "JWT token to inspect; use '-' or empty to read from STDIN."
            )
        ),
    ] = None,
    claims: Annotated[
        Optional[list[str]],
        typer.Option(
            "-c", "--claims",
            envvar="JWTQ_CLAIMS",
            help=(
                "Which claim/s to display; use multiple -c for "
                "multiple claims."
            ),
        ),
    ] = None,
    raw: Annotated[
        Optional[bool],
        typer.Option(
            "-r", "--raw",
            envvar="JWTQ_CLAIMS_RAW_OUTPUT",
            help=(
                "Whether to display raw JWT claim values."
            ),
            is_flag=True,
        ),
    ] = False,
    json: Annotated[
        Optional[bool],
        typer.Option(
            "-j", "--json",
            envvar="JWTQ_CLAIMS_JSON_OUTPUT",
            help=(
                "Whether to display the decoded JWT as raw JSON."
            ),
            is_flag=True,
        ),
    ] = False
):
    """
    Inspect a JWT token.
    """
    if not token or token == "-":
        log.debug("Reading token from stdin.")
        token = stdin.readline().strip()

    # Decode the JWT token
    payload = railguard_execution(
        decode_jwt,
        action_description="decoding JWT",
        jwt=token
    )

    # Filter claims if requested
    if claims:
        payload = railguard_execution(
            filter_jwt_claims,
            action_description="filtering JWT claims",
            jwt=payload,
            claims=claims
        )

    # Parse claims if requested
    if not raw:
        payload = railguard_execution(
            parse_jwt_registered_claims,
            action_description="parsing JWT date claims",
            jwt=payload
        )

    # Serialize JSON if requested
    if json:
        payload = railguard_execution(
            dumps,
            action_description="Serializing JWT to JSON",
            obj=payload
        )

    print(payload)


@app.command()
def version():
    """
    Display the current application version.
    """
    python_version = (
        f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    )
    print(
        f":key: [bold blue]{app_full_name}[/bold blue] {app_version} "
        f"(Python {python_version})"
    )


if __name__ == "__main__":
    try:
        app()
    except RuntimeError as e:
        print(f":warning: [bold red]Error[/bold red]: {e}")
