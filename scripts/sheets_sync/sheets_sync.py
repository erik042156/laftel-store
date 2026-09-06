#!/usr/bin/env python3
"""
Google Spreadsheet 동기화 CLI.

tc-writing Skill(.claude/skills/tc-writing/SKILL.md)의 9개 컬럼 정의를 따르는
Markdown TC 문서(docs/tc/{feature-slug}.md)를 읽어 Google Spreadsheet에 반영한다.

지원 명령:
  list                        : 현재 Spreadsheet에 저장된 TC 목록을 조회한다.
  append                      : Markdown TC 문서의 TC를 Spreadsheet에 추가한다(append-only, 수정/삭제 없음).
  candidate-create-worksheet  : 자동화 후보 평가용 워크시트를 생성한다(이미 있으면 오류).
  candidate-sync              : Candidate 문서(docs/tc/automation-candidates/{slug}.md)의
                                 AI 작성 영역만 Spreadsheet에 반영한다(신규 TC는 새 행 추가,
                                 기존 TC는 AI 컬럼만 갱신. QA Decision/QA Comment는 건드리지 않음).
  candidate-list               : 자동화 후보 워크시트를 조회한다(QA Decision/QA Comment 포함).

이 스크립트는 tc-agent / automation-candidate-agent가 Bash로 호출하는 용도로만 설계되었으며,
행 수정(update)이 필요한 candidate-sync를 제외하면 기존 행을 수정하거나 삭제하는 기능은
의도적으로 제공하지 않는다(README.md 참조). candidate-sync조차 AI 작성 영역 컬럼 범위로만
쓰기가 제한되며, 사용자 작성 영역(QA Decision/QA Comment)은 절대 덮어쓰지 않는다.
"""

import argparse
import os
import re
import sys

TC_COLUMNS = [
    "ID",
    "Requirement ID",
    "Feature",
    "Test Scenario",
    "Preconditions",
    "Test Steps",
    "Expected Result",
    "Priority",
    "Result",
]

DEFAULT_WORKSHEET_NAME = "TC"

# automation-candidate-agent.md 산출물 템플릿의 "AI 평가 결과" 표 헤더와 정확히 일치해야 한다.
CANDIDATE_AI_COLUMNS = [
    "TC ID",
    "Business Criticality",
    "Regression Frequency",
    "Automation Stability",
    "Result Determinism",
    "Manual Test Cost",
    "Maintenance Cost",
    "Automation Score",
    "Candidate (AI)",
    "선정/제외 사유",
]

# 사용자(QA)가 Google Sheet에서 직접 입력하는 영역. AI는 이 컬럼을 절대 쓰지 않는다.
CANDIDATE_QA_COLUMNS = ["QA Decision", "QA Comment"]

CANDIDATE_FULL_COLUMNS = CANDIDATE_AI_COLUMNS + CANDIDATE_QA_COLUMNS

DEFAULT_CANDIDATE_WORKSHEET_NAME = "Automation Candidates"


def load_env():
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass


def get_client_and_sheet():
    load_env()

    service_account_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")

    missing = []
    if not service_account_file:
        missing.append("GOOGLE_SERVICE_ACCOUNT_FILE")
    if not sheet_id:
        missing.append("GOOGLE_SHEET_ID")
    if missing:
        print(
            "[오류] 다음 환경변수가 설정되어 있지 않습니다: " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "설정 방법은 scripts/sheets_sync/README.md를 참고하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.isfile(service_account_file):
        print(
            f"[오류] GOOGLE_SERVICE_ACCOUNT_FILE 경로에 파일이 없습니다: {service_account_file}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import gspread
    except ImportError:
        print(
            "[오류] gspread 패키지가 설치되어 있지 않습니다. "
            "scripts/sheets_sync/README.md의 설치 안내를 참고하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        gc = gspread.service_account(filename=service_account_file)
        sh = gc.open_by_key(sheet_id)
    except Exception as exc:  # noqa: BLE001 - CLI 최상위 예외를 사용자에게 그대로 보고
        print(f"[오류] Google Sheets 연결에 실패했습니다: {exc}", file=sys.stderr)
        sys.exit(1)

    return gc, sh


def get_or_create_worksheet(sh, create_if_missing, worksheet_name=None, columns=None, default_name=DEFAULT_WORKSHEET_NAME):
    columns = columns or TC_COLUMNS
    worksheet_name = worksheet_name or os.environ.get("GOOGLE_SHEET_WORKSHEET", default_name)
    try:
        ws = sh.worksheet(worksheet_name)
        return ws, worksheet_name, False
    except Exception:  # noqa: BLE001 - gspread.WorksheetNotFound 등
        if not create_if_missing:
            return None, worksheet_name, False
        ws = sh.add_worksheet(title=worksheet_name, rows=1000, cols=len(columns))
        ws.append_row(columns, value_input_option="USER_ENTERED")
        return ws, worksheet_name, True


def column_letter(index):
    """1-based 컬럼 인덱스를 스프레드시트 컬럼 문자로 변환한다 (1 -> A, 27 -> AA)."""
    letters = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(ord("A") + remainder) + letters
    return letters


def split_table_row(line):
    """마크다운 테이블 한 행을 셀 리스트로 분리한다 (이스케이프된 '\\|' 는 리터럴 '|' 로 처리)."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    raw_cells = re.split(r"(?<!\\)\|", line)
    return [cell.replace("\\|", "|").strip() for cell in raw_cells]


def is_separator_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", cell.strip()) for cell in cells if cell.strip() != "") and any(
        cell.strip() for cell in cells
    )


def parse_markdown_tables(markdown_text, expected_header):
    """Markdown 문서에서 expected_header와 정확히 일치하는 헤더를 가진 표를 모두 찾아
    데이터 행을 합쳐 반환한다(문서 안에 같은 형식의 표가 여러 개 있어도 모두 수집)."""
    lines = markdown_text.splitlines()
    rows = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("|"):
            header_cells = split_table_row(line)
            if header_cells == expected_header:
                # 다음 줄은 구분선(---) 이어야 함
                if i + 1 < n and lines[i + 1].strip().startswith("|"):
                    sep_cells = split_table_row(lines[i + 1])
                    if is_separator_row(sep_cells):
                        j = i + 2
                        while j < n and lines[j].strip().startswith("|"):
                            data_cells = split_table_row(lines[j])
                            if len(data_cells) == len(expected_header):
                                rows.append(dict(zip(expected_header, data_cells)))
                            j += 1
                        i = j
                        continue
        i += 1
    return rows


def parse_tc_tables(markdown_text):
    """Markdown 문서에서 TC 컬럼 정의(9개 컬럼)와 일치하는 표를 모두 찾아 데이터 행을 합쳐 반환한다."""
    return parse_markdown_tables(markdown_text, TC_COLUMNS)


def parse_candidate_ai_table(markdown_text):
    """Markdown 문서에서 Candidate "AI 평가 결과" 표(10개 컬럼)와 일치하는 표를 찾아 반환한다."""
    return parse_markdown_tables(markdown_text, CANDIDATE_AI_COLUMNS)


def cmd_list(args):
    _, sh = get_client_and_sheet()
    ws, worksheet_name, created = get_or_create_worksheet(
        sh, create_if_missing=False, worksheet_name=args.worksheet
    )

    if ws is None:
        print(f"워크시트 '{worksheet_name}'가 아직 없습니다. 반영된 TC가 없습니다.")
        return

    values = ws.get_all_values()
    if not values:
        print(f"워크시트 '{worksheet_name}'에 데이터가 없습니다.")
        return

    header = values[0]
    data_rows = values[1:]

    if args.ids_only:
        id_col = header.index("ID") if "ID" in header else 0
        for row in data_rows:
            if len(row) > id_col and row[id_col].strip():
                print(row[id_col].strip())
        return

    print(f"워크시트: {worksheet_name} (총 {len(data_rows)}건)")
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for row in data_rows:
        padded = row + [""] * (len(header) - len(row))
        print("| " + " | ".join(padded[: len(header)]) + " |")


def cmd_append(args):
    if not os.path.isfile(args.input):
        print(f"[오류] 입력 파일을 찾을 수 없습니다: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    new_rows = parse_tc_tables(markdown_text)
    if not new_rows:
        print(
            f"[오류] {args.input} 에서 TC 컬럼 정의와 일치하는 표를 찾지 못했습니다.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 입력 파일 내 ID 중복 검사
    seen = {}
    dups_in_file = []
    for row in new_rows:
        tc_id = row["ID"]
        if tc_id in seen:
            dups_in_file.append(tc_id)
        seen[tc_id] = True
    if dups_in_file:
        print(
            "[오류] 입력 파일 내에 중복된 TC ID가 있습니다: " + ", ".join(sorted(set(dups_in_file))),
            file=sys.stderr,
        )
        sys.exit(1)

    _, sh = get_client_and_sheet()
    ws, worksheet_name, created = get_or_create_worksheet(
        sh, create_if_missing=not args.dry_run, worksheet_name=args.worksheet
    )

    existing_ids = set()
    need_header_write = False
    if ws is not None:
        values = ws.get_all_values()
        is_fully_blank = not values or all(
            all(cell.strip() == "" for cell in row) for row in values
        )
        if is_fully_blank:
            # 완전히 빈 워크시트(사용자가 이름만 미리 만들어 둔 경우 포함) — 헤더가 없을 뿐이므로
            # 안전하게 헤더를 새로 쓴다. 데이터가 섞여 있는 상태는 아래 else 분기에서 그대로 검증한다.
            need_header_write = True
        else:
            header = values[0]
            if header != TC_COLUMNS:
                print(
                    "[오류] 기존 워크시트의 헤더가 TC 컬럼 정의와 다릅니다. "
                    "시트를 임의로 덮어쓰지 않고 중단합니다.",
                    file=sys.stderr,
                )
                print(f"  기존 헤더: {header}", file=sys.stderr)
                print(f"  기대 헤더: {TC_COLUMNS}", file=sys.stderr)
                sys.exit(1)
            id_col = header.index("ID")
            for row in values[1:]:
                if len(row) > id_col and row[id_col].strip():
                    existing_ids.add(row[id_col].strip())

    conflict_ids = [row["ID"] for row in new_rows if row["ID"] in existing_ids]
    if conflict_ids:
        print(
            "[오류] 이미 Spreadsheet에 존재하는 TC ID와 충돌합니다(append는 기존 행을 "
            "수정/삭제하지 않으므로 중단합니다): " + ", ".join(sorted(set(conflict_ids))),
            file=sys.stderr,
        )
        print(
            "기존 TC를 수정해야 하는 경우 사용자와 함께 반영 방법을 결정하세요 "
            "(README.md '승인완료 문서 재수정 시 처리' 참고).",
            file=sys.stderr,
        )
        sys.exit(1)

    if ws is None:
        sheet_note = " (신규 생성 예정)"
    elif need_header_write:
        sheet_note = " (기존 빈 워크시트, 헤더 신규 작성 예정)"
    else:
        sheet_note = ""

    print(f"입력 파일: {args.input}")
    print(f"대상 워크시트: {worksheet_name}{sheet_note}")
    print(f"추가될 TC 수: {len(new_rows)}건")
    print("추가될 TC ID: " + ", ".join(row["ID"] for row in new_rows))

    if args.dry_run:
        print("\n[dry-run] 실제로 Spreadsheet에 반영하지 않았습니다.")
        return

    if need_header_write:
        ws.update(range_name="A1", values=[TC_COLUMNS])

    rows_to_append = [[row[col] for col in TC_COLUMNS] for row in new_rows]
    ws.append_rows(rows_to_append, value_input_option="USER_ENTERED")
    print(f"\n{len(rows_to_append)}건을 워크시트 '{worksheet_name}'에 추가했습니다.")


def cmd_candidate_create_worksheet(args):
    _, sh = get_client_and_sheet()
    worksheet_name = args.worksheet or os.environ.get(
        "GOOGLE_SHEET_CANDIDATE_WORKSHEET", DEFAULT_CANDIDATE_WORKSHEET_NAME
    )
    try:
        sh.worksheet(worksheet_name)
        print(
            f"[오류] 워크시트 '{worksheet_name}'가 이미 존재합니다. "
            "기존 워크시트를 그대로 사용하세요(새로 만들지 않았습니다).",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception:  # noqa: BLE001 - gspread.WorksheetNotFound 등
        pass

    ws = sh.add_worksheet(title=worksheet_name, rows=1000, cols=len(CANDIDATE_FULL_COLUMNS))
    ws.append_row(CANDIDATE_FULL_COLUMNS, value_input_option="USER_ENTERED")
    print(f"워크시트 '{worksheet_name}'를 생성했습니다. (컬럼: {', '.join(CANDIDATE_FULL_COLUMNS)})")


def cmd_candidate_sync(args):
    if not os.path.isfile(args.input):
        print(f"[오류] 입력 파일을 찾을 수 없습니다: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    new_rows = parse_candidate_ai_table(markdown_text)
    if not new_rows:
        print(
            f"[오류] {args.input} 에서 Candidate 'AI 평가 결과' 표(10개 컬럼)와 일치하는 표를 찾지 못했습니다.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 입력 파일 내 TC ID 중복 검사
    seen = {}
    dups_in_file = []
    for row in new_rows:
        tc_id = row["TC ID"]
        if tc_id in seen:
            dups_in_file.append(tc_id)
        seen[tc_id] = True
    if dups_in_file:
        print(
            "[오류] 입력 파일 내에 중복된 TC ID가 있습니다: " + ", ".join(sorted(set(dups_in_file))),
            file=sys.stderr,
        )
        sys.exit(1)

    _, sh = get_client_and_sheet()
    worksheet_name = args.worksheet or os.environ.get(
        "GOOGLE_SHEET_CANDIDATE_WORKSHEET", DEFAULT_CANDIDATE_WORKSHEET_NAME
    )
    ws, worksheet_name, _created = get_or_create_worksheet(
        sh,
        create_if_missing=False,
        worksheet_name=worksheet_name,
        columns=CANDIDATE_FULL_COLUMNS,
        default_name=DEFAULT_CANDIDATE_WORKSHEET_NAME,
    )
    if ws is None:
        print(
            f"[오류] 워크시트 '{worksheet_name}'가 아직 없습니다. "
            "먼저 'candidate-create-worksheet'로 생성하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    values = ws.get_all_values()
    if not values:
        print(
            f"[오류] 워크시트 '{worksheet_name}'에 헤더가 없습니다. "
            "먼저 'candidate-create-worksheet'로 올바르게 생성하세요.",
            file=sys.stderr,
        )
        sys.exit(1)

    header = values[0]
    if header != CANDIDATE_FULL_COLUMNS:
        print(
            "[오류] 기존 워크시트의 헤더가 Candidate 컬럼 정의와 다릅니다. "
            "시트를 임의로 덮어쓰지 않고 중단합니다.",
            file=sys.stderr,
        )
        print(f"  기존 헤더: {header}", file=sys.stderr)
        print(f"  기대 헤더: {CANDIDATE_FULL_COLUMNS}", file=sys.stderr)
        sys.exit(1)

    id_col_index = header.index("TC ID")
    existing_row_of_id = {}
    for row_idx, row in enumerate(values[1:], start=2):  # 1행은 헤더, 데이터는 2행부터
        if len(row) > id_col_index and row[id_col_index].strip():
            existing_row_of_id[row[id_col_index].strip()] = row_idx

    rows_to_append = [row for row in new_rows if row["TC ID"] not in existing_row_of_id]
    rows_to_update = [row for row in new_rows if row["TC ID"] in existing_row_of_id]

    print(f"입력 파일: {args.input}")
    print(f"대상 워크시트: {worksheet_name}")
    print(f"신규 추가될 TC: {len(rows_to_append)}건" + (f" ({', '.join(r['TC ID'] for r in rows_to_append)})" if rows_to_append else ""))
    print(f"AI 영역만 갱신될 기존 TC: {len(rows_to_update)}건" + (f" ({', '.join(r['TC ID'] for r in rows_to_update)})" if rows_to_update else ""))
    print("(QA Decision / QA Comment는 이 명령으로 변경되지 않습니다.)")

    if args.dry_run:
        print("\n[dry-run] 실제로 Spreadsheet에 반영하지 않았습니다.")
        return

    last_ai_col_letter = column_letter(len(CANDIDATE_AI_COLUMNS))
    for row in rows_to_update:
        row_idx = existing_row_of_id[row["TC ID"]]
        values_for_row = [row[col] for col in CANDIDATE_AI_COLUMNS]
        ws.update(
            range_name=f"A{row_idx}:{last_ai_col_letter}{row_idx}",
            values=[values_for_row],
        )

    if rows_to_append:
        rows_payload = [
            [row[col] for col in CANDIDATE_AI_COLUMNS] + ["", ""] for row in rows_to_append
        ]
        ws.append_rows(rows_payload, value_input_option="USER_ENTERED")

    print(
        f"\n완료: 신규 {len(rows_to_append)}건 추가, 기존 {len(rows_to_update)}건 AI 영역 갱신 "
        f"(워크시트 '{worksheet_name}')."
    )


def cmd_candidate_list(args):
    _, sh = get_client_and_sheet()
    worksheet_name = args.worksheet or os.environ.get(
        "GOOGLE_SHEET_CANDIDATE_WORKSHEET", DEFAULT_CANDIDATE_WORKSHEET_NAME
    )
    ws, worksheet_name, _created = get_or_create_worksheet(
        sh,
        create_if_missing=False,
        worksheet_name=worksheet_name,
        columns=CANDIDATE_FULL_COLUMNS,
        default_name=DEFAULT_CANDIDATE_WORKSHEET_NAME,
    )

    if ws is None:
        print(f"워크시트 '{worksheet_name}'가 아직 없습니다. 평가된 TC가 없습니다.")
        return

    values = ws.get_all_values()
    if not values:
        print(f"워크시트 '{worksheet_name}'에 데이터가 없습니다.")
        return

    header = values[0]
    data_rows = values[1:]

    print(f"워크시트: {worksheet_name} (총 {len(data_rows)}건)")
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for row in data_rows:
        padded = row + [""] * (len(header) - len(row))
        print("| " + " | ".join(padded[: len(header)]) + " |")


def main():
    parser = argparse.ArgumentParser(description="TC Markdown 문서를 Google Spreadsheet에 동기화한다.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="Spreadsheet의 기존 TC 목록을 조회한다.")
    list_parser.add_argument(
        "--ids-only", action="store_true", help="TC ID만 한 줄에 하나씩 출력한다."
    )
    list_parser.add_argument(
        "--worksheet", default=None, help="대상 워크시트(탭) 이름 (기본값: GOOGLE_SHEET_WORKSHEET 환경변수 또는 'TC')"
    )
    list_parser.set_defaults(func=cmd_list)

    append_parser = subparsers.add_parser("append", help="Markdown TC 문서를 Spreadsheet에 추가한다.")
    append_parser.add_argument("--input", required=True, help="docs/tc/{feature-slug}.md 경로")
    append_parser.add_argument(
        "--dry-run", action="store_true", help="실제로 반영하지 않고 미리보기만 출력한다."
    )
    append_parser.add_argument(
        "--worksheet", default=None, help="대상 워크시트(탭) 이름 (기본값: GOOGLE_SHEET_WORKSHEET 환경변수 또는 'TC')"
    )
    append_parser.set_defaults(func=cmd_append)

    candidate_create_parser = subparsers.add_parser(
        "candidate-create-worksheet", help="자동화 후보 평가용 워크시트를 생성한다(이미 있으면 오류)."
    )
    candidate_create_parser.add_argument(
        "--worksheet",
        default=None,
        help=f"대상 워크시트(탭) 이름 (기본값: GOOGLE_SHEET_CANDIDATE_WORKSHEET 환경변수 또는 '{DEFAULT_CANDIDATE_WORKSHEET_NAME}')",
    )
    candidate_create_parser.set_defaults(func=cmd_candidate_create_worksheet)

    candidate_sync_parser = subparsers.add_parser(
        "candidate-sync",
        help="Candidate 문서의 AI 작성 영역을 Spreadsheet에 반영한다(QA Decision/QA Comment는 보존).",
    )
    candidate_sync_parser.add_argument(
        "--input", required=True, help="docs/tc/automation-candidates/{feature-slug}.md 경로"
    )
    candidate_sync_parser.add_argument(
        "--dry-run", action="store_true", help="실제로 반영하지 않고 미리보기만 출력한다."
    )
    candidate_sync_parser.add_argument(
        "--worksheet",
        default=None,
        help=f"대상 워크시트(탭) 이름 (기본값: GOOGLE_SHEET_CANDIDATE_WORKSHEET 환경변수 또는 '{DEFAULT_CANDIDATE_WORKSHEET_NAME}')",
    )
    candidate_sync_parser.set_defaults(func=cmd_candidate_sync)

    candidate_list_parser = subparsers.add_parser(
        "candidate-list", help="자동화 후보 워크시트를 조회한다(QA Decision/QA Comment 포함)."
    )
    candidate_list_parser.add_argument(
        "--worksheet",
        default=None,
        help=f"대상 워크시트(탭) 이름 (기본값: GOOGLE_SHEET_CANDIDATE_WORKSHEET 환경변수 또는 '{DEFAULT_CANDIDATE_WORKSHEET_NAME}')",
    )
    candidate_list_parser.set_defaults(func=cmd_candidate_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
