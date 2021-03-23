from line import Line

class Transcript(Line):

    def __init__(self, line):

        super(Transcript, self).__init__(line)

        self.length = int(self.end_pos) - int(self.start_pos)
        self.gene_id = line.attrs['gene_id']
        self.transcript_id = line.attrs['transcript_id']
        self.gene_name = line.attrs['gene_name']

        self.is_pseudo = True
        self.CDSs = []
        self.exons = []
        self.UTRs = []
        self.UTRs5 = []
        self.UTRs3 = []
        self.line_types = {"exon":self.add_exon,
                           "CDS": self.add_CDS,
                           "UTR":self.add_UTR,
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

    def add_3UTR(self, line):
        self.UTRs3.append(line)

    def add_5UTR(self, line):
        self.UTRs5.append(line)

    def add_start_codon(self, line):
        pass

    def add_stop_codon(self, line):
        pass

    def split_UTRs(self):
        self.CDSs.sort()

        for UTR in self.UTRs:
            if UTR.start_pos < self.CDSs[0].start_pos and not self.negative_dir:
                self.UTRs5.append(UTR)
            elif UTR.start_pos > self.CDSs[0].start_pos and self.negative_dir:
                self.UTRs5.append(UTR)
            else:
                self.UTRs3.append(UTR)

class Transcripts(object):

    def __init__(self):
        self.transcripts = {} #dict of chromosome names (keys), and a list of dictionaries
                              #of transcript start sites (keys) and transcripts (values)

    def add_transcript(self, transcript):
        self.check_chrom(transcript.chr)
        self.transcripts[transcript.chr][transcript.start_pos] = transcript

    def check_chrom(self, chrome):
        try:
            self.transcripts[chrome]
        except KeyError:
            self.transcripts[chrome] = {}
