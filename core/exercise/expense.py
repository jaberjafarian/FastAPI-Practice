from fastapi import FastAPI, HTTPException, status, Body

app = FastAPI(title="Expenses API")

# دیکشنری در حافظه: کلید = ID ، مقدار = دیکشنری هزینه
expenses = {}
next_id = 0


# ---------- Create ----------
@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(
    description: str = Body(...),
    amount: float = Body(...)
):
    global next_id
    
    new_expense = {
        "id": next_id,
        "description": description,
        "amount": amount
    }
    
    expenses[next_id] = new_expense
    next_id += 1
    
    return new_expense


# ---------- Read (دریافت همه) ----------
@app.get("/expenses")
def get_all_expenses():
    return list(expenses.values())


# ---------- Read (دریافت یک مورد) ----------
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expenses[expense_id]


# ---------- Update ----------
@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    description: str = Body(...),
    amount: float = Body(...)
):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expenses[expense_id] = {
        "id": expense_id,
        "description": description,
        "amount": amount
    }
    
    return expenses[expense_id]


# ---------- Delete ----------
@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    del expenses[expense_id]


