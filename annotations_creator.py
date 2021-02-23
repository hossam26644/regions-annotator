from line import Line

class AnnotationsCreator(object):

    def __init__(self, transcripts, transcript_keys=None):
        if transcript_keys is None:
            self.transcript_keys = list(transcript_keys.keys())
        else:
            self.transcript_keys = transcript_keys
        self.transcript_keys.sort(key=int)

        self.transcripts = transcripts
        self.intergenic_lines = []
        self.interonic_lines = []
        self.flanking_exons = []
        self.internal_exons = []
        self.UTRs = []
        self.analyze_intergenic()
        self.write_annotations()

    def analyze_intergenic(self):
        last_transcript_end = None

        for key in self.transcript_keys:
            transcript = self.transcripts[key]

            if last_transcript_end is None:
                last_transcript_end = transcript.end_pos
            else:
                self.intergenic_lines.append(Line.creat_line_by_name_and_corr("Intergenic",
                                                                              last_transcript_end,
                                                                              transcript.start_pos))
                last_transcript_end = transcript.end_pos

            self.analyze_interonics(transcript)

    def analyze_interonics(self, transcript):
        if transcript.is_pseudo:
            return
        else:
            self.creat_UTRs(transcript)
            if len(transcript.exons) > 1:
                self.creat_intronics(transcript)
            if len(transcript.CDSs) > 2:
                self.creat_flanking_and_internal_exons(transcript)

    def creat_flanking_and_internal_exons(self, transcript):
        transcript.CDSs.sort()
        transcript.CDSs[0].type = "flanking_exon"
        transcript.CDSs[-1].type = "flanking_exon"
        self.flanking_exons.append(str(transcript.CDSs[0]))
        self.flanking_exons.append(str(transcript.CDSs[-1]))
        for exon in transcript.CDSs[1:-1]:
            exon.type = "internal_exon"
            self.internal_exons.append(str(exon))



    def creat_intronics(self, transcript):
        transcript.exons.sort()
        last_exon_end = transcript.exons[0].end_pos
        for exon in transcript.exons[1:]:
            self.interonic_lines.append(Line.creat_line_by_name_and_corr("intron",
                                                                          last_exon_end,
                                                                          exon.start_pos,
                                                                          sign="-" if exon.negative_dir else "+"))
            last_exon_end = exon.end_pos

    def creat_UTRs(self, transcript):
        self.check_UTRs(transcript)
        for utr in transcript.UTRs:
            self.UTRs.append(Line.create_line_by_name_and_region("UTR", utr))

    def check_UTRs(self, transcript):
        if len(transcript.UTRs) >= 2:
            return
        else:
            pass
            #raise ValueError("transcript does not have 2 UTRs")

    def write_annotations(self):
        with open('somefile.txt', 'w') as the_file:
            the_file.write('\n'.join(self.intergenic_lines) + '\n')
            the_file.write('\n'.join(self.interonic_lines) + '\n')
            the_file.write('\n'.join(self.flanking_exons) + '\n')
            the_file.write('\n'.join(self.internal_exons) + '\n')
            the_file.write('\n'.join(self.UTRs))
