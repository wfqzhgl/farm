# -*- coding: utf-8 -*-

import sys
try:
    PY2 = sys.version_info.major == 2
except:
    PY2 = sys.version_info[0] == 2

import functools
import os
import socket
import struct

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

with open(os.path.join(os.path.dirname(__file__), "17monipdb.dat"), "rb") as f:
    dat = f.read()
    offset, = _unpack_N(dat[:4])
    index = dat[4:offset]


def memoize(func):
    """Memoize for functions based on memory
    """
    cache = func.cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = "{0}{1}".format(args, kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper


@memoize
def _find_ip(ip):
    nip = socket.inet_aton(ip)

    tmp_offset = int(ip.split(".")[0]) * 4
    start, = _unpack_V(index[tmp_offset:tmp_offset + 4])

    index_offset = index_length = 0
    max_comp_len = offset - 1028
    start = start * 8 + 1024
    while start < max_comp_len:
        if index[start:start + 4] >= nip:
            index_offset, = _unpack_V(
                index[start + 4:start + 7] + chr(0).encode("utf-8"))
            if PY2:
                index_length, = _unpack_C(index[start + 7])
            else:
                index_length = index[start + 7]
            break
        start += 8

    if index_offset == 0:
        return

    res_offset = offset + index_offset - 1024
    return dat[res_offset:res_offset + index_length].decode("utf-8").strip()


def find(ip):
    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        return

    return _find_ip(ip)


if __name__ == '__main__':
    import re
    print find("58.192.191.255"), re.split(r'\t', find("58.192.191.255"))[:3]
    print find("218.56.0.202"), re.split(r'\t', find("218.56.0.202"))[:3]
    print find("60.171.139.143"), re.split(r'\t', find("60.171.139.143"))[:3]
    print find("222.23.243.122"), re.split(r'\t', find("222.23.243.122"))[:3]
    print find("218.162.197.1")
    print find("61.10.255.255")
    print find("117.136.19.125")