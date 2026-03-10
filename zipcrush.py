import argparse
import zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps

parser = argparse.ArgumentParser()
parser.add_argument('file', type=Path)
parser.add_argument('-o', '--out', default='$FILE-crush.jpg')
parser.add_argument('-l', '--limit', type=int, default=2953)
args = parser.parse_args()

output = Path(args.out.replace('$FILE', args.file.stem))

original = Image.open(args.file).convert('RGB')
width, height = original.size

if height <= width:
	hi = width // 8
	ratio = width / height
	def dim(index):
		return index * 8, int(index / ratio) * 8
else:
	hi = height // 8
	ratio = height / width
	def dim(index):
		return int(index / ratio) * 8, index * 8
	
buffer = BytesIO()
image_data = None
lo = 0

while lo < hi:
	index = (lo + hi) // 2
	width, height = dim(index)
	image = ImageOps.fit(original, (width, height), Image.LANCZOS)
	# buffer.seek(0)
	buffer.truncate()
	image.save(buffer, 'JPEG', quality=1, optimize=True)
	file_size = buffer.tell()
	buffer.seek(0)
	zip_buffer = BytesIO()
	with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as z:
		z.writestr('0.jpg', buffer.getvalue())
	
	zip_size = zip_buffer.tell()
	over_limit = zip_size > args.limit
	print(f"{index}. {width} x {height}: {file_size} bytes, {zip_size} zipped {'' if over_limit else ' *'}")
	
	if over_limit:
		hi = index
	else:
		lo = index + 1
		image_data = buffer
		buffer = BytesIO()


image_data.seek(0)

with open(output, 'wb') as f:
    f.write(image_data.read())
