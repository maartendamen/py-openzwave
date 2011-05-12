#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from examples.common.ozwWrapper import ZWaveWrapper

FORMAT='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
log = logging.getLogger('ZWaveWrapper')

wrapper = ZWaveWrapper(device='/dev/keyspan-2', config='openzwave/config/', log=log)

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
ipshell()
