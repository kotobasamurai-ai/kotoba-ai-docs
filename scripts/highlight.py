#!/usr/bin/env python3
"""
画像の指定領域を強調するスクリプト。
指定領域以外を暗いオーバーレイで覆います。

使い方:
  python scripts/highlight.py <入力画像> <x1> <y1> <x2> <y2> [--output <出力先>] [--shade <透明度>]

例:
  python scripts/highlight.py images/quickstart/new_agent_card.png 406 228 810 432
  python scripts/highlight.py images/quickstart/new_agent_card.png 406 228 810 432 -o out.png
  python scripts/highlight.py images/quickstart/test_call_button.png 1970 4 2200 56 --shade 120
"""

import argparse
from PIL import Image, ImageDraw


def add_highlight(input_path, output_path, box, shade_alpha):
    img = Image.open(input_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle([0, 0, img.size[0], img.size[1]], fill=(0, 0, 0, shade_alpha))

    x1, y1, x2, y2 = box
    draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 0))

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(output_path)
    print(f"Saved: {output_path} (box: {box})")


def main():
    parser = argparse.ArgumentParser(description="画像の指定領域を強調する")
    parser.add_argument("input", help="入力画像パス")
    parser.add_argument("x1", type=int, help="強調領域の左上X")
    parser.add_argument("y1", type=int, help="強調領域の左上Y")
    parser.add_argument("x2", type=int, help="強調領域の右下X")
    parser.add_argument("y2", type=int, help="強調領域の右下Y")
    parser.add_argument("--output", "-o", help="出力先パス（省略時は入力を上書き）")
    parser.add_argument("--shade", type=int, default=140, help="オーバーレイの透明度 0-255 (default: 140)")

    args = parser.parse_args()
    output = args.output or args.input

    add_highlight(args.input, output, (args.x1, args.y1, args.x2, args.y2), args.shade)


if __name__ == "__main__":
    main()
