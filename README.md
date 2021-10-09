# callflow
Binary function flow analyzer

plugins will:
* get a list of functions
* go through the function and find everything they call
* send data to server, which will store that data in the neo4j db

add an "implied call" or something between __libc_start_main and main