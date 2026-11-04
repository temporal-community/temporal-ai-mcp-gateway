from durable_mcp_gateway import config

from .run import main

if __name__ == "__main__":
    # `python -m stdio` bypasses the CLI's logging setup, so do the quiet default here.
    config.configure_logging()
    main()
