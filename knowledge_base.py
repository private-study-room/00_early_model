# 지식 기반 시스템을 구현한 간단한 예제

# 1. 지식 베이스 정의 (증상에 따른 질병 규칙 정의)
knowledge_base = {
    "기침": ["감기", "천식"],
    "열": ["감기", "독감"],
    "몸살": ["독감"],
    "피로": ["감기", "빈혈"],
    "숨가쁨": ["천식", "폐렴"],
    "가슴 통증": ["폐렴"],
    "두통": ["빈혈", "편두통"],
}

# 2. 추론 엔진 구현 (전방향 추론 사용)
def infer_disease(symptoms):
    possible_diseases = {}

    # 입력된 증상에 따라 질병을 추론
    for symptom in symptoms:
        if symptom in knowledge_base:
            diseases = knowledge_base[symptom]
            for disease in diseases:
                # 질병이 이미 존재하면 발생 횟수 증가
                if disease in possible_diseases:
                    possible_diseases[disease] += 1
                else:
                    possible_diseases[disease] = 1

    # 발생 횟수가 많은 질병 순서대로 정렬하여 반환
    return sorted(possible_diseases.items(), key=lambda x: x[1], reverse=True)

# 3. 사용자 인터페이스 (증상 입력 및 결과 출력)
def diagnose():
    print("진단을 위해 증상을 입력하세요 (예: 기침, 열, 피로)")
    symptoms = input("증상 (쉼표로 구분하여 입력): ").split(", ")

    # 추론 엔진을 사용하여 질병을 추론
    possible_diseases = infer_disease(symptoms)

    # 진단 결과 출력
    if possible_diseases:
        print("\n가능성이 높은 질병 순위:")
        for disease, count in possible_diseases:
            print(f"- {disease} (관련 증상 수: {count})")
    else:
        print("\n해당 증상에 맞는 질병을 찾을 수 없습니다.")

# 진단 시스템 실행
diagnose()
