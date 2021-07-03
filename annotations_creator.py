from line import Line

class AnnotationsCreator(object):

    def __init__(self, transcripts, filename='somefile.txt'):
        filename="cairoGP.gtf"
        self.transcripts = transcripts
        transcripts_dic = transcripts.transcripts
        self.clear_file(filename)
        '''
        for chromosome in transcripts_dic.keys():
            self.transcripts = transcripts_dic[chromosome]
            self.transcript_keys = list(self.transcripts.keys())
            self.transcript_keys.sort(key=int)

            self.intergenic_lines = []
            self.interonic_lines = []
            self.flanking_exons = []
            self.internal_exons = []
            self.one_exons = []
            self.first_of_twos = []
            self.second_of_twos = []
            self.UTRs5 = []
            self.UTRs3 = []
            self.analyze_intergenic()
        '''
        self.write_annotations(filename)

    def analyze_intergenic(self):
        last_transcript_end = None
        last_transcript_neg = None

        for key in self.transcript_keys:
            transcript = self.transcripts[key] #loop through certain chrom transcripts in order

            if last_transcript_end is None:
                last_transcript_end = transcript.end_pos
                last_transcript_neg = transcript.negative_dir

            else:
                sign = "-" if last_transcript_neg and transcript.negative_dir else "+"

                self.intergenic_lines.append(Line.creat_line_by_name_and_corr(transcript.chr,
                                                                              "Intergenic",
                                                                              last_transcript_end,
                                                                              transcript.start_pos,
                                                                              sign=sign))
                last_transcript_end = transcript.end_pos
                last_transcript_neg = transcript.negative_dir

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
            else:
                self.creat_one_or_two_exons(transcript)

    def creat_one_or_two_exons(self, transcript):
        if len(transcript.CDSs) == 1:
            transcript.CDSs[0].type = "one_exon"
            self.one_exons.append(str(transcript.CDSs[0]))
        elif len(transcript.CDSs) == 2:
            transcript.CDSs.sort(reverse=transcript.negative_dir)
            transcript.CDSs[0].type = "first_of_twos"
            transcript.CDSs[-1].type = "second_of_twos"
            self.first_of_twos.append(str(transcript.CDSs[0]))
            self.second_of_twos.append(str(transcript.CDSs[1]))

    def creat_flanking_and_internal_exons(self, transcript):
        transcript.CDSs.sort(reverse=transcript.negative_dir)
        transcript.CDSs[0].type = "first_coding_exon"
        transcript.CDSs[-1].type = "last_coding_exon"
        self.flanking_exons.append(str(transcript.CDSs[0]))
        self.flanking_exons.append(str(transcript.CDSs[-1]))
        for exon in transcript.CDSs[1:-1]:
            exon.type = "internal_exon"
            self.internal_exons.append(str(exon))

    def creat_intronics(self, transcript):
        transcript.exons.sort()
        last_exon_end = transcript.exons[0].end_pos
        for exon in transcript.exons[1:]:
            self.interonic_lines.append(Line.creat_line_by_name_and_corr(exon.chr,
                                                                         "intron",
                                                                         last_exon_end,
                                                                         exon.start_pos,
                                                                         sign="-" if exon.negative_dir else "+",
                                                                         gene_name=transcript.gene_name))
            last_exon_end = exon.end_pos

    def creat_UTRs(self, transcript):
        transcript.split_UTRs()
        for utr in transcript.UTRs5:
            self.UTRs5.append(Line.create_line_by_name_and_region("5UTR", utr,
                                                                  transcript.gene_name))
        for utr in transcript.UTRs3:
            self.UTRs3.append(Line.create_line_by_name_and_region("3UTR", utr,
                                                                  transcript.gene_name))

    def write_annotations(self, filename):
        with open(filename, 'a') as the_file:
            for chromosome in self.transcripts.transcripts.keys():
                transcripts = self.transcripts.transcripts[chromosome]
                for transcript in transcripts.values():
                    for cds in transcript.CDSs:
                        the_file.write(cds.written_line)

    def get_annotation_string(self, annotation):
        if annotation == []:
            return ''
        return ('\n'.join(annotation) + '\n')

    def clear_file(self, filename):
        with open(filename, 'w') as the_file:
            the_file.write('')
