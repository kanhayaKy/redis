# Redis Server in Python

## Overview
This project is a simple Redis-like in-memory key-value store implemented in Python. It supports essential Redis commands, including basic string operations, list operations, and database persistence.

## Features
The server supports the following Redis commands:
- `PING` - Check if the server is alive.
- `ECHO <message>` - Echo back the provided message.
- `GET <key>` - Retrieve the value of a key.
- `SET <key> <value>` - Set a key to a specific value.
- `EXISTS <key>` - Check if a key is present.
- `DEL <key1> [<key2> ...]` - Delete one or more keys.
- `INCR <key>` - Increment the value of a key by one.
- `DECR <key>` - Decrement the value of a key by one.
- `LPUSH <key> <value1> [<value2> ...]` - Insert values at the head of a list.
- `RPUSH <key> <value1> [<value2> ...]` - Insert values at the tail of a list.
- `SAVE` - Save the database state to disk.

## Installation
This project is managed using [Poetry](https://python-poetry.org/). To install dependencies, ensure you have Poetry installed, then run:

```sh
poetry install
```

## Running the Server
To start the Redis server, use:

```sh
poetry run python redis_server/server.py 
```

![image](https://github.com/user-attachments/assets/17e4e5a8-7a8d-4942-8e09-66df64923587)

## Running Tests
Tests are managed using `pytest`. To run the test suite, execute:

```sh
poetry run pytest
```

### Coverage Report
To get the coverage report of the project, execute :

```sh
poetry run coverage run -m pytest && coverage report -m                                           
```

## Persistence
The `SAVE` command allows saving the current state of the database to disk, ensuring data durability.

## Contributing
Feel free to fork this repository, submit pull requests, or open issues to enhance functionality and fix bugs.

## License
This project is licensed under the MIT License.

