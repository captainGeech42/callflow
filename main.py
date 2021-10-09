import argparse
import json
import sys

from callflow.db import CallflowDb
from callflow.model import Binary
from callflow.server import CallflowServer

def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(title="Commands (use -h after a command to see available options)", dest="command")

    # global args
    parent_parser = argparse.ArgumentParser(description="Global options", add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parent_parser.add_argument("-d", "--db-host", help="Neo4j database host", default="localhost")
    parent_parser.add_argument("-p", "--db-port", help="Neo4j database port", default=7687, type=int)
    parent_parser.add_argument("-u", "--db-user", help="Neo4j database user", default="neo4j")
    parent_parser.add_argument("-pw", "--db-pass", help="Neo4j database password", default="password")

    # server args
    server_parser = subparsers.add_parser("server", help="Spawn server to receive callflow data from IDA, Ghidra, or Binja", parents=[parent_parser], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    server_parser.add_argument("-lh", "--listen-host", help="IP address to listen on", default="localhost")
    server_parser.add_argument("-lp", "--listen-port", help="Port to listen on", default=8300, type=int)

    # import args
    import_parser = subparsers.add_parser("import", help="Import callflow JSON data", parents=[parent_parser], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    import_parser.add_argument("-fp", "--path", help="Path to JSON file", required=True)

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        return None
    
    return args

def import_data(db: CallflowDb, path: str) -> bool:
    try:
        with open(path, "r") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"failed to open {path} to import")
        return False

    binary = Binary.from_json(json.loads(data))
    print(f"imported JSON data, adding to db: {binary}")
    id = db.add_binary(binary)
    print(f"added binary to db, id = {id}")

    return True

def main():
    args = get_args()
    if args is None:
        return 2

    db = CallflowDb(args.db_host, args.db_port, args.db_user, args.db_pass)

    if args.command == "server":
        server = CallflowServer(args.listen_host, args.listen_port, db)
        try:
            server.run()
        except KeyboardInterrupt:
            print("got SIGINT, exiting...")
    elif args.command == "import":
        if not import_data(db, args.path):
            db.close()
            return 1
    
    db.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())