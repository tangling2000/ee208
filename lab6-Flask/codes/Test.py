from whoosh.index import open_dir

dirname = "index"
ix = open_dir(dirname=dirname)

print(ix.doc_count())