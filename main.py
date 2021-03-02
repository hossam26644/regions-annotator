from transcript import  Transcript, Transcripts
from line import Line
from annotations_creator import AnnotationsCreator

with open("hg38.refGene.gtf") as f:
    LINES = f.readlines()

transcripts = Transcripts()

for idx, line in enumerate(LINES):
    line = Line(line)

    if line.type == "transcript":

        if transcripts.is_location_availble(line):
            transcripts.add_transcript(line)
        else:
            transcripts.use_longer_transcript(line)

    else:
        transcripts.add_line(line)

    Line.print_progres(idx, len(LINES))

AnnotationsCreator(transcripts)
