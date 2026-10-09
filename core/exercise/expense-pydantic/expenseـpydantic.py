from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Expenses API")


# ---------- Pydantic Models ----------

class ExpenseCreate(BaseModel):
    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="توضیح هزینه"
    )
    amount: float = Field(
        ...,
        gt=0,
        description="مبلغ هزینه"
    )


class ExpenseOut(BaseModel):
    id: int
    description: str
    amount: float


# ---------- In-memory storage ----------

expenses: dict[int, ExpenseOut] = {}
next_id = 0


# ---------- Create ----------

@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseOut)
def create_expense(data: ExpenseCreate) -> ExpenseOut:
    global next_id

    new_expense = ExpenseOut(
        id=next_id,
        description=data.description,
        amount=data.amount
    )
    expenses[next_id] = new_expense
    next_id += 1

    return new_expense


# ---------- Get all ----------

@app.get("/expenses", response_model=list[ExpenseOut])
def get_all_expenses() -> list[ExpenseOut]:
    return list(expenses.values())


# ---------- Get one ----------

@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int) -> ExpenseOut:
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


# ---------- Update ----------

@app.put("/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, data: ExpenseCreate) -> ExpenseOut:
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated = ExpenseOut(
        id=expense_id,
        description=data.description,
        amount=data.amount
    )
    expenses[expense_id] = updated
    return updated


# ---------- Delete ----------

@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int) -> None:
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    del expenses[expense_id]
