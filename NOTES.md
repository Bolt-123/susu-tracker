# Architecture Decisions & Assumptions

## Architectural Assumptions & Decisions

1. **Membership Lock**:
   * **Rule**: Members can only join before payments begin.
   * **Reasoning**: Once Week 1 payments start, allowing new members mid-cycle would alter the total pot size and complicate rotating payout ordering. Locking membership ensures predictable financial planning.

2. **Strict Overpayment Rejection**:
   * **Rule**: If a member attempts to pay more than their outstanding balance for the current week, the entire payment is rejected.
   * **Reasoning**: This complies directly with requirement guidelines and prevents unmanaged credit balances across payment cycles.

3. **Partial Payment Handling**:
   * **Rule**: Partial payments are accumulated toward a member's weekly target. A week cannot close until every member's balance reaches 0.00 GHS.
   * **Reasoning**: Members can pay in installments throughout the week without blocking other members from making contributions.

4. **Sequential Payout Rotation**:
   * **Rule**: The pot recipient is determined deterministically using `(current_week - 1) % total_members`.
   * **Reasoning**: Guarantees members receive the pot strictly in the order they joined the group.

## Financial Precision
Standard floating-point representation (`float`) introduces binary rounding inaccuracies (e.g., `0.1 + 0.2 != 0.3`). All monetary figures are ingested as string representations and processed strictly using Python's `decimal.Decimal` type.

## Improvements with More Time
1. **Data Persistence**: Integrate SQLite or JSON file storage so group state persists across application restarts.
2. **REST API Interface**: Wrap core logic with FastAPI/Flask endpoints to support web or mobile frontend clients.
3. **Multi-Group Management**: Scale models to allow an administrator to manage multiple distinct Susu groups concurrently.
