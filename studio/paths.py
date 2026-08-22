# -*- coding: utf-8 -*-
"""경로 설정 — 모든 스크립트는 여기서만 경로를 가져온다.

환경변수로 덮어쓸 수 있다.
  CARDNEWS_OUT   산출물 루트 (기본: <repo>/out)
  CARDNEWS_DIST  갤러리 빌드 결과 (기본: <repo>/dist)
  CARDNEWS_DRIVE 구글드라이브 로컬 동기화 폴더 (선택, 지정 시 스캔 대상에 추가)
"""
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

OUT_ROOT = pathlib.Path(os.environ.get("CARDNEWS_OUT", ROOT / "out"))
DIST = pathlib.Path(os.environ.get("CARDNEWS_DIST", ROOT / "dist"))
DRIVE = os.environ.get("CARDNEWS_DRIVE")

ENGINE = ROOT / "engine"
CONTENTS = ROOT / "contents"
GALLERY = ROOT / "gallery"
DOCS = ROOT / "docs"

# 갤러리가 편 폴더를 찾는 위치 (앞에 있는 것이 우선)
SOURCE_DIRS = [OUT_ROOT] + ([pathlib.Path(DRIVE)] if DRIVE else [])

OUT_ROOT.mkdir(parents=True, exist_ok=True)
