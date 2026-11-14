"""F-03~F-06 퀴즈. 출제 선정·FSRS·학습 기록 저장은 호출자의 책임이다."""

import argparse
import json


def normalize_answer(text):
    """화면에 표시할 원문은 보존하고, 비교할 때만 공백을 제거한다."""
    return "".join(text.split())


def validate_words(words):
    """영어 키 → meanings 목록 형식인지 확인한다. 잘못된 데이터는 거부한다."""
    if not isinstance(words, dict):
        raise ValueError("단어 데이터는 JSON 객체여야 합니다.")
    for english, info in words.items():
        if not isinstance(english, str) or not english.strip():
            raise ValueError("영어 단어는 비어 있지 않은 문자열이어야 합니다.")
        if english != english.strip().lower():
            raise ValueError("영어 키는 앞뒤 공백 없는 소문자로 저장해 주세요.")
        if not isinstance(info, dict):
            raise ValueError(f"{english}: 단어 정보는 객체여야 합니다.")
        meanings = info.get("meanings")
        if not isinstance(meanings, list) or not meanings:
            raise ValueError(f"{english}: meanings는 비어 있지 않은 목록이어야 합니다.")
        if any(not isinstance(m, str) or not normalize_answer(m) for m in meanings):
            raise ValueError(f"{english}: 뜻은 비어 있지 않은 문자열이어야 합니다.")


def reject_duplicate_keys(pairs):
    """JSON의 동일 키가 조용히 덮어써지는 일을 방지한다."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON에 중복 키가 있습니다: {key}")
        result[key] = value
    return result


def load_words(path):
    """UTF-8 JSON을 읽고 검증한다. 파일·디코딩·형식 오류는 호출자에게 전달한다."""
    with open(path, encoding="utf-8-sig") as file:
        words = json.load(file, object_pairs_hook=reject_duplicate_keys)
    validate_words(words)
    return words


def is_correct(answer, meanings):
    normalized = normalize_answer(answer)
    return bool(normalized) and any(
        normalized == normalize_answer(meaning) for meaning in meanings
    )


def show_results(results, write=print):
    correct_count = sum(result["correct"] for result in results)
    write(f"전체 {len(results)}문제 | 정답 {correct_count} | 오답 {len(results) - correct_count}")
    for number, result in enumerate(results, 1):
        label = "정답" if result["correct"] else "오답"
        write(f"{number}. {result['english']} | 입력: {result['answer']!r} | {label} | {result['rating']}")
        if not result["correct"]:
            write("등록 뜻: " + ", ".join(result["meanings"]))


def run_quiz(words, selected_words, read=input, write=print):
    """선정된 영어 키 순서로 진행. 확정 결과 list, 대상 없음 [], 취소 None 반환.

    words를 변경하지 않는다. selected_words는 복습 모듈이 결정하며,
    중복 키를 제거한 첫 15개를 사용한다. 존재하지 않는 키는 ValueError다.
    """
    validate_words(words)
    if isinstance(selected_words, (str, bytes)):
        raise ValueError("선정 단어는 영어 키 목록으로 전달해 주세요.")
    selected = []
    for english in selected_words:
        if not isinstance(english, str) or english not in words:
            raise ValueError(f"등록되지 않은 출제 단어: {english}")
        if english not in selected:
            selected.append(english)
    selected = selected[:15]
    if not words:
        write("등록된 단어가 없습니다. 먼저 단어를 등록해 주세요.")
        return []
    if not selected:
        write("현재 출제 가능한 문제가 없습니다.")
        return []

    results = []
    try:
        for number, english in enumerate(selected, 1):
            answer = read(f"[{number}/{len(selected)}] {english}의 한국어 뜻: ")
            meanings = words[english]["meanings"]
            correct = is_correct(answer, meanings)
            write("정답입니다." if correct else "오답입니다. 등록 뜻: " + ", ".join(meanings))
            results.append({
                "english": english, "answer": answer, "correct": correct,
                "meanings": list(meanings), "rating": "Good" if correct else "Again",
            })
        show_results(results, write)
        while True:
            choice = read("평가를 바꿀 정답 번호 (Enter: 최종 확정): ").strip()
            if not choice:
                write("평가를 확정했습니다.")
                return results
            try:
                index = int(choice) - 1
            except ValueError:
                write("문제 번호를 입력해 주세요.")
                continue
            if not 0 <= index < len(results) or not results[index]["correct"]:
                write("정답인 문제 번호를 선택해 주세요. 오답은 Again입니다.")
                continue
            rating = read("평가 선택 (1: Hard, 2: Good, 3: Easy): ").strip()
            ratings = {"1": "Hard", "2": "Good", "3": "Easy"}
            if rating not in ratings:
                write("평가는 1, 2, 3 중 선택해 주세요.")
                continue
            results[index]["rating"] = ratings[rating]
            write(f"{results[index]['english']}: {results[index]['rating']}")
    except (KeyboardInterrupt, EOFError):
        write("퀴즈를 취소했습니다. 학습 상태에 반영하지 않습니다.")
        return None


def main():
    parser = argparse.ArgumentParser(description="선정된 단어로 퀴즈를 실행합니다. FSRS·저장은 아직 연결되지 않았습니다.")
    parser.add_argument("path", help="단어 JSON 파일")
    parser.add_argument("words", nargs="*", help="출제할 영어 키 (순서대로)")
    parser.add_argument("--demo", action="store_true", help="샘플 실행: 파일 순서로 최대 15문제")
    args = parser.parse_args()
    if not args.demo and not args.words:
        parser.error("출제할 영어 키를 지정하거나 --demo를 사용해 주세요.")
    if args.demo and args.words:
        parser.error("--demo와 출제할 영어 키는 함께 지정할 수 없습니다.")
    try:
        words = load_words(args.path)
        run_quiz(words, list(words) if args.demo else args.words)
    except (OSError, ValueError) as error:
        parser.exit(1, f"퀴즈를 시작할 수 없습니다: {error}\n")


if __name__ == "__main__":
    main()
