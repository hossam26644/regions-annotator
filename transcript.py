from line import Line

class Transcript(Line):

    def __init__(self, line):
        self.written_line = line.written_line
        self.chr = line.chr
        self.start_pos = line.start_pos
        self.end_pos = line.end_pos
        self.negative_dir = line.negative_dir
        self.gene_id = line.attrs['gene_id']
        self.transcript_id = line.attrs['transcript_id']
        self.gene_name = line.attrs['gene_name']
        self.is_pseudo = True
        self.CDSs = []
        self.exons = []
        self.UTRs = []
        self.line_types = {"exon":self.add_exon,
                           "CDS": self.add_CDS,
                           "5UTR":self.add_UTR,
                           "3UTR":self.add_UTR,
                           "start_codon":self.add_start_codon,
                           "stop_codon":self.add_stop_codon}

    def add_line(self, line):
        if line.attrs['transcript_id'] == self.transcript_id:
            self.line_types[line.type](line)

    def add_exon(self, line):
        self.exons.append(line)

    def add_CDS(self, line):
        self.is_pseudo = False
        self.CDSs.append(line)

    def add_UTR(self, line):
        self.UTRs.append(line)

    def add_start_codon(self, line):
        pass

    def add_stop_codon(self, line):
        pass

