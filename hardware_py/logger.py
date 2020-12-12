#!/usr/bin/env python3

import configlogger as log  
import submodule

logger = log.set_logger(__name__)

logger.debug('Messaggio di debug')
logger.info('Messaggio info')
logger.warning('Avviso')
logger.error('Messaggio di errore')
logger.critical('Errore grave')