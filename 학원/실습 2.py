# ============================================================
# 3주차 강의자료 ⑤: 추상클래스 (Abstract Base Class)
# ============================================================
# "자식 클래스가 반드시 구현해야 할 메서드"를 강제하는 방법
# ============================================================

from abc import ABC, abstractmethod


# ── 추상클래스: 직접 객체를 만들 수 없다 ─────────────────────

class Payment(ABC):
    """결제 수단의 추상클래스"""

    @abstractmethod
    def pay(self, amount):
        """자식 클래스에서 반드시 구현해야 함"""
        pass


# ── 자식 클래스: pay()를 반드시 구현 ─────────────────────────

class CreditCard(Payment):
    def pay(self, amount):
        print(f"신용카드로 {amount}원 결제")


class KakaoPay(Payment):
    def pay(self, amount):
        print(f"카카오페이로 {amount}원 결제")


class Bitcoin(Payment):
    def pay(self, amount):
        print(f"비트코인으로 {amount}원 결제")


# ── 다형성: 어떤 결제 수단이든 동일하게 처리 ─────────────────

payments = [CreditCard(), KakaoPay(), Bitcoin()]

for p in payments:
    p.pay(10000)

# ── 추상클래스는 직접 객체 생성 불가 ─────────────────────────
# p = Payment()  # ← TypeError 발생!
# 반드시 자식 클래스에서 @abstractmethod를 구현해야 객체 생성 가능

# ── 정리 ─────────────────────────────────────────────────────
# ABC         : 추상클래스의 부모 (import 필요)
# @abstractmethod: 자식이 반드시 구현해야 하는 메서드 표시
# 추상클래스는 "설계도" 역할 → 직접 사용 X, 상속해서 사용 O
# ============================================================
