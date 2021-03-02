from line import Line

class Transcript(Line):

    def __init__(self, line):
        self.written_line = line.written_line
        self.chr = line.chr
        self.start_pos = line.start_pos
        self.end_pos = line.end_pos
        self.length = int(self.end_pos) - int(self.start_pos)
        self.negative_dir = line.negative_dir
        self.gene_id = line.attrs['gene_id']
        self.transcript_id = line.attrs['transcript_id']
        self.gene_name = line.attrs['gene_name']
        self.is_pseudo = True
        self.CDSs = []
        self.exons = []
        self.UTRs5 = []
        self.UTRs3 = []
        self.line_types = {"exon":self.add_exon,
                           "CDS": self.add_CDS,
                           "5UTR":self.add_5UTR,
                           "3UTR":self.add_3UTR,
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

    def add_3UTR(self, line):
        self.UTRs3.append(line)

    def add_5UTR(self, line):
        self.UTRs5.append(line)

    def add_start_codon(self, line):
        pass

    def add_stop_codon(self, line):
        pass

class Transcripts(object):

    def __init__(self):
        self.transcripts = {} #dict of chromosome names (keys), and a list of dictionaries
                              #of transcript start sites (keys) and transcripts (values)
        self.current_transcript = None

    def is_location_availble(self, line):
        '''checks if there is another transcript starts from the same site'''
        self.check_chrom(line.chr)
        if line.start_pos in self.transcripts[line.chr]:
            return False
        return True

    def add_transcript(self, line):
        self.check_chrom(line.chr)
        transcript = Transcript(line)
        self.transcripts[transcript.chr][transcript.start_pos] = transcript
        self.current_transcript = transcript


    def use_longer_transcript(self, new_transc_line):
        self.current_transcript = Transcript(new_transc_line)
        original_transcript = self.transcripts[new_transc_line.chr][new_transc_line.start_pos]
        if new_transc_line.length > original_transcript.length:
            self.transcripts[new_transc_line.chr][new_transc_line.start_pos] = self.current_transcript

    def check_chrom(self, chrome):
        try:
            self.transcripts[chrome]
        except KeyError:
            self.transcripts[chrome] = {}

    def add_line(self, line):
        self.current_transcript.add_line(line)
