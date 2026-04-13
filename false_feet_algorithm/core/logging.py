"""
Logging utilities for the False Feet Algorithm.

Configures logging for debug output, iteration tracking, and performance metrics.
"""

import logging
import sys
from typing import Optional


class AmoebaLogger:
    """Centralized logging configuration for Amoeba."""

    _logger: Optional[logging.Logger] = None
    _configured = False

    @staticmethod
    def configure(
        level: str = "INFO",
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
    ) -> logging.Logger:
        """
        Configure the Amoeba logger.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR)
            log_file: Optional file to log to (in addition to console)
            format_string: Custom format string (uses sensible default if None)

        Returns:
            Configured logger instance
        """
        if AmoebaLogger._configured:
            return AmoebaLogger._logger

        logger = logging.getLogger("false_feet_algorithm")
        logger.setLevel(getattr(logging, level.upper()))

        if format_string is None:
            format_string = "%(levelname)-8s [%(name)s] %(message)s"

        formatter = logging.Formatter(format_string)

        # Console handler
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        AmoebaLogger._logger = logger
        AmoebaLogger._configured = True

        return logger

    @staticmethod
    def get_logger() -> logging.Logger:
        """Get the logger (configure with defaults if not already done)."""
        if AmoebaLogger._logger is None:
            AmoebaLogger.configure()
        return AmoebaLogger._logger

    @staticmethod
    def reset():
        """Reset the logger (for testing)."""
        if AmoebaLogger._logger:
            for handler in AmoebaLogger._logger.handlers[:]:
                AmoebaLogger._logger.removeHandler(handler)
        AmoebaLogger._logger = None
        AmoebaLogger._configured = False


# Get the default logger
logger = logging.getLogger("false_feet_algorithm")

# Default configuration with minimal setup
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
