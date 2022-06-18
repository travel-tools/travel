

def log_title(logger, title: str, char: str = "*", ending: bool = False):
    logger.info("")
    if not ending:
        logger.info(char*60)
    logger.info(f"   {title}   ".center(60, char))
    logger.info(char*60)
