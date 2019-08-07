class Tile:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color


class Summary:
    def __init__(self, player, tiles):
        self.player = player
        self.tiles = tiles

class Response:
    def __init__(self, resp_type, resp_info):
        self.resp_type = resp_type
        self.resp_info = resp_info


def parse_int_tuple(src):
    return tuple(map(int, src.split(".")))


def parse_color(col):
    return "#%x%x%x" % parse_int_tuple(col)


def parse_tile(loc):
    pos, color = tuple(loc.split(":"))
    return Tile(parse_int_tuple(pos), parse_color(color))


def parse_summary(sum):
    player, tiles = tuple(sum.split(","))
    return Summary(parse_color(player), map(parse_tile, tiles.split("|")))

def parse_response(resp):
    resp_type, resp_info = resp.split(";")
    if resp_type == "Error": return Response(resp_type, resp_info)
    if resp_type == "Update": return Response(resp_type, parse_summary(resp_info))


def request_start(): return "Start;"


def request_do_turn(x, y): return "DoTurn;%d,%d" % (x, y)
