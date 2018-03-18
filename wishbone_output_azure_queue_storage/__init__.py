#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
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


from gevent import monkey; monkey.patch_all()
from azure.storage.queue import QueueService
from base64 import b64encode
import logging
from wishbone.module import OutputModule
from wishbone.protocol.decode.plain import Plain
from gevent.event import Event


class AzureQueueStorageOut(OutputModule):
    '''
    Submit messages to Azure Queue Storage

    Submit messages to the Microsoft Azure Queue Storage service.


    Parameters::

        - account_name(str)("wishbone")
           |  The account name to authenticate to

        - account_key(str)("wishbone")
           |  The account key to authenticate to the queue

        - b64encode(bool)(True)
           |  Encode the message payload.

        - endpoint_suffix(str)("core.windows.net")
           |  The endpoint suffix of the service

        - native_events(bool)(False)
           |  Whether to expect incoming events to be native Wishbone events

        - parallel_streams(int)(1)
           |  The number of outgoing parallel data streams.

        - payload(str)(None)
           |  The string to submit.
           |  If defined takes precedence over `selection`.

        - queue_name(str)("wishbone")
           |  The name of the queue to consume

        - selection(str)(data)
           |  The event key to submit.
           |  If ``None`` the complete event is selected.
           |  By default the content of the ``data`` is selected.

        - time_to_live(int)(0)
           | If not specified, the default value is 0. Specifies the
           | new visibility timeout value, in seconds, relative to server time.
           | The value must be larger than or equal to 0, and cannot be
           | larger than 7 days. The visibility timeout of a message cannot be
           | set to a value later than the expiry time. visibility_timeout
           | should be set to a value smaller than the time-to-live value.

        - visibility_timeout(int)(0)
           |  If not specified, the default value is 0. Specifies the new visibility timeout
           |  value, in seconds, relative to server time. The value must be larger than or
           |  equal to 0, and cannot be larger than 7 days. The visibility timeout of a
           |  message cannot be set to a value later than the expiry time.
           |  visibility_timeout should be set to a value smaller than the time-to-live
           |  value.


    Queues::

        - outbox
           |  Outgoing events.
    '''

    def __init__(self, actor_config, selection="data", payload=None, native_events=False, parallel_streams=1,
                 account_name="wishbone", account_key="wishbone", queue_name="wishbone", endpoint_suffix='core.windows.net',
                 visibility_timeout=0, time_to_live=0, b64encode=True):

        OutputModule.__init__(self, actor_config)
        self.pool.createQueue("inbox")

        self.decode = Plain().handler

        self.__connect = Event()
        self.__connect.set()

        self.__submit = Event()
        self.__submit.clear()

    def preHook(self):

        logger = logging.getLogger('azure.storage')
        logger.setLevel(logging.CRITICAL)

        self.sendToBackground(self.setupConnectivity)
        self.registerConsumer(self.submitEvent, "inbox")

    def setupConnectivity(self):

        while self.loop():
            self.__connect.wait()
            try:
                self.queue_service = QueueService(
                    account_name=self.kwargs.account_name,
                    account_key=self.kwargs.account_key,
                    endpoint_suffix=self.kwargs.endpoint_suffix,
                )
                self.queue_service.create_queue(self.kwargs.queue_name)
            except Exception as err:
                message = "Failed to connect to Azure Queue Service https://%s.queue.%s/%s Reason: " % (self.kwargs.account_name, self.kwargs.endpoint_suffix, self.kwargs.queue_name)
                raise Exception(message + str(err).partition("\n")[0])
            else:
                self.logging.info("Connected to Azure Queue Service https://%s.queue.%s/%s" % (self.kwargs.account_name, self.kwargs.endpoint_suffix, self.kwargs.queue_name))
                self.__connect.clear()
                self.__submit.set()

    def submitEvent(self, event):

        self.__submit.wait()

        data = self.getDataToSubmit(event)
        data = self.encode(data)
        if self.kwargs.b64encode:
            data = b64encode(bytes(data, 'utf-8'))
            data = data.decode()
        try:
            self.queue_service.put_message(event.kwargs.queue_name, data)
        except Exception as err:
            self.__connect.set()
            self.__submit.clear()
            raise Exception("Failed to submit message. Reason: %s" % (err))
