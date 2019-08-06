class Location:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color


class Response:
    def __init__(self, resp_type, resp_info):
        self.resp_type = resp_type
        self.resp_info = resp_info


def parse_location(loc):
    pos, color = tuple(loc.split(":"))
    parse = lambda src: tuple(map(int, src.split(".")))
    return Location(parse(pos), "#%x%x%x" % parse(color))


def parse_response(resp):
    resp_type, resp_info = resp.split(";")
    if resp_type == "Error": return Response(resp_type, resp_info)

    if resp_type == "Update": return Response(resp_type, map(parse_location, resp_info.split(",")))


def request_start(): return "Start;"


def request_do_turn(x, y): return "DoTurn;%d,%d" % (x, y)
