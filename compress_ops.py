import gzip, os, glob, sys
for i in glob.glob('./*.pickle'):
    try:
        with open(i, 'rb') as f:
            data = gzip.decompress(f.read())
            with open(i, 'wb') as r:
                r.write(data)
            sys.exit()
    except Exception:
        pass

for i in glob.glob('./*.pickle'):
    try:
        with open(i, 'rb') as f:
            data = gzip.compress(f.read())
            with open(i, 'wb') as r:
                r.write(data)
            sys.exit()
    except Exception:
        pass