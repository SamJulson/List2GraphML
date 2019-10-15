import sys
import io
import os
import json
import string

def main(args):
    if (len(args) < 3):
        print("Error: Files not specified", file=sys.stderr)
        sys.exit(0)
    if (os.path.exists(args[len(args)-1])):
        print("Error: Database already exists", file=sys.stderr)
        sys.exit(0)
    databaseFilepath = args.pop(len(args) - 1)
    args.pop(0)

    for path in args:
         if not os.path.exists(path) or not os.path.isfile(path):
             print("Warning: Path" + path + "not found. Removing from list.")
             args.remove(path)

    createDatabase(args, databaseFilepath)

def createDatabase(paths, databaseFilepath):
    objs = []
    id = 0
    for path in paths:
        print("Opening file " + path)
        fs = open(path, mode='rb')
        type = fs.readline().decode("utf-8").strip()
        fs.readline()
        while True:
            name = fs.readline().decode("utf-8").strip()
            if name == "":
                break
            prereqs = []
            while True:
                marker = fs.read(1)
                if marker != b'\t':
                    fs.seek(-1, io.SEEK_CUR)
                    break
                prereq = fs.readline().decode("utf-8").strip()
                prereqs.append(prereq)
            obj = {
                'id': id,
                'type': type,
                'name': name,
                'prereqs': prereqs
            }
            print("Adding object " + obj['name'])
            objs.append(obj)
            id += 1
        fs.close()

    for parent in objs:
        prereqs = parent['prereqs']
        ids = []
        for prereq in prereqs:
            for child in objs:
                if child['name'] == prereq:
                    ids.append(child['id'])
                    break
        parent['prereqs'] = ids

    dbfile = open(databaseFilepath, mode='w')
    json.dump(objs, dbfile, ensure_ascii=True, indent=4)
    dbfile.flush()
    dbfile.close()

main(sys.argv)
