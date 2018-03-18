::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|


    ==================================================
    wishbone_contrib.module.output.azure-queue-storage
    ==================================================

    Version: 1.0.0

    Submit messages to Azure Queue Storage
    --------------------------------------

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

