"""Исполнить ограниченный Lua fixture через Lua 5.1 текущей X4 (без игры)."""
import argparse
import ctypes as C
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('fixture', type=Path)
    args = parser.parse_args()
    lua = C.CDLL(str((args.game / 'lua51_64.dll').resolve()))
    lua.luaL_newstate.restype = C.c_void_p
    lua.luaL_openlibs.argtypes = [C.c_void_p]
    lua.luaL_loadbuffer.argtypes = [C.c_void_p, C.c_char_p, C.c_size_t, C.c_char_p]
    lua.lua_pcall.argtypes = [C.c_void_p, C.c_int, C.c_int, C.c_int]
    lua.lua_tolstring.argtypes = [C.c_void_p, C.c_int, C.POINTER(C.c_size_t)]
    lua.lua_tolstring.restype = C.c_void_p
    lua.lua_close.argtypes = [C.c_void_p]
    state = lua.luaL_newstate()
    if not state:
        raise RuntimeError('Нет Lua state')
    try:
        lua.luaL_openlibs(state)
        source = args.fixture.read_bytes()
        status = lua.luaL_loadbuffer(state, source, len(source), str(args.fixture).encode())
        if status == 0:
            status = lua.lua_pcall(state, 0, 0, 0)
        if status:
            size = C.c_size_t()
            ptr = lua.lua_tolstring(state, -1, C.byref(size))
            raise RuntimeError(C.string_at(ptr, size.value).decode('utf-8', 'replace'))
    finally:
        lua.lua_close(state)
    print('PASS: ' + str(args.fixture))


if __name__ == '__main__':
    main()
