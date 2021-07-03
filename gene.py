from line import Line
from transcript import  Transcript

class Gene(Line):
    ANALYZED_CATEGORIES = ['CDS', 'UTR', 'exon']
    def __new__(cls, line):
        if line.attrs['gene_type'] == 'protein_coding' and line.attrs['level'] in ['1', '2']:
            return super(Gene, cls).__new__(cls)
        return None

    def __init__(self, line):
        super(Gene, self).__init__(line)
        self.transcript = None
        self.type = 'None'

    def add_line(self, line):
        if line.type == "transcript":
            self.add_transcript(line)
        elif line.type in Gene.ANALYZED_CATEGORIES and self.transcript:
            # there is a transcript and subcategories are analyzed
            if line.attrs['transcript_id'] == self.transcript.attrs['transcript_id']:
                self.transcript.add_line(line)

    def add_transcript(self, line):
        if line.attrs["transcript_type"] == "protein_coding" and \
           line.attrs["level"] in ['1', '2']: # initial transcript acceptance categories

            if not self.transcript:
                self.check_first_transcript(line)

            else:
                if self.type == 'only_transcript':
                    self.type = 'first_transcript'
                self.check_more_trusted_transcript(line)

    def check_first_transcript(self, line):
        if "CCDS" in line.attrs['tags']: #check that it's a member of the consensus CDS gene set
            self.transcript = Transcript(line)
            if 'MANE_Select' in self.transcript.attrs['tags']: #the transcript belongs to the MANE Select data set
                self.type = 'MANE_Select'
            else:
                self.type = 'only_transcript'
        else:
            self.type = 'one_rejected_transcript'

    def check_more_trusted_transcript(self, line):

        if self.check_MANE_dataset(line):
            #if line or self.transcript is a member of MANE dataset use it
            return

        if self.check_CCDS(line):
            # if candidate transcript has CCDS while self.transcript doesnt, or vice versa
            return

        try:
            if self.check_support_level(line):
                return

        except KeyError: # no support level for one of the two values
            if self.check_level(line):
                return

        except ValueError: #support level for one is NA
            if self.use_the_non_NA_transcript_supported(line):
                return

        if self.check_length(line):
            return

    def check_MANE_dataset(self, line):
        if 'MANE_Select' in self.transcript.attrs['tags']:
            self.type = 'MANE_Select'
            return True

        elif 'MANE_Select' in line.attrs['tags']:
            self.transcript = Transcript(line)
            self.type = 'MANE_Select'
            return True

        return False

    def check_CCDS(self, line):
        if "CCDS" in line.attrs['tags'] and "CCDS" not in self.transcript.attrs['tags']:
            self.transcript = Transcript(line)
            self.type = 'CCDS'
            return True

        elif "CCDS" not in line.attrs['tags'] and "CCDS" in self.transcript.attrs['tags']:
            return True

        return False

    def check_support_level(self, line):
        line_transcript_support_level = int(line.attrs['transcript_support_level'])
        original_trnascript_support_level = int(self.transcript.attrs['transcript_support_level'])

        if line_transcript_support_level < original_trnascript_support_level:
            self.transcript = Transcript(line)
            self.type = 'transcript_support_level'
            return True

        return False

    def check_level(self, line):
        if int(line.attrs['level']) < int(self.transcript.attrs['level']):
            self.transcript = Transcript(line)
            self.type = 'level'
            return True

        return False

    def use_the_non_NA_transcript_supported(self, line):
        if line.attrs['transcript_support_level'] == 'NA':
            return True

        if self.transcript.attrs['transcript_support_level'] == 'NA':
            self.transcript = Transcript(line)
            self.type = 'transcript_support_level'
            return True

        return False

    def check_length(self, line):
        alt_transcript = Transcript(line)
        if alt_transcript.length > self.transcript.length:
            self.type = 'length'
            self.transcript = alt_transcript
            return True
        return False
