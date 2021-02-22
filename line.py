from copy import deepcopy
class Line(object):
    DEFAULT_ATTR = ["chr1", "refGene", "type", "0", "0", ".", "+", ".", " "]

    def __init__(self, line):
        self.written_line = line
        line = line.split("\t")
        self.chr = line[0]
        self.type = line[2]
        self.start_pos = line[3]
        self.end_pos = line[4]
        self.negative_dir = (line[6] == "-")
        self.frame = line[7]
        self.attrs = {}
        attrs = line[8].split(";")[:-1]
        for attr in attrs:
            attr = attr.split()
            self.attrs[attr[0]] = attr[1].split('\"')[1]

    @staticmethod
    def creat_line_by_name_and_corr(name, start_pos, end_pos, sign="+"):
        attrs = deepcopy(Line.DEFAULT_ATTR)
        attrs[2] = name
        attrs[3] = start_pos
        attrs[4] = end_pos
        attrs[6] = sign
        return "\t".join(attrs)


    @staticmethod
    def create_line_by_name_and_region(name, region):
        attrs = deepcopy(Line.DEFAULT_ATTR)
        attrs[2] = name
        attrs[3] = region.start_pos
        attrs[4] = region.end_pos
        attrs[6] = "-" if region.negative_dir else "+"

        return "\t".join(attrs)

    def __lt__(self, other):
        return self.start_pos < other.start_pos

    def __str__(self):
        attr = deepcopy(Line.DEFAULT_ATTR)
        attr[0] = self.chr
        attr[2] = self.type
        attr[3] = self.start_pos
        attr[4] = self.end_pos
        attr[6] = "-" if self.negative_dir else "+"
        attr[7] = self.frame

        for key, value in self.attrs.items():
            attr[8] += (key)
            attr[8] += (" \"" + value + "\"; ")
        return "\t".join(attr)
