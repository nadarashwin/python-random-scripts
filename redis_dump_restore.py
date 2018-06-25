#!/usr/bin/env python

import json
import redis
import argparse
from pprint import pprint


def get_args():
    parser = argparse.ArgumentParser(
        description="redis usage for dump & restore",
        add_help=False)

    parser.add_argument('-h', '--host',
                        default='localhost',
                        help='connect to HOST(default is localhost)')

    parser.add_argument('-p', '--port',
                        default=6379,
                        help='port to connect')

    parser.add_argument('-P', '--password',
                        help='password for redis host to connect')

    parser.add_argument('-k', '--keys',
                        default='*',
                        help='redis keys to query')

    parser.add_argument('-o', '--output',
                        help='save the file to redis')

    parser.add_argument('-i', '--input',
                        help='load the file to redis')

    parser.add_argument('-d', '--database',
                        default=0,
                        help='database to connect')

    return parser.parse_args()


def dump(fp, keys, host, port, password=None, db=0, pretty=False):
    r = redis.StrictRedis(host=host, port=port, password=password,
                          db=db, decode_responses=True)
    kwargs = {}
    if not pretty:
        kwargs['separators'] = (',', ':')
    else:
        kwargs['indent'] = 2
        kwargs['sor_keys'] = True

    encoder = json.JSONEncoder(**kwargs)

    key_count = 0

    for key, type, value in _reader(r, keys, pretty):
        d = {}
        d[key] = {'type': type, 'value': value}
        item = encoder.encode(d)
        fp.write(item)
        fp.write("\n")
        key_count = key_count + 1

    print(key_count, ' keys dumped into the file')


def load(fp, host, port, password=None, db=0):
    r = redis.StrictRedis(host=host, port=port, password=password,
                          db=db, decode_responses=True)
    pipe = r.pipeline()
    size = 0
    key_count = 0
    for s in fp.readlines():
        table = json.loads(s)
        size = size + s.__len__()
        for key in table:
            item = table[key]
            type = item['type']
            value = item['value']
            _writer(pipe, key, type, value)
            key_count = key_count + 1
        if size > 1024*1024*5:
            pipe.execute()
            pipe = r.pipeline()
            size = 0
    pipe.execute()
    print(key_count, ' keys inserted into redis')


def _reader(r, keys, pretty):
    kys = r.keys(keys)
    pprint(len(keys))
    for key in kys:
        type = r.type(key)
        if type == 'string':
            value = r.get(key)
        elif type == 'list':
            value = r.lrange(key, 0, -1)
        elif type == 'set':
            value = list(r.smembers(key))
            if pretty:
                value.sort()
        elif type == 'zset':
            value = r.zrange(key, 0, -1, False, True)
        elif type == 'hash':
            value = r.hgetall(key)
        else:
            return ('Unknown key type: %s' % type)
        yield key, type, value


def _writer(pipe, key, type, value):
    if type == 'string':
        pipe.set(key, value)
    elif type == 'list':
        for element in value:
            pipe.rpush(key, element)
    elif type == 'set':
        for element in value:
            pipe.sadd(key, element)
    elif type == 'zset':
        for element in value.keys():
            pipe.zadd(key, element, value[element])
    elif type == 'hash':
        for element in value.keys():
            pipe.hset(key, element, value[element])
    else:
        return ("Unknown key type: %s" % type)


def main():
    args = get_args()
    if args.output:
        output = open(args.output, 'w')
        dump(output, args.keys, args.host, args.port,
             args.password, args.database)
    if args.input:
        input = open(args.input, 'r')
        load(input, args.host, args.port,
             args.password, args.database)


if __name__ == '__main__':
    main()
