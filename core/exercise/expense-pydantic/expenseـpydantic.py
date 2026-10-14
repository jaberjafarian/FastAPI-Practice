from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uuid

app = FastAPI(title="Expenses API")


# ---------- Pydantic Models ----------

class ExpenseCreateSchema(BaseModel):
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


class ExpenseOutSchema(BaseModel):
    id: int
    description: str
    amount: float


# ---------- In-memory storage ----------

expenses: dict[int, ExpenseOutSchema] = {}
next_id = new_id = int(uuid.uuid4())


# ---------- Create ----------

@app.post("/expenses", status_code=status.HTTP_201_CREATED, response_model=ExpenseOutSchema)
def create_expense(data: ExpenseCreateSchema) -> ExpenseOutSchema:
    global next_id

    new_expense = ExpenseOutSchema(
        id=next_id,
        description=data.description,
        amount=data.amount
    )
    expenses[next_id] = new_expense

    return new_expense


# ---------- Get all ----------

@app.get("/expenses", response_model=list[ExpenseOutSchema])
def get_all_expenses() -> list[ExpenseOutSchema]:
    return list(expenses.values())


# ---------- Get one ----------

@app.get("/expenses/{expense_id}", response_model=ExpenseOutSchema)
def get_expense(expense_id: int) -> ExpenseOutSchema:
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


# ---------- Update ----------

@app.put("/expenses/{expense_id}", response_model=ExpenseOutSchema)
def update_expense(expense_id: int, data: ExpenseCreateSchema) -> ExpenseOutSchema:
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated = ExpenseOutSchema(
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
