import argparse
import sys
import io
import json
import pyyed

nodeWidth = 125
nodeHeight = 50
nodeDistanceX = nodeWidth + 25
nodeDistanceY = 2 * nodeHeight
nodeShape = 'ellipse'
colors = {
    'Key Item' : '#FFFF99',
    'Basic Job' : '#BBBBFF',
    'Intermediate Job' : '#AAAAEE',
    'Advanced Job' : '#9999DD',
    'Basic Race' : '#FFBBBB',
    'Intermediate Race' : '#EEAAAA',
    'Advanced Race' : '#DD9999'
}

description = '''
    Creates a graph in graphml from a database file.
'''

def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dbfile', type=argparse.FileType('r'))
    parser.add_argument('-o', type=argparse.FileType('w'), nargs='+', default=open('./output.graphml', 'w'))

    args = parser.parse_args()

    generateGraphML(args.dbfile, args.o)
    args.dbfile.close()
    args.o.flush()
    args.o.close()

def generateGraphML(databaseFile, outputFile):
    g = pyyed.Graph()
    objs = json.load(databaseFile)
    xcoord = 0
    ycoord = 0
    currtype = objs[0]['type']
    for obj in objs:
        if obj['type'] != currtype:
            ycoord += nodeDistanceY
            xcoord = 0
            currtype = obj['type']
        g.add_node(obj['id'], label=obj['name'], shape=nodeShape, width=str(nodeWidth), height=str(nodeHeight), x=str(xcoord), y=str(ycoord), shape_fill=colors[obj['type']])
        xcoord += nodeDistanceX
    for parent in objs:
        for child in parent['prereqs']:
            parentId = parent['id']
            childId = child
            g.add_edge(childId, parentId)
    outputFile.write(g.get_graph())

main()
