YugaByte Python Driver for YugaByte DB's Cassandra compatible YCQL API
======================================================================


A modern, `feature-rich <https://github.com/yugabyte/cassandra-python-driver#features>`_ and highly-tunable Python client library for YugaByte DB's Cassandra compatible YCQL API using Cassandra's binary protocol and Cassandra Query Language v3.

The driver supports Python 3.10 through 3.14.


**Note:** This driver does not support big-endian systems.

Feedback Requested
------------------
Please provide feedback by opening an issue on github.

Features
--------
* `Synchronous <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/cluster/index.html#cassandra.cluster.Session.execute>`_ and `Asynchronous <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/cluster/index.html#cassandra.cluster.Session.execute_async>`_ APIs
* `Simple, Prepared, and Batch statements <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/query/index.html#cassandra.query.Statement>`_
* Asynchronous IO, parallel execution, request pipelining
* `Connection pooling <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/cluster/index.html#cassandra.cluster.Cluster.get_core_connections_per_host>`_
* Automatic node discovery
* `Automatic reconnection <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/policies/index.html#reconnecting-to-dead-hosts>`_
* Configurable `load balancing <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/policies/index.html#load-balancing>`_ and `retry policies <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/policies/index.html#retrying-failed-operations>`_
* `Concurrent execution utilities <https://docs.datastax.com/en/developer/python-driver/latest/api/cassandra/concurrent/index.html>`_
* `Object mapper <https://docs.datastax.com/en/developer/python-driver/latest/object_mapper/>`_
* `Connecting to DataStax Astra database (cloud) <https://docs.datastax.com/en/developer/python-driver/latest/cloud/>`_
* DSE Graph execution API
* DSE Geometric type serialization
* DSE PlainText and GSSAPI authentication

Installation
------------
Installation through pip is recommended::

    $ pip install yb-cassandra-driver

For more complete installation instructions, see the
`installation guide <https://docs.datastax.com/en/developer/python-driver/latest/installation/index.html>`_.

Documentation
-------------
A couple of links for getting up to speed:

* `Getting started guide <https://docs.yugabyte.com/latest/develop/client-drivers/python/>`_
* `API docs <http://datastax.github.io/python-driver/api/index.html>`_
* `Performance tips <http://datastax.github.io/python-driver/performance.html>`_


Contributing
------------
See `CONTRIBUTING.md <https://github.com/YugaByte/cassandra-python-driver/blob/master/CONTRIBUTING.rst>`_.

Error Handling
--------------
While originally written for the Java driver, users may reference the `Cassandra error handling done right blog <https://www.datastax.com/blog/cassandra-error-handling-done-right>`_ for resolving error handling scenarios with Apache Cassandra.

Reporting Problems
------------------
Please report any bugs and make any feature requests on github.

Getting Help
------------
For help on this product, please open a github issue.

License
-------
Copyright 2018, YugaByte Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
