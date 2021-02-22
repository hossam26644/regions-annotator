from transcript import  Transcript
from line import Line
from annotations_creator import AnnotationsCreator
with open("hg38.refGene.gtf") as f:
    LINES = f.readlines()

transcripts = {}
transcript_keys = []
current_transcript = None

for line in LINES:
    line = Line(line)
    if line.chr == "chr1" and line.type == "transcript":
        current_transcript = Transcript(line)
        if current_transcript.start_pos not in transcripts:
            transcripts[current_transcript.start_pos] = current_transcript
            transcript_keys.append(current_transcript.start_pos)

        else:
            transcripts[current_transcript.start_pos] = max(current_transcript,
                                                            transcripts[current_transcript.start_pos])
    else:
        current_transcript.add_line(line)

AnnotationsCreator(transcripts, transcript_keys)
