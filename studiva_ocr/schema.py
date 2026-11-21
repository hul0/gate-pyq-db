"""
schema.py - Assembles and normalizes the canonical GATE paper JSON schema.
"""

from typing import List, Dict, Any, Optional

def normalize_paper_json(
    paper_id: str,
    year: int,
    subject: str,
    session: str,
    questions: List[Dict[str, Any]],
    answer_keys: Optional[Dict[int, Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Sorts, validates, and standardizes extracted questions into the canonical repository schema.
    """
    # Sort by question number
    questions_sorted = sorted(questions, key=lambda q: q.get("question_number", 0))

    normalized_questions = []
    cs_count = 0
    ga_count = 0

    for q in questions_sorted:
        q_num = q.get("question_number", 0)
        key_meta = answer_keys.get(q_num, {}) if answer_keys else {}

        # Section determination
        sec_code = key_meta.get("section_code")
        if not sec_code:
            sec_code = "GA" if q_num >= 56 else "CS"

        sec_name = key_meta.get("section")
        if not sec_name:
            sec_name = "General Aptitude" if sec_code == "GA" else "Computer Science and Information Technology"

        if sec_code == "GA":
            ga_count += 1
        else:
            cs_count += 1

        # Marks determination
        marks = float(key_meta.get("marks", 2.0 if (26 <= q_num <= 55 or q_num >= 61) else 1.0))
        q_type = key_meta.get("question_type", "MCQ")

        # Negative marks
        if q_type == "MCQ":
            neg = 0.66 if marks == 2.0 else 0.33
        else:
            neg = 0.0

        cat_prefix = "ga" if sec_code == "GA" else "cs"
        cat_marks = "2_mark" if marks == 2.0 else "1_mark"
        category = f"{cat_prefix}_{cat_marks}"

        qid = f"{paper_id}_{sec_code}_Q{q_num:02d}"

        # Clean answer and options
        ans = q.get("answer") or key_meta.get("key", "")
        correct_opts = [ans] if ans else []
        options = q.get("options")
        is_mcq = bool(options and isinstance(options, dict) and any(options.values()))

        # Media dict
        media = q.get("media")
        has_images = bool(media and isinstance(media, dict) and len(media) > 0)

        norm_q = {
            "id": qid,
            "category": category,
            "marks": marks,
            "negative_marks": neg,
            "section": sec_name,
            "section_code": sec_code,
            "paper_id": paper_id,
            "year": year,
            "session": session,
            "question_number": q_num,
            "question_type": q_type,
            "is_multiple_choice": is_mcq,
            "has_images": has_images,
            "page_start": q.get("page_start", 0),
            "page_end": q.get("page_end", 0),
            "question_text": q.get("question_text", "").strip(),
            "options": options if is_mcq else None,
            "answer": ans,
            "correct_options": correct_opts,
            "numerical_answer_range": None,
            "topic": q.get("topic") or "Computer Science",
            "subtopic": q.get("subtopic") or "",
            "difficulty_level": q.get("difficulty_level") or "Medium",
            "explaination": q.get("explaination", "").strip(),
            "tags": [sec_code, f"GATE_{year}", q.get("topic", "CS")]
        }

        if has_images:
            norm_q["media"] = media

        normalized_questions.append(norm_q)

    sections = []
    if cs_count > 0:
        sections.append({
            "name": "Computer Science and Information Technology",
            "code": "CS",
            "questions_count": cs_count
        })
    if ga_count > 0:
        sections.append({
            "name": "General Aptitude",
            "code": "GA",
            "questions_count": ga_count
        })

    return {
        "paper_id": paper_id,
        "year": year,
        "session": session,
        "subject": subject,
        "total_questions": len(normalized_questions),
        "sections": sections,
        "questions": normalized_questions
    }
