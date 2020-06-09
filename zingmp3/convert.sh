cd data/;
for f in *.mp3; do ffmpeg -i "$f" -acodec pcm_u8 -ar 12000 "${f/%mp3/wav}"; rm "$f"; done