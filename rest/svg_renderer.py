import drawSvg as draw

R_MAX = 300


def render_as_svg(data):

    svg = draw.Drawing(R_MAX * 2.5, R_MAX * 2.5, origin="center", displayInline=False)

    node_coords = {
        node["id"]: dict(x=node["coord"]["x"] * R_MAX, y=node["coord"]["y"] * R_MAX)
        for node in data["nodes"]
    }

    for edge in data["edges"]:
        x1, y1 = node_coords[edge["left"]]["x"], node_coords[edge["left"]]["y"]
        x2, y2 = node_coords[edge["right"]]["x"], node_coords[edge["right"]]["y"]
        e = draw.Line(x1, y1, x2, y2, stroke="grey", stroke_width=1, stroke_opacity=0.3)
        svg.append(e)

    for node in data["nodes"]:

        if not node["connected"]:
            continue

        c = draw.Circle(
            node["coord"]["x"] * R_MAX,
            node["coord"]["y"] * R_MAX,
            10,
            fill="green",
            fill_opacity=0.5,
            stroke_width=1,
            stroke="white",
        )
        c.appendTitle(node["opinion"])
        svg.append(c)

    return svg.asSvg()
