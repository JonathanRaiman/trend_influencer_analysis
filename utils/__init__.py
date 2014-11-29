import gzip, datetime, re, io
from collections import Counter

to_time = datetime.datetime.fromtimestamp
splitter = re.compile("([ \.\)\(:;\"\[\]’,/\\\!?“»”…-])")

class Document:
    def __init__(self, doc_id, date, title, content, count):
        self.count = count
        self.date = date
        self.doc_id = doc_id
        self.title = title
        self.content = content

    def __str__(self):
        return (
            "<Document count=%d date=%r id=%d title=\"%s\" content=\"%s\">" % (
                self.count,
                self.date,
                self.doc_id,
                self.title,
                (self.content[0:50] + "..." + self.content[-50:]) if len(self.content) > 100 else self.content))

    def __repr__(self):
        return str(self)

def read_documents(path):
    docs = []
    with gzip.open(path, "rt") as f:
        for k, line in enumerate(f):
            if k > 0:
                (doc_id, doc_hash, date, influencers, title, content) = line.split("\t")
                docs.append(Document(int(doc_id), to_time(int(date)), title, content[:-1], influencers.count(" ") + 1))

    return docs

def get_word_counts(docs):
    counter = Counter()
    for doc in docs:
        counter.update([a for a in re.split(splitter, doc.content) if a != " " and len(a) > 1])
    return counter

def get_bigram_counts(docs):
   
    counter = Counter()
    for doc in docs:
        words = [a for a in re.split(splitter, doc.content) if a != " " and len(a) > 1]
        counter.update((words[i],words[i+1]) for i in range(len(words)-1))
    return counter

def get_textfile_word_counts(path, BUFF_SIZE=500):
    counter = Counter()
    with open(path, "rb", buffering=0) as f:
        reader = io.BufferedReader(f)
        line = b''
        while True:
            newline = reader.read(BUFF_SIZE)
            if len(newline) > 0:
                line += reader.read(BUFF_SIZE)
                right_end = line.rfind(b' ')
                counter.update(line[0:right_end].decode("utf-8").split(" "))
                line = line[right_end+1:]
            else:
                counter.update(line.decode("utf-8").split(" "))
                break
    return counter
    