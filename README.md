# callflow
Binary function flow analyzer

## Setup

Start a Neo4j database:

```
$ docker-compose up -d
```

You can also bring your own database, just set the correct flags so callflow knows how to connect to it.

Now you are ready to import data.

## Data Collection

Currently, callflow only supports IDA Pro + Linux binaries. However, support for Windows binaries and Ghidra/Binary Ninja is WIP.

1. Load your target binary in IDA Pro
2. Start the callflow server: `python main.py server`. This will listen on `localhost:8300` by default.
3. Load the IDA Python plugin at `ida/export_func_data.py`
    * If you copy this file elsewhere, make sure to bring a copy of `callflow/model.py` and put it in the same directory. The `ida/model.py` is a relative symlink.

## Analysis

For now, you can query the data via the Neo4j HTTP interface on port 7474. Here is a query to get you started:

```
match (a)-[e:CALLS]->(b) return a, e, b
```

![Call graph in neo4j](/img/example_graph.png)

## Todo

- [ ] add an "implied call" or something between `__libc_start_main` and `main`