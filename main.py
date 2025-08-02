#!/usr/bin/env python3
# Usage:
#   python3 main.py input-resourcepack.zip example-beta-texturepack.zip [--output=out.zip]

import argparse
import zipfile
import sys
import os
from io import BytesIO

BETA_FOLDERS = {
    "armor/", "art/", "environment/", "gui/", "item/",
    "misc/", "mob/", "terrain/", "title/",  # from template beta‑1.7‑3 texturepack
}

def is_pack_meta(fn):
    # Beta 1.7.3 does not understand pack.mcmeta or version.json
    return fn.lower().endswith(".mcmeta") or fn.lower().endswith(".json")

def should_copy(fp):
    fn = fp.filename
    if is_pack_meta(fn):
        return False
    if fn.startswith("assets/"):
        return False
    return True

def normalize_path(fn):
    # Make sure that the files are in the correct folders
    parts = fn.replace("\\", "/").split("/")
    if parts[0] in BETA_FOLDERS:
        return fn
    else:
        return fn  # save as is

def convert(input_zip_path, example_zip_path, output_zip_path):
    with zipfile.ZipFile(input_zip_path, 'r') as zin,\
         zipfile.ZipFile(output_zip_path, 'w', compression=zipfile.ZIP_STORED) as zout:

        # Take the structure and names of files from the source
        for f in zin.infolist():
            if not should_copy(f):
                continue
            new_path = normalize_path(f.filename)
            buf = zin.read(f.filename)
            zout.writestr(new_path, buf)
        # Don't copy any unnecessary directories

    print(f"[OK] Beta-compatible .zip file created: {output_zip_path}")

def guess_output_name(name):
    base = os.path.splitext(os.path.basename(name))[0]
    return f"{base}_converted_b1.7.3.zip"

def main():
    p = argparse.ArgumentParser(description="Converting resource pack 1.2.5+ to Beta 1.7.3")
    p.add_argument("input_pack", help="the original zip resource pack (e.g., steelfeathers-enchanted-pack_v1.6-1.2.5.zip)")
    p.add_argument("example_beta_pack", help="example of a correct Beta 1.7.3 texture pack")
    p.add_argument("--output", "-o", help="name of the output .zip file")
    args = p.parse_args()

    if not args.output:
        args.output = guess_output_name(args.input_pack)
    convert(args.input_pack, args.example_beta_pack, args.output)

if __name__ == "__main__":
    main()
