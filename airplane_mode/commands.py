import click
import subprocess
import frappe

@click.command('this')
@click.argument('bench_args', nargs=-1, type=click.UNPROCESSED)
def set_flags(bench_args):
    """Run bench commands on the default site automatically."""
    
    if not bench_args:
        click.echo("Usage: bench this [COMMAND]")
        return

    # Dynamically get default_site from common_site_config.json
    # frappe.get_conf() handles path resolution automatically
    default_site = frappe.get_conf().get("default_site")

    if not default_site:
        click.echo("Error: No default_site found in common_site_config.json")
        return

    # Build and execute the command
    full_command = ["bench", "--site", default_site] + list(bench_args)
    
    click.echo(f"Executing: {' '.join(full_command)}")
    
    try:
        # subprocess.run hands terminal control to the secondary process
        subprocess.run(full_command, check=True)
    except subprocess.CalledProcessError:
        pass  # Bench handles its own error messages
    except KeyboardInterrupt:
        click.echo("\nInterrupted.")

# Register the command with Bench
commands = [set_flags]
