from transcript import  Transcript, Transcripts
from gene import Gene
from line import Line
from annotations_creator import AnnotationsCreator

with open("gencode.v37.annotation.gtf") as f:
    LINES = f.readlines()

current_gene = None

types = {'None':0,
         'first_transcript':0,
         'MANE_Select':0,
         'CCDS':0,
         'transcript_support_level':0,
         'level':0,
         'length':0,
         'only_transcript':0,
         'one_rejected_transcript':0}
transcripts = Transcripts()

for idx, line in enumerate(LINES):
    line = Line(line)

    if line.type == "gene":

        if current_gene and current_gene.transcript:
            types[current_gene.type] += 1
            transcripts.add_transcript(current_gene.transcript)

        current_gene = Gene(line)

    elif current_gene:
        current_gene.add_line(line)
        #transcripts.add_line(line)

    Line.print_progres(idx, len(LINES))

print(types)
AnnotationsCreator(transcripts)
