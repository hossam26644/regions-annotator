from copy import deepcopy
import sys
class Line(object):
    DEFAULT_ATTR = ["chr1", "refGene", "type", "0", "0", ".", "+", ".", " "]

    def __init__(self, line):

        if isinstance(line, Line):
            self.__dict__.update(line.__dict__)
            return

        self.written_line = line

        if line[0] == "#":
            self.type = 'comment'
            return

        line = line.split("\t")
        self.chr = line[0]
        self.type = line[2]
        self.start_pos = line[3]
        self.end_pos = line[4]
        self.length = int(self.end_pos) - int(self.start_pos)
        self.negative_dir = (line[6] == "-")
        self.frame = line[7]
        self.attrs = self.get_attributes(line[8])

    @classmethod
    def get_attributes(cls, line):
        '''
        decomposes the line attributes into a keyvalue dictionary
        '''
        tags = []
        line_attributes = {}
        attrs = line.split(";")[:-1]
        for attr in attrs:
            attr = attr.split()
            try:
                int(attr[1])
                line_attributes[attr[0]] = attr[1]
            except ValueError:
                if attr[0] == 'tag':
                    tags.append(attr[1].split('\"')[1])
                else:
                    line_attributes[attr[0]] = attr[1].split('\"')[1]


        line_attributes['tags'] = tags

        return line_attributes

    @staticmethod
    def creat_line_by_name_and_corr(chrom, name, start_pos, end_pos,
                                    sign="+", gene_name="no_gene"):

        attrs = deepcopy(Line.DEFAULT_ATTR)
        attrs[0] = chrom
        attrs[2] = name
        attrs[3] = start_pos
        attrs[4] = end_pos
        attrs[6] = sign
        attrs[8] = "gene_name \"" + gene_name + "\";"
        return "\t".join(attrs)


    @staticmethod
    def create_line_by_name_and_region(name, region, gene_name='no_gene'):
        attrs = deepcopy(Line.DEFAULT_ATTR)
        attrs[0] = region.chr
        attrs[2] = name
        attrs[3] = region.start_pos
        attrs[4] = region.end_pos
        attrs[6] = "-" if region.negative_dir else "+"
        attrs[8] = "gene_name \"" + gene_name + "\";"

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
            attr[8] += (" \"" + ''.join(value) + "\"; ")
        return "\t".join(attr)

    @staticmethod
    def print_progres(current_progress, max_progress):
        """
        docstring
        """
        if current_progress%1000 == 0:
            sys.stderr.write("%.f%% done.\r" %(100.*current_progress/max_progress))
