#!/usr/bin/env python3
"""The World Today — Sunday 22 November 2026.

A newspaper front page summing up the day's world news, drawn
entirely in code with PIL shapes and text (no network, no external
assets). It writes $MAKEFUN_OUTPUT_DIR/entry.png, or
/output/entry.png by default, and is deterministic: two runs
produce byte-identical files.
"""

import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import draw_frontpage as fp

PAGE_W, PAGE_H = fp.PAGE_W, fp.PAGE_H
MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), fp.PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ---------------------------------------------------
    title_f = fp.load_font(fp.SERIF_BOLD_PATH, 58)
    title = "THE WORLD TODAY"
    d.text(((PAGE_W - title_f.getlength(title)) / 2, 12), title,
           font=title_f, fill=fp.INK)
    fp.double_hline(d, MARGIN, PAGE_W - MARGIN, 84)

    date_f = fp.load_font(fp.SANS_BOLD_PATH, 27)
    date = "SUNDAY 22 NOVEMBER 2026"
    d.text(((PAGE_W - date_f.getlength(date)) / 2, 96), date,
           font=date_f, fill=fp.RED)
    side_f = fp.load_font(fp.SANS_PATH, 14)
    d.text((MARGIN, 104), "WORLD EDITION", font=side_f, fill=fp.GREY)
    tag = "ONE DAY  •  ONE PAGE"
    d.text((PAGE_W - MARGIN - side_f.getlength(tag), 104), tag,
           font=side_f, fill=fp.GREY)
    fp.hline(d, MARGIN, PAGE_W - MARGIN, 130, weight=2)

    # ---- lead story -------------------------------------------------
    kick_f = fp.load_font(fp.SANS_BOLD_PATH, 19)
    d.text((MARGIN, 142), "WASHINGTON  —  PENTAGON MOVES ON CANADA",
           font=kick_f, fill=fp.RED)
    head_f = fp.load_font(fp.SERIF_BOLD_PATH, 43)
    d.text((MARGIN, 168), "PENTAGON MOVES TO RESTRICT", font=head_f,
           fill=fp.INK)
    d.text((MARGIN, 214), "US–CANADA DEFENCE TIES", font=head_f, fill=fp.INK)

    ix, iy, iw, ih = MARGIN, 272, 560, 204
    fp.draw_pentagon_scene(img, ix, iy, iw, ih)
    tx = 608
    tw = PAGE_W - MARGIN - tx
    body_f = fp.load_font(fp.SERIF_PATH, 18)
    lead = ("The Pentagon is moving to restrict defence ties with "
            "Canada, AFP reported on 22 November — a sharp chill to "
            "one of the world's closest military partnerships.")
    y = fp.text_block(d, tx, iy + 2, lead, body_f, tw, spacing=24)
    # fact box under the lead text
    box_y = 404
    d.rectangle([tx, box_y, PAGE_W - MARGIN, box_y + 72], fill=fp.PANEL,
                outline=fp.RED, width=2)
    stat_f = fp.load_font(fp.SANS_BOLD_PATH, 16)
    d.text((tx + 12, box_y + 8), "REPORTED: AFP, 22 NOVEMBER",
           font=stat_f, fill=fp.DARK_RED)
    d.text((tx + 12, box_y + 31), "THE ALLIES: US AND CANADA",
           font=stat_f, fill=fp.DARK_RED)
    d.text((tx + 12, box_y + 54), "THE MOVE: DEFENCE TIES CUT BACK",
           font=stat_f, fill=fp.DARK_RED)

    # ---- divider -----------------------------------------------------
    fp.double_hline(d, MARGIN, PAGE_W - MARGIN, 498)

    # ---- three secondary stories -------------------------------------
    cards = [
        ("WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
         "The World Court finds Myanmar guilty of genocide against "
         "the Rohingya.",
         fp.draw_court_scene),
        ("IRAN STRIKES TANKERS AND A US BASE",
         "Iran strikes three tankers and a US air base in Kuwait "
         "and targets Bahrain amid wider attacks across the Gulf.",
         fp.draw_gulf_scene),
        ("TRUMP, XI AND PUTIN TALK NUKES",
         "Rare three-way talks on nuclear risks end with no "
         "breakthrough; Trump calls China's buildup "
         "\u201chot and heavy\u201d.",
         fp.draw_summit_scene),
    ]
    card_w = 312
    card_x = [MARGIN, MARGIN + 332, MARGIN + 664]
    card_y = 514
    illo_h = 104
    for (headline, body, draw_fn), cx in zip(cards, card_x):
        draw_fn(img, cx, card_y, card_w, illo_h)
        hy = card_y + illo_h + 10
        h_f = fp.load_font(fp.SERIF_BOLD_PATH, 19)
        hy = fp.text_block(d, cx, hy, headline, h_f, card_w, spacing=24)
        b_f = fp.load_font(fp.SANS_PATH, 15)
        fp.text_block(d, cx, hy + 6, body, b_f, card_w, spacing=20)

    # ---- divider -----------------------------------------------------
    fp.hline(d, MARGIN, PAGE_W - MARGIN, 754, weight=2)

    # ---- bottom row: three small stories ------------------------------
    small = [
        ("PERU QUAKE: 6.7–6.9, NO DEATHS",
         "A magnitude 6.7–6.9 earthquake strikes Peru's Andes. "
         "No deaths are reported.",
         fp.draw_quake_icon),
        ("RUSSIAN MISSILE CRASHES IN POLAND",
         "A Russian missile crashes in Poland. Warsaw calls it a "
         "provocation; NATO calls it a violation.",
         fp.draw_missile_icon),
        ("TRUMP VOWS 10% CARD RATE CAP",
         "Trump vows to work with Democrats to cap credit card "
         "interest rates at 10%.",
         fp.draw_card_icon),
    ]
    row_y = 770
    icon_s = 62
    for (headline, body, draw_fn), cx in zip(small, card_x):
        draw_fn(img, cx, row_y, icon_s)
        hx = cx + icon_s + 10
        hw = card_w - icon_s - 10
        h_f = fp.load_font(fp.SERIF_BOLD_PATH, 19)
        hy = fp.text_block(d, hx, row_y, headline, h_f, hw, spacing=23)
        b_f = fp.load_font(fp.SANS_PATH, 15)
        fp.text_block(d, cx, row_y + icon_s + 8, body, b_f, card_w,
                      spacing=20)

    # ---- briefs strip --------------------------------------------------
    by = 926
    d.rectangle([0, by, PAGE_W, PAGE_H], fill=fp.NAVY)
    brief_f = fp.load_font(fp.SANS_PATH, 15)
    brief_b = fp.load_font(fp.SANS_BOLD_PATH, 15)
    d.text((MARGIN, by + 12), "IN BRIEF", font=brief_b,
           fill=(255, 196, 66))
    bx = MARGIN + 96
    line1 = ("Taiwan warns PM Carney: deeper China ties carry risks.   "
             "Kim visits factories after \u201cTrump snub\u201d.")
    line2 = ("Houthis launch revenge strikes on the Saudi capital.   "
             "Storms bring historic flooding to Florida.")
    line3 = ("S. Korea's Lee: speed decides the AI race.   Protests "
             "hit Meta offices in India; 11 die of tainted alcohol "
             "in Manipur.")
    d.text((bx, by + 12), line1, font=brief_f, fill=(240, 240, 235))
    d.text((bx, by + 38), line2, font=brief_f, fill=(240, 240, 235))
    d.text((bx, by + 64), line3, font=brief_f, fill=(240, 240, 235))

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build_page()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
