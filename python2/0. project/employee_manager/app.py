from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from db import get_connection
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey-please-change")

@app.route("/")
def home():
    return redirect(url_for("list_employees"))

@app.route("/employees")
def list_employees():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, email, department, salary, hire_date
                FROM employees
                ORDER BY id ASC   -- 작은 id가 위로
            """)
            employees = cur.fetchall()
    return render_template("employees/index.html", employees=employees)

@app.route("/employees/new", methods=["GET","POST"])
def create_employee():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        salary = request.form.get("salary", "").strip()
        hire_date = request.form.get("hire_date", "").strip()

        # 검증
        errors = []
        if not name:
            errors.append("이름은 필수입니다.")
        if not email or "@" not in email:
            errors.append("올바른 이메일이 필요합니다.")
        if not department:
            errors.append("부서는 필수입니다.")
        if not salary:
            errors.append("급여는 필수입니다.")
        else:
            try:
                float(salary)
            except ValueError:
                errors.append("급여는 숫자여야 합니다.")
        if not hire_date:
            errors.append("입사일은 필수입니다.")
        else:
            try:
                datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                errors.append("입사일은 YYYY-MM-DD 형식이어야 합니다.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("employees/form.html", mode="create", form=request.form)

        # INSERT
        with get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO employees (name, email, department, salary, hire_date)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (name, email, department, salary, hire_date))
                conn.commit()
                flash("직원이 추가되었습니다.", "success")
                return redirect(url_for("list_employees"))
            except Exception as ex:
                conn.rollback()
                flash(f"추가 중 오류: {ex}", "danger")
                return render_template("employees/form.html", mode="create", form=request.form)

    return render_template("employees/form.html", mode="create", form={})

@app.route("/employees/<int:emp_id>")
def view_employee(emp_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
            emp = cur.fetchone()
    return render_template("employees/_view.html", emp=emp)

@app.route("/employees/<int:emp_id>/edit", methods=["GET", "POST"])
def edit_employee(emp_id):
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        salary = request.form.get("salary", "").strip()
        hire_date = request.form.get("hire_date", "").strip()

        errors = []
        if not name: errors.append("이름은 필수입니다.")
        if not email or "@" not in email: errors.append("올바른 이메일이 필요합니다.")
        if not department: errors.append("부서는 필수입니다.")
        try:
            float(salary)
        except:
            errors.append("급여는 숫자여야 합니다.")
        try:
            datetime.strptime(hire_date, "%Y-%m-%d")
        except:
            errors.append("입사일은 YYYY-MM-DD 형식이어야 합니다.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("employees/form.html", mode="edit", emp_id=emp_id, form=request.form)

        with get_connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE employees
                        SET name=%s, email=%s, department=%s, salary=%s, hire_date=%s
                        WHERE id=%s
                    """, (name, email, department, salary, hire_date, emp_id))
                conn.commit()
                flash("수정되었습니다.", "success")
                return redirect(url_for("list_employees"))
            except Exception as ex:
                conn.rollback()
                flash(f"수정 중 오류: {ex}", "danger")
                return render_template("employees/form.html", mode="edit", emp_id=emp_id, form=request.form)

    # GET: 기존 데이터
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees WHERE id=%s", (emp_id,))
            emp = cur.fetchone()
    if not emp:
        flash("해당 직원이 없습니다.", "warning")
        return redirect(url_for("list_employees"))

    form = {
        "name": emp["name"],
        "email": emp["email"],
        "department": emp["department"],
        "salary": emp["salary"],
        "hire_date": emp["hire_date"].strftime("%Y-%m-%d"),
    }
    return render_template("employees/form.html", mode="edit", emp_id=emp_id, form=form)

@app.route("/employees/<int:emp_id>/delete", methods=["POST"])
def delete_employee(emp_id):
    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
            conn.commit()
            flash("삭제되었습니다.", "success")
        except Exception as ex:
            conn.rollback()
            flash(f"삭제 중 오류: {ex}", "danger")
    return redirect(url_for("list_employees"))

if __name__ == "__main__":
    app.run(debug=True)