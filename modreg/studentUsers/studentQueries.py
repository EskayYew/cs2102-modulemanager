from modreg import db, login_manager
#Modules that are prereqs for the module the student has highlighted
def get_missing_prereq_modules(student_id, module_code):
    query = "SELECT * FROM Prerequisites" \
            "WHERE Prerequisites.modcode = ('{}')" \
            "AND" \
            "NOT EXISTS (" \
            "SELECT * " \
            "FROM " \
            "Completions" \
            "WHERE" \
            "Completions.modcode = Prequisites.prereq" \
            "AND Completions.uid = ({}))" \
            "" \
            "".format(module_code, student_id)
    missing_prereq_modules = db.session.execute(query).fetchall()
    return missing_prereq_modules
