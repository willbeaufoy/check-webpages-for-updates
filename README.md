### check-webpages-for-updates

Checks urls passed to it for updates and emails user. First arg must be url to check, second must be email address to notify

#### Requires a config.py like the following + an sqlite database

    import logging

    db_name = 'your_db_name'

    server = 'your_smtp_server:your_smtp_port'
    username = 'your_smtp_username'
    password = 'your_smtp_password'
    from_address = 'your_from_address'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler('your_desired_log_name')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
