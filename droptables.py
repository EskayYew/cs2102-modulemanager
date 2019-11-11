from modreg import db, create_app

app = create_app()

with app.app_context():
    db.engine.execute("""
    DROP TABLE IF EXISTS webusers CASCADE;
    DROP TABLE IF EXISTS webadmins CASCADE;
    DROP TABLE IF EXISTS students CASCADE;
    DROP TABLE IF EXISTS exchanges CASCADE;
    DROP TABLE IF EXISTS faculties CASCADE;
    DROP TABLE IF EXISTS gets CASCADE;
    DROP TABLE IF EXISTS completions CASCADE;
    DROP TABLE IF EXISTS bids CASCADE;
    DROP TABLE IF EXISTS lectures CASCADE;
    DROP TABLE IF EXISTS majoring CASCADE;
    DROP TABLE IF EXISTS majors CASCADE;
    DROP TABLE IF EXISTS minoring CASCADE;
    DROP TABLE IF EXISTS minors CASCADE;
    DROP TABLE IF EXISTS modules CASCADE;
    DROP TABLE IF EXISTS preclusions CASCADE;
    DROP TABLE IF EXISTS prerequisites CASCADE;
    DROP TABLE IF EXISTS slots CASCADE;

    DROP FUNCTION IF EXISTS hash_proc;
    DROP FUNCTION IF EXISTS create_student_user;
    DROP FUNCTION IF EXISTS dual_preclusion;
    DROP FUNCTION IF EXISTS compute_workload;
    DROP FUNCTION IF EXISTS time_clash;
    DROP FUNCTION IF EXISTS remove_cyclic_prereq;
    DROP FUNCTION IF EXISTS DFS_fulfill;
    DROP FUNCTION IF EXISTS findNeededModules;
    DROP FUNCTION IF EXISTS compute_year;
    DROP FUNCTION IF EXISTS handle_bit;
    DROP TRIGGER IF EXISTS proc_bid ON bids;
    """)