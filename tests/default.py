#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simple.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


from wishbone.actorconfig import ActorConfig
from wishbone_output_azure_queue_storage import AzureQueueStorageOut


def test_module_init():

    actor_config = ActorConfig('AzureQueueStorageOut', 100, 1, {}, "")
    d = AzureQueueStorageOut(actor_config)
    d.start()
    assert d.name == "AzureQueueStorageOut"
