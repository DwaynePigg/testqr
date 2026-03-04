import argparse
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps

parser = argparse.ArgumentParser()
parser.add_argument('file', type=Path)
parser.add_argument('-o', '--out', default='$FILE-crush.jpg')
parser.add_argument('-l', '--limit', type=int, default=2953)
args = parser.parse_args()

original = Image.open(args.file).convert('RGB')
dim = min(original.size) // 8 * 8
output = Path(args.out.replace('$FILE', args.file.stem))
buf = BytesIO()

while True:
	img = ImageOps.fit(original, (dim, dim), Image.LANCZOS)
	img.save(buf, 'JPEG', quality=1, optimize=True)
	size = buf.tell()
	print(dim, size)
	buf.seek(0)
	if size <= args.limit:
		break
	dim -= 8
	buf.truncate()

with open(output, 'wb') as f:
    f.write(buf.read())
